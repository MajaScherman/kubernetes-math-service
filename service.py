# /// script
# requires-python = "==3.11.*"
# dependencies = [
#   "uvloop>=0.17.0",
#   "fastapi==0.115.8",
#   "uvicorn==0.15.0",
#   "structlog==21.2.0"
# ]
# [tool.env-checker]
# env_vars = [
#   "PORT=8000",
#   "LOGLEVEL=INFO",
# ]
# ///

import uvloop; uvloop.install()
import logging, os
import structlog
from fastapi import FastAPI
from pydantic import BaseModel
import asyncio

# Logging setup
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(sort_keys=True)
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
logger = structlog.get_logger()

# FastAPI app
app = FastAPI(
    title="Simple Math API",
    description="A simple API to perform basic arithmetic operations",
    version="1.0.0"
)

class AddRequest(BaseModel):
    a: float
    b: float

class AddResponse(BaseModel):
    result: float

@app.post("/", response_model=AddResponse)
async def add_numbers(request: AddRequest):
    logger.info("Received addition request", a=request.a, b=request.b)
    result = request.a + request.b
    await asyncio.sleep(5)  # Simulate a longish-running operation
    logger.info("Computed result", result=result)
    return {"result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
