from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import models

def create_job(db: Session, job):
    db_job = models.Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def create_candidate(db: Session, candidate):

    existing_candidate = db.query(models.Candidate).filter_by(email=candidate.email).first()
    if existing_candidate:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_candidate = models.Candidate(**candidate.dict())
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

def apply_for_job(db: Session, job_id: int, candidate_id: int):

    job=db.query(models.Job).filter_by(id=job_id).first()
    if not job or not job.isActive:
        raise HTTPException(status_code=404, detail="Job not found or inactive")
    
    candidate=db.query(models.Candidate).filter_by(id=candidate_id).first()
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    existing_application = db.query(models.Application).filter_by(job_id=job_id, candidate_id=candidate_id).first()
    if existing_application:
        raise HTTPException(status_code=400, detail="Application already exists for this job and candidate")

    application = models.Application(job_id=job_id, candidate_id=candidate_id)

    db.add(application)
    db.commit()
    db.refresh(application)
    return application


def update_application_status(db:Session, app_id:int,status):

    application=db.query(models.Application).filter_by(id=app_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    allowed={
        "APPLIED":["SHORTLISTED","REJECTED"],
        "SHORTLISTED":["REJECTED","SELECTED"],
    }

    current=application.status.value
    if current in allowed and status not in allowed[current]:
        raise HTTPException(status_code=400, detail=f"Invalid status transition from {current} to {status}")
    
    application.status=status
    db.commit()
    db.refresh(application)
    return application