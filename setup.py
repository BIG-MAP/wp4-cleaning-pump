from distutils.core import setup

setup(
    name="cleaning-pump",
    version="0.1",
    description="SDK for Cleaning Pump",
    packages=["cleaning_pump_driver", "cleaning_pump_http"],
    install_requires=["pyserial", "fastapi", "uvicorn", "PyCmdMessenger"],
)
