import os
from supabase import create_client, Client
from dotenv import load_dotenv
from models import JobApplication, JobApplicationCreate, StatusUpdate
from datetime import datetime, timezone
import uuid

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

TABLE = "job_applications"


def get_client() -> Client:
    """Return a Supabase client. Raises if env vars are missing."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise EnvironmentError(
            "SUPABASE_URL and SUPABASE_KEY must be set in environment variables."
        )
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def list_applications() -> list[dict]:
    """Fetch all job applications ordered by created_at descending."""
    client = get_client()
    response = (
        client.table(TABLE)
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )
    return response.data


def get_application(app_id: str) -> dict | None:
    """Fetch a single application by ID."""
    client = get_client()
    response = (
        client.table(TABLE)
        .select("*")
        .eq("id", app_id)
        .single()
        .execute()
    )
    return response.data


def create_application(data: JobApplicationCreate) -> dict:
    """Insert a new job application and return the created record."""
    client = get_client()
    now = datetime.now(timezone.utc).isoformat()
    record = {
        "id": str(uuid.uuid4()),
        "company": data.company,
        "role": data.role,
        "job_url": data.job_url,
        "job_description": data.job_description,
        "status": data.status,
        "applied_date": data.applied_date.isoformat() if data.applied_date else None,
        "follow_up_date": data.follow_up_date.isoformat() if data.follow_up_date else None,
        "notes": data.notes,
        "created_at": now,
        "updated_at": now,
    }
    response = client.table(TABLE).insert(record).execute()
    return response.data[0]


def update_status(app_id: str, status_update: StatusUpdate) -> dict | None:
    """Update the status of a job application."""
    client = get_client()
    now = datetime.now(timezone.utc).isoformat()
    response = (
        client.table(TABLE)
        .update({"status": status_update.status, "updated_at": now})
        .eq("id", app_id)
        .execute()
    )
    return response.data[0] if response.data else None


def save_score(app_id: str, score: int, summary: str, skill_gaps: list[str]) -> dict | None:
    """Persist the AI match score and summary back to the database."""
    client = get_client()
    now = datetime.now(timezone.utc).isoformat()
    response = (
        client.table(TABLE)
        .update({
            "match_score": score,
            "match_summary": summary,
            "skill_gaps": skill_gaps,
            "updated_at": now,
        })
        .eq("id", app_id)
        .execute()
    )
    return response.data[0] if response.data else None


def delete_application(app_id: str) -> bool:
    """Delete a job application by ID. Returns True if deleted."""
    client = get_client()
    response = client.table(TABLE).delete().eq("id", app_id).execute()
    return len(response.data) > 0
