# AI Build Log – AI Job Tracker

This document explains how I used AI tools (Claude, GPT-4o) to design and build the AI Job Tracker. Written for reviewers who want to understand how I work with AI as a co-pilot.

## Project Goal

Build a production-style backend service that:
- Tracks job applications with status and deadlines
- Uses GPT-4o to score how well a resume matches a job description
- Stores everything in Supabase (PostgreSQL)
- Exposes a clean REST API built with FastAPI

## How I Used AI Tools

### 1. Architecture Design

I started by prompting Claude with the core requirements and asked it to propose a clean Python project structure. The key prompt pattern I used:

> "I want to build a FastAPI backend that tracks job applications and uses GPT-4o to score resume-job matches. It needs a Supabase backend. Propose a module structure and explain the separation of concerns."

AI suggested separating:
- `models.py` for Pydantic schemas
- `db.py` for all database logic
- `scorer.py` for all LLM interaction
- `main.py` for routing only

I accepted this structure because it makes testing easy and keeps each file focused. I did not accept a more complex suggestion involving a separate `services/` layer since the app scope did not warrant it.

### 2. Data Modeling

I described the domain to the AI and asked it to propose Pydantic models. Key decision points I made myself:
- Chose `ApplicationStatus` as a string enum so values are human-readable in the database
- Added a `score_breakdown` JSON field concept (documented in README) for future extensibility
- Kept `ScoreResult` as a separate model from `JobApplication` to keep the API clean

### 3. Scoring Prompt Engineering

This was the most iterative part. I worked with GPT-4o to design the system prompt for the scorer. I tested several prompt versions and evaluated outputs on real job descriptions before settling on the final version in `scorer.py`.

Key decisions:
- Used `response_format={"type": "json_object"}` to get stable structured output
- Set `temperature=0.2` to reduce randomness in scoring
- Asked the model to be "specific and honest" and explicitly told it not to inflate scores — this improved accuracy noticeably in testing
- Added a mock version (`score_resume_match_mock`) so the project can be demoed without an OpenAI key

### 4. Database Layer

I used AI to draft the initial Supabase client helpers, then hand-edited them to:
- Use environment variable validation with clear error messages
- Add consistent `updated_at` timestamps on every mutation
- Return `None` instead of raising on missing records, so the API layer controls the 404 logic

### 5. API Design

I used AI to brainstorm the API surface (which endpoints, what status codes, what request/response shapes). I then made these decisions myself:
- `POST /applications/{id}/score` takes both resume and job description in the body so it works even if the stored job description is stale
- Scoring still saves results to the DB but does not fail if the DB is unavailable — score is always returned
- Used `status_code=204` with `return None` for DELETE, which is the correct REST convention

### 6. Error Handling

AI generated initial try/except blocks. I rewrote them to:
- Distinguish between `EnvironmentError` (missing config) and `ValueError` (bad LLM output) and `Exception` (unexpected failures)
- Return appropriate HTTP status codes for each (503, 422, 500)
- Never expose internal error details in production-facing messages

### 7. Testing and Iteration

I used AI to generate the `sample_data/jobs.csv` test cases covering the full status pipeline: saved, applied, phone screen, interview, offer, rejected. This let me verify the status enum and CSV import path worked end-to-end.

## What This Demonstrates

| What I used AI for | What I decided myself |
|---|---|
| Module structure proposal | Final architecture (simplified it) |
| Pydantic model drafts | Field names, types, enum values |
| Scoring system prompt drafts | Final prompt, temperature, response format |
| DB helper boilerplate | Error handling strategy, return conventions |
| API endpoint brainstorm | Status codes, request shapes, edge cases |
| Test data generation | What edge cases actually matter |

The pattern throughout: AI generates options and drafts, I evaluate, decide, and refine. This is exactly how I would operate inside an AI-forward engineering team — fast iterations with AI, human judgment on correctness and product fit.
