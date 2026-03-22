# oracle-tec

`oracle-tec` is the modernization layer for Oracle database interactions within the **mingo-system**. It uses the modern `python-oracledb` driver to provide a clean, OOP-based interface.

## Vision

- **Modern Driver:** Built on `python-oracledb`. `mingo-system` defaults to and highly prefers the **"Thin"** mode (direct connection), which means **this library does not depend on any external Oracle binaries by default**.
- **Python 3.12+ Support:** Designed for the latest Python versions, avoiding common setuptools/packaging issues of legacy drivers.
- **Improved Abstraction:** Moving away from procedural scripts to robust, reusable classes and clear APIs.
- **Thick Mode Fallback:** While we aim for complete binary independence, "Thick" mode (requiring the Instant Client) is fully supported strictly as a fallback for specific legacy database configurations.

## Key Features

- **Hybrid Mode Support:** Seamlessly handles switching between "Thin" and "Thick" modes.
- **Auto-Healing:** Automatically handles password rotations on expiration.
- **Context Manager Support:** Proper resource management via `with` statements.
- **Type-Safe Interfaces:** Comprehensive type hints for all database operations.

## Setup

For 99% of use cases, no system-level setup is required (Thin mode). 

If your specific database requires "Thick" mode, see [docs/ORACLE_SETUP.md](../../docs/ORACLE_SETUP.md) for information on setting up the local Oracle Instant Client.
