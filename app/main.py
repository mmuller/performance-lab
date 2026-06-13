import json
import logging
import sys
import time
from uuid import uuid4

from fastapi import FastAPI, Request


logger = logging.getLogger("performance_lab.requests")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)


app = FastAPI(title="Performance Lab")


@app.middleware("http")
async def log_request(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or str(uuid4())
    started_at = time.perf_counter()
    status_code = 500

    try:
        response = await call_next(request)
        status_code = response.status_code
        response.headers["x-request-id"] = request_id
        return response
    finally:
        duration_ms = round((time.perf_counter() - started_at) * 1000, 2)
        logger.info(
            json.dumps(
                {
                    "request_id": request_id,
                    "route": request.url.path,
                    "status": status_code,
                    "duration_ms": duration_ms,
                }
            )
        )


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/work")
async def work() -> dict[str, str]:
    return {"status": "completed", "result": "simulated work"}
