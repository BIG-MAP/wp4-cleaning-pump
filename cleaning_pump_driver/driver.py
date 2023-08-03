import os
from typing import Optional

from cleaning_pump_driver.arduino import ArduinoController

serial_port = os.environ.get("CLEANING_PUMP_SERIAL_PORT")


class CleaningPump(ArduinoController):
    def __init__(self, port: str) -> None:
        """
        A diaphragm pump with a DAC to control the speed.
        Speed is set by a voltage between 0 and 4096.
        """
        super().__init__(port)
        self._default_speed = 1024

    def start(self, speed: Optional[int] = None):
        """
        Starts the pump at a given speed, a range between 0 and 4096.
        If no speed is given, the pump will start at the default speed.
        """
        if self._is_busy():
            raise RuntimeError("Pump is already running")

        self._set_voltage(speed or self._default_speed)
        self._cycle_pump()

    def stop(self):
        self._stop_pump()

    def is_busy(self) -> bool:
        return self._is_busy()

    def close(self):
        self.stop()
        self._close()
