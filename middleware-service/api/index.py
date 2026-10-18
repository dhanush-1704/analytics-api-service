import os
import threading
import time
import uuid
from collections import defaultdict, deque

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

EMAIL = os.getenv("EMAIL", "23f2001912@ds.study.iitm.ac.in")
ASSIGNED_ORIGIN = "https://app-t6f4lz.example.com"
EXAM_ORIGIN = os.getenv("EXAM_ORIGIN", "")
ALLOWED_ORIGINS = [ASSIGNED_ORIGIN] + ([EXAM_ORIGIN] if EXAM_ORIGIN else [])
RATE_LIMIT = 14
WINDOW_SECONDS = 10.0

app = FastAPI(title="Middleware Stack API")
_lock = threading.Lock()
_events = defaultdict(deque)


def get_retry_after(client_id: str):
    now = time.monotonic()
    with _lock:
        bucket = _events[client_id]
        while bucket and now - bucket[0] >= WINDOW_SECONDS:
            bucket.popleft()
        if len(bucket) >= RATE_LIMIT:
            return max(1, int(WINDOW_SECONDS - (now - bucket[0]) + 0.999))
        bucket.append(now)
        return None


@app.middleware("http")
async def request_context_and_limit(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request.state.request_id = request_id
    client_id = request.headers.get("X-Client-Id") or (request.client.host if request.client else "anonymous")
    retry_after = get_retry_after(client_id)
    if retry_after is not None:
        response = JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded"},
            headers={"Retry-After": str(retry_after), "X-Request-ID": request_id},
        )
        return response
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


# Add CORS as the outer middleware so preflight requests can be handled before routing.
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["X-Request-ID", "X-Client-Id", "Content-Type"],
    expose_headers=["X-Request-ID", "Retry-After"],
    allow_credentials=False,
)


@app.get("/ping")
def ping(request: Request):
    return {"email": EMAIL, "request_id": request.state.request_id}
