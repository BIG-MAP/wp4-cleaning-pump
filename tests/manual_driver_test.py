import os
import time

from cleaning_pump_driver.driver import CleaningPump

serial_port = os.environ.get("CLEANING_PUMP_SERIAL_PORT")

pump = CleaningPump(serial_port)

print(f"Pump busy: {pump.is_busy()}")

pump.start()

print(f"Pump busy: {pump.is_busy()}")

time.sleep(5)

pump.stop()

print(f"Pump busy: {pump.is_busy()}")
