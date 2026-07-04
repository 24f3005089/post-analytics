from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

EMAIL = "YOUR_REGISTERED_EMAIL"
API_KEY = "ak_h3okoj3oz7uakwvq5bepewb0"

app = FastAPI()

# Allow browser access for grading
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Event(BaseModel):
    user: str
    amount: float
    ts: int


class AnalyticsRequest(BaseModel):
    events: List[Event]


@app.get("/")
def root():
    return {"status": "running"}


@app.post("/analytics")
def analytics(
    request: AnalyticsRequest,
    x_api_key: str = Header(default=None),
):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
        )

    total_events = len(request.events)

    unique_users = len(
        {event.user for event in request.events}
    )

    revenue = 0.0

    user_totals = {}

    for event in request.events:
        if event.amount > 0:
            revenue += event.amount
            user_totals[event.user] = (
                user_totals.get(event.user, 0.0)
                + event.amount
            )

    top_user = ""

    if user_totals:
        top_user = max(
            user_totals,
            key=user_totals.get,
        )

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user,
    }