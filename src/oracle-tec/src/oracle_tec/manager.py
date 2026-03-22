from pathlib import Path
from typing import Optional, Dict, List
from .client import OracleClient

class OracleManager:
    """
    Manages multiple OracleClient instances sharing shared environment settings.
    """
    
    def __init__(
        self, 
        env_path: Optional[str] = None, 
        thick_mode: bool = False, 
        lib_dir: Optional[str] = None
    ):
        self.env_path = env_path
        self.thick_mode = thick_mode
        self.lib_dir = lib_dir
        self.clients: Dict[str, OracleClient] = {}

    def get_client(
        self, 
        user_env_var: str, 
        pwd_env_var: str, 
        dsn_env_var: str
    ) -> OracleClient:
        """
        Retrieves or creates an OracleClient for the given env variable set.
        """
        client_id = f"{user_env_var}:{dsn_env_var}"
        if client_id not in self.clients:
            self.clients[client_id] = OracleClient(
                user_env_var=user_env_var,
                pwd_env_var=pwd_env_var,
                dsn_env_var=dsn_env_var,
                env_path=self.env_path,
                thick_mode=self.thick_mode,
                lib_dir=self.lib_dir
            )
        return self.clients[client_id]

    def close_all(self) -> None:
        """Closes all managed clients."""
        for client in self.clients.values():
            client.close()
        self.clients.clear()
