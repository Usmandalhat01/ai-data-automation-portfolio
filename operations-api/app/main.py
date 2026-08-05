from datetime import datetime
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="Operations Automation API",
    version="1.0.0",
    description="A small API for tracking operational requests and automation jobs.",
)

Status = Literal["pending", "in_progress", "completed", "failed"]


class JobCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    owner: str = Field(min_length=2, max_length=80)
    priority: Literal["low", "medium", "high"] = "medium"


class Job(JobCreate):
    id: int
    status: Status = "pending"
    created_at: datetime


jobs: dict[int, Job] = {}
next_id = 1


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/jobs", response_model=list[Job])
def list_jobs(status: Status | None = None) -> list[Job]:
    records = list(jobs.values())
    if status:
        records = [job for job in records if job.status == status]
    return records


@app.post("/jobs", response_model=Job, status_code=201)
def create_job(payload: JobCreate) -> Job:
    global next_id
    job = Job(
        id=next_id,
        title=payload.title.strip(),
        owner=payload.owner.strip(),
        priority=payload.priority,
        created_at=datetime.utcnow(),
    )
    jobs[next_id] = job
    next_id += 1
    return job


@app.patch("/jobs/{job_id}/status", response_model=Job)
def update_job_status(job_id: int, status: Status) -> Job:
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    updated = job.model_copy(update={"status": status})
    jobs[job_id] = updated
    return updated


@app.delete("/jobs/{job_id}", status_code=204)
def delete_job(job_id: int) -> None:
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    del jobs[job_id]
