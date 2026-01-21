from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base


class ApplicationStatus(str, enum.Enum):
    APPLIED = "APPLIED"
    SHORTLISTED = "SHORTLISTED"
    REJECTED = "REJECTED"
    SELECTED = "SELECTED"


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    location = Column(String, nullable=False)
    isActive = Column(Boolean, default=True)

    applications = relationship("Application", back_populates="job")


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    resumeLink = Column(String, nullable=False)

    applications = relationship("Application", back_populates="candidate")


class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (
        UniqueConstraint("job_id", "candidate_id", name="unique_application"),
    )

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.APPLIED)
    applied_at = Column(DateTime, default=datetime.utcnow)

    job = relationship("Job", back_populates="applications")
    candidate = relationship("Candidate", back_populates="applications")
