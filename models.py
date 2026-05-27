from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class ApplicationStatus(str, Enum):
    SAVED = "saved"
    APPLIED = "applied"
    PHONE_SCREEN = "phone_screen"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class JobApplication(BaseModel):
    id: Optional[str] = None
    company: str
    role: str
    job_url: Optional[str] = None
    job_description: Optional[str] = None
    status: ApplicationStatus = ApplicationStatus.SAVED
    match_score: Optional[int] = None
    match_summary: Optional[str] = None
    skill_gaps: Optional[list[str]] = None
    applied_date: Optional[datetime] = None
    follow_up_date: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        use_enum_values = True


class JobApplicationCreate(BaseModel):
    company: str
    role: str
    job_url: Optional[str] = None
    job_description: Optional[str] = None
    status: ApplicationStatus = ApplicationStatus.SAVED
    applied_date: Optional[datetime] = None
    follow_up_date: Optional[datetime] = None
    notes: Optional[str] = None


class StatusUpdate(BaseModel):
    status: ApplicationStatus


class ScoreRequest(BaseModel):
    resume_text: str = Field(..., description="Your resume as plain text")
    job_description: str = Field(..., description="The job description to score against")


class ScoreResult(BaseModel):
    score: int = Field(..., ge=0, le=100, description="Match score from 0 to 100")
    summary: str = Field(..., description="Brief explanation of the match")
    strengths: list[str] = Field(default_factory=list, description="Skills and experiences that match well")
    skill_gaps: list[str] = Field(default_factory=list, description="Skills or experience you are missing")
    recommendation: str = Field(..., description="Short recommendation on whether to apply")
