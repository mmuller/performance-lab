import asyncio
import json
import logging
import os
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

WORK_CAPACITY_LIMIT = 5
WORK_PROCESSING_DELAY_MS = int(os.getenv("WORK_PROCESSING_DELAY_MS", "150"))

work_semaphore = asyncio.Semaphore(WORK_CAPACITY_LIMIT)
active_work_requests = 0
active_work_requests_lock = asyncio.Lock()


@app.middleware("http")
async def log_request(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or str(uuid4())
    started_at = time.perf_counter()
    status_code = 500
    request.state.request_id = request_id
    request.state.active_requests = 0

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
                    "active_requests": request.state.active_requests,
                    "capacity_limit": WORK_CAPACITY_LIMIT,
                }
            )
        )


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/work")
async def work(request: Request) -> dict[str, str | int]:
    global active_work_requests

    async with work_semaphore:
        async with active_work_requests_lock:
            active_work_requests += 1
            current_active_requests = active_work_requests

        request.state.active_requests = current_active_requests

        try:
            await asyncio.sleep(WORK_PROCESSING_DELAY_MS / 1000)
        finally:
            async with active_work_requests_lock:
                active_work_requests -= 1

    return {
        "status": "completed",
        "request_id": request.state.request_id,
        "processing_delay_ms": WORK_PROCESSING_DELAY_MS,
        "active_requests": current_active_requests,
        "capacity_limit": WORK_CAPACITY_LIMIT,
    }
