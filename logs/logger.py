import inspect
import os
from typing import Optional
from config.globals import BACKEND_API_URL
import httpx


class Logger:
    def __init__(self):
        self.logger = __name__
        self.DEBUG = "DEBUG"
        self.INFO = "INFO"
        self.WARNING = "WARNING"
        self.ERROR = "ERROR"
        self.CRITICAL = "CRITICAL"

    async def log(self, msg: str, level: Optional[str] = "DEBUG"):
        url = f"{BACKEND_API_URL}/api/v1/logs/add"
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        a = str(os.path.abspath(os.path.dirname(__file__))).replace("/logs", "")
        filename = f".{module.__file__.replace(a, " ")}"
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url, json={"filename": filename, "message": str(msg), "level": level}
            )

            return response.json()
