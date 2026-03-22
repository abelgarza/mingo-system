import logging
import json
from pathlib import Path
from oracle_tec import OracleManager

# Set up logging to see what the library is doing under the hood
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

def main():
    # Point to the local .env file in the current project root
    env_file_path = "/home/abelg/dev/mingo-system/.env"
    
    # Initialize the Manager with Thick Mode enabled
    manager = OracleManager(
        env_path=env_file_path,
        thick_mode=True,
        lib_dir="/opt/oracle/instantclient_19_30"
    )

    try:
        # Get the client for the REPORTS environment
        # According to the legacy client, these were the environment variables used:
        client = manager.get_client(
            user_env_var="ORACLE_USER",
            pwd_env_var="PASSWORD_REPORTS",
            dsn_env_var="DNS_REPORTS"
        )

        print("--- Executing Query ---")
        # Oracle uses FETCH FIRST n ROWS ONLY instead of LIMIT
        sql = "SELECT * FROM REPORTS.CLIENTES_DIGITALES FETCH FIRST 10 ROWS ONLY"
        
        results = client.query(sql)
        
        print(f"\n--- Results ({len(results)} rows fetched) ---")
        for i, row in enumerate(results):
            # Print each row compactly
            print(f"Row {i+1}: {row}")

    except Exception as e:
        print(f"\nFailed to execute query: {e}")
    finally:
        manager.close_all()

if __name__ == "__main__":
    main()
