import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from models import ScoreRequest, ScoreResult

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

SYSTEM_PROMPT = """
You are an expert technical recruiter and career coach.
You will be given a candidate's resume and a job description.
Your job is to evaluate how well the candidate matches the role.

Return a JSON object with exactly these fields:
- score: integer from 0 to 100 (overall match percentage)
- summary: string, 2-3 sentence summary of the match
- strengths: list of strings, specific skills or experiences that match well
- skill_gaps: list of strings, specific skills or experience the candidate is missing
- recommendation: string, one sentence recommendation (e.g. "Strong match, apply now" or "Missing key skills, consider upskilling first")

Be specific and honest. Do not inflate scores.
"""


def score_resume_match(request: ScoreRequest) -> ScoreResult:
    """
    Send resume and job description to GPT-4o and return a structured match score.
    Raises ValueError if the LLM response cannot be parsed.
    """
    user_message = f"""RESUME:
{request.resume_text}

---

JOB DESCRIPTION:
{request.job_description}
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
    )

    raw = response.choices[0].message.content

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse LLM response as JSON: {e}\nRaw: {raw}")

    return ScoreResult(
        score=int(data.get("score", 0)),
        summary=data.get("summary", ""),
        strengths=data.get("strengths", []),
        skill_gaps=data.get("skill_gaps", []),
        recommendation=data.get("recommendation", ""),
    )


def score_resume_match_mock(request: ScoreRequest) -> ScoreResult:
    """
    Mock version of score_resume_match for local testing without an OpenAI key.
    Returns a realistic-looking but fake score.
    """
    return ScoreResult(
        score=72,
        summary=(
            "The candidate has strong Python and data analysis skills that align with "
            "the role. However, the position requires production ML deployment experience "
            "which is not clearly demonstrated in the resume."
        ),
        strengths=[
            "Proficient in Python and pandas",
            "Experience with API development using FastAPI",
            "Supabase and PostgreSQL database experience",
            "Demonstrated AI/ML project work",
        ],
        skill_gaps=[
            "No mention of Docker or containerization",
            "Limited production ML model deployment experience",
            "No experience with MLflow or model versioning tools",
        ],
        recommendation="Good candidate with room to grow. Apply and highlight your AI project experience.",
    )
