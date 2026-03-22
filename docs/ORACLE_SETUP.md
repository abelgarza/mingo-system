# Oracle Setup & `oracle-tec` Library

This document outlines the usage of the `oracle-tec` library and records the setup for Oracle Instant Client (which is **optional** and only required if "Thick" mode is mandated by legacy systems).

> **Note:** `mingo-system` defaults to and prefers the "Thin" mode of `oracledb`, which **does not** require external Oracle binaries. The Instant Client setup is documented here strictly as a fallback for specific enterprise environments that require "Thick" mode.

## 1. Installation of Instant Client
(The same as before...)

## 2. System Library Configuration
(The same as before...)

## 3. Dependency Fix: libaio
(The same as before...)

## 4. `oracle-tec` Library

`oracle-tec` is the standard library for Oracle database interactions within `mingo-system`, designed to be modern, OOP-based, and resilient.

### Key Features
- **Auto-Healing**: Automatically detects ORA-28001 (Password Expired), rotates the password, updates `.env`, and retries.
- **SQLAlchemy Integrated**: Uses `oracledb` dialect for modern Python support (3.12+).
- **Manager Pattern**: Handles multiple database connections sharing the same environment.

### Installation
```bash
pip install -e src/oracle-tec
```

### Basic Usage
```python
from oracle_tec import OracleManager

manager = OracleManager(thick_mode=True, lib_dir="/opt/oracle/instantclient_19_30")
client = manager.get_client("ORACLE_USER", "PASSWORD_REPORTS", "DNS_REPORTS")

# Execute and get results as dictionaries
results = client.query("SELECT * FROM TABLE FETCH FIRST 10 ROWS ONLY")
```
