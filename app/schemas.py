from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum

class JobCreate(BaseModel):
    title: str
    description: str
    location: str

class JobResponse(JobCreate):
    id: int
    isActive: bool

    class Config:
        orm_mode = True

class CandidateCreate(BaseModel):
    name: str
    email: EmailStr
    resumeLink: str

class CandidateResponse(CandidateCreate):
    id: int

    class Config:
        orm_mode = True

class ApplicationCreate(BaseModel):
    jobID: int
    candidateID: int

class ApplicationStatus(str, Enum):
    APPLIED = "APPLIED"
    SHORTLISTED = "SHORTLISTED"
    REJECTED = "REJECTED"
    SELECTED = "SELECTED"

class ApplicationResponse(BaseModel):
    id: int
    status: ApplicationStatus
    appliedAt: datetime

    class Config:
        orm_mode = True