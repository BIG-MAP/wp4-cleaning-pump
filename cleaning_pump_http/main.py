import logging
import os
from dataclasses import dataclass
from typing import Any, Optional

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from cleaning_pump_driver.driver import CleaningPump

serial_port: Optional[str] = os.environ.get("CLEANING_PUMP_SERIAL_PORT")
if serial_port is None:
    raise RuntimeError("CLEANING_PUMP_SERIAL_PORT environment variable is not set")

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def lifespan(app: FastAPI):
    yield
    app.state.logger.info("Shutting down the cleaning pump")
    app.state.pump.close()


app = FastAPI(lifespan=lifespan)
app.state.pump = CleaningPump(serial_port)
app.state.logger = logger


@dataclass
class APIResponse:
    data: Optional[Any] = None
    message: Optional[str] = None
    error: Optional[str] = None

    def json(self):
        return self.__dict__


@app.post("/start")
async def stirr(speed: int):
    try:
        app.state.pump.start(speed=speed)
    except RuntimeError as e:
        return JSONResponse(status_code=400, content=APIResponse(error=str(e)).json())
    return APIResponse(message=f"Pumping at {speed}")


@app.post("/stop")
async def stop_stirring():
    app.state.pump.stop()
    return APIResponse(message="Stopped pumping")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
