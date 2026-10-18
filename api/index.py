import os
from collections import defaultdict

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Any

API_KEY = os.environ.get("API_KEY", "ak_o58uovw9911xg3iti7ydidyy")
EMAIL = os.environ.get("EMAIL", "23f2001912@ds.study.iitm.ac.in")

app = FastAPI(title="Analytics API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-API-Key"],
)

class Event(BaseModel):
    user: str
    amount: float
    ts: int

class AnalyticsRequest(BaseModel):
    events: list[Event] = Field(default_factory=list)

@app.post("/analytics")
def analytics(
    payload: AnalyticsRequest,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    events = payload.events
    user_totals = defaultdict(float)
    for event in events:
        if event.amount > 0:
            user_totals[event.user] += event.amount

    top_user = max(user_totals, key=user_totals.get) if user_totals else None
    return {
        "email": EMAIL,
        "total_events": len(events),
        "unique_users": len({event.user for event in events}),
        "revenue": sum(event.amount for event in events if event.amount > 0),
        "top_user": top_user,
    }
