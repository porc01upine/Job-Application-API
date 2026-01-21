from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from . import schemas, crud

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Job Application API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/jobs/", response_model=schemas.JobResponse)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    return crud.create_job(db, job)

@app.post("/candidates/", response_model=schemas.CandidateResponse)
def create_candidate(candidate: schemas.CandidateCreate, db: Session = Depends(get_db)):
    return crud.create_candidate(db, candidate)

@app.post("/applications/", response_model=schemas.ApplicationResponse)
def apply_for_job(application: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    return crud.apply_for_job(db, application.jobID, application.candidateID)

@app.patch("/applications/{app_id}/status/", response_model=schemas.ApplicationResponse)
def update_application_status(app_id: int, status: schemas.ApplicationStatus, db: Session = Depends(get_db)):
    return crud.update_application_status(db, app_id, status.value)

@app.get("/")
def root():
    return {"message": "Job Application API is running"}