import PyCmdMessenger


import logging
import time


class ArduinoController:
    def __init__(self, port: str) -> None:
        self._busy = False
        self._logger = logging.getLogger(__class__.__name__)

        _arduino = PyCmdMessenger.ArduinoBoard(port, baud_rate=115200, timeout=10)
        # List of command names (and formats for their associated arguments).
        # These must be in the same order as in the sketch.
        commands = [
            ["kWatchdog", "s"],
            ["kAcknowledge", "s"],
            ["kError", "s"],
            ["kSetVoltage", "i"],
            ["kStopPump", "s"],
            ["kCyclePump", ""],
        ]
        # Initialize the messenger
        self._messenger = PyCmdMessenger.CmdMessenger(_arduino, commands)

        # Wait for arduino to come up
        response = self._messenger.receive()
        self._logger.info(f"Arduino initialization: {response}")

    def _set_voltage(self, voltage: int):
        """
        Sets the voltage of the DAC controlling the pump. Range between 0 and 4096.
        """

        self._messenger.send("kSetVoltage", voltage)

        response = self._messenger.receive()
        self._logger.info(f"kSetVoltage: {response[1]}")

    def _stop_pump(self):
        self._messenger.send("kStopPump")

        response = self._messenger.receive()
        self._logger.info(f"kStopPump: {response[1]}")

        self._busy = False

    def _cycle_pump(self):
        """
        Starts or stops the pump.
        """

        self._messenger.send("kCyclePump")

        response = self._messenger.receive()
        self._logger.info(f"kCyclePump: {response[1]}")

        time.sleep(0.4)

        self._busy = not self._busy

    def _is_busy(self) -> bool:
        return self._busy