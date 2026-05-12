from __future__ import annotations

import json

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

from app.render import render_api_summary, render_overview, render_playbooks, render_queue
from app.services.outreach_service import build_service

app = FastAPI(
    title="Advisor Outreach Orchestrator",
    version="0.1.0",
    description=(
        "Advisor workflow engine for student outreach prioritization, escalation routing, "
        "and channel-aware intervention planning."
    ),
)

service = build_service()


@app.get("/", response_class=HTMLResponse)
def overview() -> str:
    return render_overview()


@app.get("/queue", response_class=HTMLResponse)
def queue_page() -> str:
    return render_queue()


@app.get("/playbooks", response_class=HTMLResponse)
def playbooks_page() -> str:
    return render_playbooks()


@app.get("/api-summary", response_class=HTMLResponse)
def api_summary_page() -> str:
    return render_api_summary()


@app.get("/api/dashboard/summary")
def dashboard_summary() -> dict:
    return service.summary()


@app.get("/api/queue")
def queue() -> list[dict]:
    return service.outreach_queue()


@app.get("/api/lanes")
def lanes() -> list[dict]:
    return service.lane_breakdown()


@app.get("/api/students/{student_id}")
def student(student_id: str) -> dict:
    value = service.student(student_id)
    if value is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return value


@app.get("/api/sample")
def sample() -> dict:
    return service.sample_payload()


@app.get("/openapi.json")
def openapi_spec() -> JSONResponse:
    return JSONResponse(json.loads(json.dumps(app.openapi())))


if __name__ == "__main__":
    import os

    import uvicorn

    port = int(os.environ.get("PORT", "4728"))
    uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=False)
