import logging
import os
import time
from enum import Enum

import PyCmdMessenger
from pydantic import BaseModel, Field

serial_port = os.environ.get("CLEANING_PUMP_SERIAL_PORT")

pumpState = False

arduino = PyCmdMessenger.ArduinoBoard(serial_port, baud_rate=115200, timeout=10)

# List of command names (and formats for their associated arguments). These must
# be in the same order as in the sketch.
commands = [
    ["kWatchdog", "s"],
    ["kAcknowledge", "s"],
    ["kError", "s"],
    ["kSetVoltage", "i"],
    ["kStopPump", "s"],
    ["kCyclePump", ""],
]

# Initialize the messenger
comm = PyCmdMessenger.CmdMessenger(arduino, commands)
# Wait for arduino to come up
msg = comm.receive()
print(msg)


def setVoltage(voltage: int) -> int:
    """Function for setting the voltage of the DAC controlling the pump (0-4096)."""

    comm.send("kSetVoltage", voltage)

    msg = comm.receive()
    logging.info(msg[1])

    return 0


def stopPump() -> int:
    global pumpState
    """Function for stopping the pump."""

    comm.send("kStopPump")

    msg = comm.receive()
    logging.info(msg[1])

    pumpState = False

    return 0


def cyclePump() -> int:
    global pumpState
    """Function for starting or stopping the pump."""

    comm.send("kCyclePump")

    msg = comm.receive()
    logging.info(msg[1])

    time.sleep(0.4)

    pumpState = not pumpState

    return 0


def getPumpState() -> bool:
    """Function for returning the pump state"""
    global pumpState

    return pumpState


class Status(str, Enum):
    stopped = "stopped"
    running = "running"


class PumpSettings(BaseModel):
    speed: int = Field(0, title="The pump speed", ge=0, le=4095, example=1024)
    run: bool = Field(False, title="Start the pump", description="Starts or stops the pump regardless of speed")


class DiaphragmPump:
    status: Status = Status.stopped
    settings: PumpSettings = PumpSettings()

    def startPump(self):
        self.settings.run = True
        self.status = Status.running
        if getPumpState():
            print("Pump already started")
        else:
            cyclePump()
            print("Pump started")

    def stopPump(self):
        if getPumpState():
            stopPump()
            self.settings.run = False
            self.settings.speed = 0
            self.status = Status.stopped
        print("Pump stopped")

    def setSpeed(self, speed: int):
        self.settings.speed = speed
        setVoltage(speed)
        print("Pump speed set to " + str(speed))
