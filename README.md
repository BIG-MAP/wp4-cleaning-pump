# WP4 Cleaning Pump

This repository contains:

- The [driver](./cleaning_pump_driver/) for the pump.
- The [HTTP server](./cleaning_pump_http/) that provides a REST API to control the pump.

## Getting Started

We use the obsolete way of installing Python packages using `setup.py` to avoid issues with the missing Rust compiler for the cryptography package [[1](https://github.com/pyca/cryptography/issues/5771#issuecomment-775016788), [2](https://cryptography.io/en/latest/faq/#why-does-cryptography-require-rust)].

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install the packages
pip install -r requirements.txt
python setup.py install

# Run the manual test
python tests/manual_driver_test.py
```

To start an HTTP server, run:

```bash
CLEANING_PUMP_SERIAL_PORT=/dev/ttyACM0 uvicorn cleaning_pump_http.main:app --host "0.0.0.0" --port 8080
```
