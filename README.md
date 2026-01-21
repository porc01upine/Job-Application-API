project:
  name: Job Application Management API
  description: A backend REST API built using FastAPI to manage job applications for a single company and job opening.

tech_stack:
  - Python 3.9+
  - FastAPI
  - SQLAlchemy
  - SQLite
  - Pydantic
  - Uvicorn

project_structure:
  - job_api/
    - app/
      - __init__.py
      - main.py
      - database.py
      - models.py
      - schemas.py
      - crud.py
    - venv/
    - jobs.db
    - README.md
    - .gitignore

setup_steps:
  - clone_repository: "git clone https://github.com/<your-username>/job-application-api.git"
  - navigate: "cd job_api"
  - create_virtualenv_windows: "python -m venv venv && venv\\Scripts\\Activate.ps1"
  - create_virtualenv_unix: "python3 -m venv venv && source venv/bin/activate"
  - install_dependencies: "pip install fastapi uvicorn sqlalchemy pydantic email-validator"
  - run_server: "uvicorn app.main:app --reload"
  - swagger_ui: "http://127.0.0.1:8000/docs"

database:
  engine: SQLite
  file: jobs.db
  tables:
    - jobs
    - candidates
    - applications
  note: "Automatically created on server start"

api:
  jobs:
    create_job:
      method: POST
      endpoint: /jobs
      request_body:
        title: string
        description: string
        location: string
      response_example:
        id: 1
        title: Backend Developer
        description: FastAPI backend role
        location: Remote
        isActive: true

  candidates:
    create_candidate:
      method: POST
      endpoint: /candidates
      request_body:
        name: string
        email: string
        resumeLink: string
      response_example:
        id: 1
        name: John Doe
        email: john@example.com
        resumeLink: https://example.com/resume.pdf

  applications:
    apply_for_job:
      method: POST
      endpoint: /applications
      request_body:
        jobId: 1
        candidateId: 1
      response_example:
        id: 1
        jobId: 1
        candidateId: 1
        status: APPLIED
        appliedAt: 2026-01-22T14:00:00

    update_status:
      method: PATCH
      endpoint: /applications/{application_id}/status
      query_params:
        status:
          allowed_values:
            - APPLIED
            - SHORTLISTED
            - REJECTED
            - SELECTED
      response_example:
        id: 1
        jobId: 1
        candidateId: 1
        status: SHORTLISTED
        appliedAt: 2026-01-22T14:00:00

business_rules:
  - A candidate can apply only once per job.
  - Job must be active to accept applications.
  - Valid status transitions:
      - APPLIED → SHORTLISTED → SELECTED
      - APPLIED → REJECTED
      - SHORTLISTED → REJECTED

error_handling:
  400: Invalid request or business rule violation
  404: Resource not found
  422: Validation error (handled by FastAPI)

testing:
  methods:
    - Swagger UI at /docs
    - Postman
    - curl

author:
  name: Swapnil Kumar

notes:
  - Project demonstrates REST API design, validation, database modeling, and clean backend architecture using FastAPI.
  - SQLite used for simplicity; can be migrated to PostgreSQL for production.
