import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import JobApplicationCreate, StatusUpdate, ScoreRequest, ScoreResult
import db
from scorer import score_resume_match, score_resume_match_mock
from dotenv import load_dotenv

load_dotenv()

# Set USE_MOCK=true in .env to run without an OpenAI key
USE_MOCK = os.getenv("USE_MOCK", "false").lower() == "true"

app = FastAPI(
    title="AI Job Tracker",
    description="Track job applications and score resume-to-job matches using AI.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "AI Job Tracker API is running.", "docs": "/docs"}


@app.get("/applications")
def list_applications():
    """Return all job applications sorted by most recent."""
    try:
        return db.list_applications()
    except EnvironmentError as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.post("/applications", status_code=201)
def create_application(data: JobApplicationCreate):
    """Add a new job application."""
    try:
        return db.create_application(data)
    except EnvironmentError as e:
        raise HTTPException(status_code=503, detail=str(e))


@app.get("/applications/{app_id}")
def get_application(app_id: str):
    """Get a single job application by ID."""
    try:
        result = db.get_application(app_id)
    except EnvironmentError as e:
        raise HTTPException(status_code=503, detail=str(e))
    if not result:
        raise HTTPException(status_code=404, detail="Application not found")
    return result


@app.put("/applications/{app_id}/status")
def update_status(app_id: str, body: StatusUpdate):
    """Update the status of a job application."""
    try:
        result = db.update_status(app_id, body)
    except EnvironmentError as e:
        raise HTTPException(status_code=503, detail=str(e))
    if not result:
        raise HTTPException(status_code=404, detail="Application not found")
    return result


@app.post("/applications/{app_id}/score", response_model=ScoreResult)
def score_application(app_id: str, body: ScoreRequest):
    """
    Score how well a resume matches a job description using GPT-4o.
    Pass USE_MOCK=true in your .env to test without an API key.
    """
    scorer = score_resume_match_mock if USE_MOCK else score_resume_match
    try:
        result = scorer(body)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scoring failed: {str(e)}")

    # Persist score back to database
    try:
        db.save_score(app_id, result.score, result.summary, result.skill_gaps)
    except EnvironmentError:
        pass  # DB not configured — still return the score

    return result


@app.delete("/applications/{app_id}", status_code=204)
def delete_application(app_id: str):
    """Delete a job application by ID."""
    try:
        deleted = db.delete_application(app_id)
    except EnvironmentError as e:
        raise HTTPException(status_code=503, detail=str(e))
    if not deleted:
        raise HTTPException(status_code=404, detail="Application not found")
    return None
