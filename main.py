from fastapi import FastAPI, Header, HTTPException
from fastapi import Request
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
async def analytics(
    request: Request,
    x_api_key: str | None = Header(default=None),
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    body = await request.json()
    events = body.get("events", [])

    total_events = len(events)
    unique_users = len({e["user"] for e in events})

    revenue = 0.0
    user_totals = {}

    for e in events:
        amount = float(e["amount"])
        if amount > 0:
            revenue += amount
            user_totals[e["user"]] = user_totals.get(e["user"], 0) + amount

    top_user = max(user_totals, key=user_totals.get) if user_totals else ""

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user,
    }