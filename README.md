# AI Job Tracker

An AI-powered job application tracker that scores how well your resume matches each job description, tracks application status, and stores everything in a Supabase database. Built with Python and FastAPI.

## Features

- Log job applications with company, role, URL, and status
- AI-powered resume-to-job match scoring using OpenAI
- Track status pipeline: Applied, Phone Screen, Interview, Offer, Rejected
- Deadline and follow-up reminders
- Supabase (PostgreSQL) backend
- REST API with FastAPI
- Sample data included to run without a database

## Tech Stack

- Python 3.11+
- FastAPI
- Supabase (PostgreSQL)
- OpenAI API (GPT-4o)
- Pydantic
- Uvicorn

## Project Structure

```
ai-job-tracker/
├── main.py              # FastAPI app and API routes
├── scorer.py            # Resume-to-job match scoring logic
├── db.py                # Supabase client and database helpers
├── models.py            # Pydantic data models
├── requirements.txt     # Dependencies
├── .env.example         # Environment variable template
├── CLAUDE.md            # AI build log
└── sample_data/
    └── jobs.csv         # Sample job applications
```

## How to Run Locally

1. Clone the repo:

```bash
git clone https://github.com/Sergo123-eng/ai-job-tracker.git
cd ai-job-tracker
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables (copy `.env.example` to `.env`):

```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
OPENAI_API_KEY=your_openai_api_key
```

5. Run the API server:

```bash
uvicorn main:app --reload
```

6. Open the interactive API docs at:

```
http://localhost:8000/docs
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/applications` | List all job applications |
| POST | `/applications` | Add a new job application |
| GET | `/applications/{id}` | Get a single application |
| PUT | `/applications/{id}/status` | Update application status |
| POST | `/applications/{id}/score` | Score resume match for a job |
| DELETE | `/applications/{id}` | Delete an application |

## Match Scoring

The `/score` endpoint sends your resume and the job description to GPT-4o and returns:
- A match score from 0 to 100
- A short explanation of strengths
- A list of skill gaps to address

## Sample Data

See `sample_data/jobs.csv` for example applications you can import and test with.

## CLAUDE.md

See `CLAUDE.md` for a full log of how AI tools were used to design and build this project.
