import os
import uuid
import logging
import oracledb
from pathlib import Path
from typing import Optional, Dict, Any, Union, List, Tuple, Callable
from sqlalchemy import create_engine, text, Engine
from dotenv import load_dotenv, set_key

# Configure basic logging for the library
logger = logging.getLogger(__name__)

class PasswordRotator:
    """Handles Oracle password rotation and .env persistence."""
    
    @staticmethod
    def generate_password() -> str:
        """Generates a secure, Oracle-compatible password."""
        uuid_part = str(uuid.uuid4()).replace('-', '')[:12]
        return f"{uuid_part}#Az1"

    @staticmethod
    def rotate(
        user: str, 
        dsn: str, 
        old_pwd: str, 
        env_path: Path, 
        pwd_env_var: str,
        thick_mode: bool = False
    ) -> str:
        """
        Rotates the password in Oracle and updates the .env file.
        Returns the new password if successful, else the old one.
        """
        new_pwd = PasswordRotator.generate_password()
        logger.info(f"Attempting password rotation for {user} at {dsn}...")

        # Method 1: Using the 'newpassword' parameter (specific to Oracle drivers)
        try:
            # We connect briefly to change the password
            conn = oracledb.connect(
                user=user,
                password=old_pwd,
                dsn=dsn,
                newpassword=new_pwd
            )
            conn.close()
            
            # Persist to .env
            set_key(str(env_path), pwd_env_var, new_pwd)
            logger.info(f"Rotation successful for {user} (Method 1). .env updated.")
            return new_pwd
        except oracledb.DatabaseError as e:
            error_obj, = e.args
            logger.warning(f"Method 1 failed (ORA-{error_obj.code}): {error_obj.message}")
            
            # Method 2: ALTER USER (requires current session)
            try:
                conn = oracledb.connect(user=user, password=old_pwd, dsn=dsn)
                with conn.cursor() as cursor:
                    # Use double quotes for password to avoid syntax issues with special chars
                    cursor.execute(f'ALTER USER {user} IDENTIFIED BY "{new_pwd}" REPLACE "{old_pwd}"')
                conn.close()
                
                set_key(str(env_path), pwd_env_var, new_pwd)
                logger.info(f"Rotation successful for {user} (Method 2). .env updated.")
                return new_pwd
            except Exception as e2:
                logger.error(f"Rotation failed for {user}. Manual intervention required. Error: {e2}")
                return old_pwd

class OracleClient:
    """
    Enhanced Oracle Client with SQLAlchemy support and Auto-Healing.
    """
    
    def __init__(
        self,
        user_env_var: str,
        pwd_env_var: str,
        dsn_env_var: str,
        env_path: Optional[Union[str, Path]] = None,
        thick_mode: bool = False,
        lib_dir: Optional[str] = None
    ):
        self.user_var = user_env_var
        self.pwd_var = pwd_env_var
        self.dsn_var = dsn_env_var
        self.env_path = Path(env_path) if env_path else Path(".env")
        self.thick_mode = thick_mode
        self.lib_dir = lib_dir
        
        self._engine: Optional[Engine] = None
        self._initialize_driver()
        self.refresh_config()

    def _initialize_driver(self) -> None:
        """Initializes thick mode if requested."""
        if self.thick_mode:
            try:
                oracledb.init_oracle_client(lib_dir=self.lib_dir)
            except oracledb.ProgrammingError:
                pass # Already initialized

    def refresh_config(self) -> None:
        """Reloads credentials from the environment."""
        load_dotenv(dotenv_path=self.env_path, override=True)
        self.user = os.getenv(self.user_var)
        self.password = os.getenv(self.pwd_var)
        self.dsn = os.getenv(self.dsn_var)

        if not all([self.user, self.password, self.dsn]):
            logger.warning(f"Incomplete config for {self.user_var}. Check your .env.")

        # Re-create engine if it exists
        if self._engine:
            self._engine.dispose()
            self._engine = None

    @property
    def engine(self) -> Engine:
        """Returns a SQLAlchemy engine, creating it if necessary."""
        if not self._engine:
            # Modern oracledb dialect for SQLAlchemy
            connection_url = f"oracle+oracledb://{self.user}:{self.password}@{self.dsn}"
            self._engine = create_engine(connection_url)
        return self._engine

    def _execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """Decorator-like wrapper for ORA-28001 (Password Expired) auto-healing."""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Extract underlying Oracle error
            orig = getattr(e, "orig", None)
            if orig and isinstance(orig, oracledb.DatabaseError):
                error_obj, = orig.args
                if error_obj.code == 28001:
                    logger.warning(f"Password expired for {self.user} (ORA-28001). Healing...")
                    self.password = PasswordRotator.rotate(
                        user=self.user,
                        dsn=self.dsn,
                        old_pwd=self.password,
                        env_path=self.env_path,
                        pwd_env_var=self.pwd_var,
                        thick_mode=self.thick_mode
                    )
                    self.refresh_config()
                    logger.info("Retrying operation after successful rotation.")
                    return func(*args, **kwargs)
            raise e

    def query(self, sql: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Executes a query and returns a list of dictionaries (rows)."""
        def _run():
            with self.engine.connect() as conn:
                result = conn.execute(text(sql), params or {})
                return [dict(row._mapping) for row in result]
        return self._execute_with_retry(_run)

    def execute(self, sql: str, params: Optional[Dict[str, Any]] = None) -> None:
        """Executes a statement (DDL/DML) with no return value."""
        def _run():
            with self.engine.connect() as conn:
                conn.execute(text(sql), params or {})
                conn.commit()
        self._execute_with_retry(_run)

    def close(self) -> None:
        """Disposes the engine resources."""
        if self._engine:
            self._engine.dispose()
            self._engine = None
