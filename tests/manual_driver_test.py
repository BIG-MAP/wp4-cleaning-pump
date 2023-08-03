import logging
import os
import time

from cleaning_pump_driver.driver import CleaningPump

logging.basicConfig(level=logging.INFO)

serial_port = os.environ.get("CLEANING_PUMP_SERIAL_PORT")

pump = CleaningPump(serial_port)
pump.start()
time.sleep(5)
pump.stop()
