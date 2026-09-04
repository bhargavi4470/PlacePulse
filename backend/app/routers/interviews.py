from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime
from .. import database, models, auth

router = APIRouter(prefix="/api/interviews", tags=["interviews"])

class InterviewCreate(BaseModel):
    application_id: int
    round_name: str
    scheduled_time: datetime
    meeting_link: str = None
    interviewer_id: int = None

class InterviewUpdate(BaseModel):
    scheduled_time: datetime = None
    meeting_link: str = None
    feedback: str = None
    rating: float = None
    verdict: models.InterviewVerdict = None

@router.post("/")
def schedule_interview(interview: InterviewCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.require_role(models.RoleEnum.RECRUITER))):
    app = db.query(models.Application).filter(models.Application.id == interview.application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
        
    recruiter = db.query(models.Recruiter).filter(models.Recruiter.user_id == current_user.id).first()
    if app.drive.company_id != recruiter.company_id:
        raise HTTPException(status_code=403, detail="Not authorized to schedule interview for this application")

    new_interview = models.Interview(
        application_id=interview.application_id,
        round_name=interview.round_name,
        scheduled_time=interview.scheduled_time,
        meeting_link=interview.meeting_link,
        interviewer_id=interview.interviewer_id
    )
    db.add(new_interview)
    db.commit()
    db.refresh(new_interview)
    return new_interview

@router.put("/{interview_id}")
def update_interview(interview_id: int, updates: InterviewUpdate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.require_role(models.RoleEnum.RECRUITER))):
    interview = db.query(models.Interview).filter(models.Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    recruiter = db.query(models.Recruiter).filter(models.Recruiter.user_id == current_user.id).first()
    if interview.application.drive.company_id != recruiter.company_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this interview")

    if updates.scheduled_time is not None:
        interview.scheduled_time = updates.scheduled_time
    if updates.meeting_link is not None:
        interview.meeting_link = updates.meeting_link
    if updates.feedback is not None:
        interview.feedback = updates.feedback
    if updates.rating is not None:
        interview.rating = updates.rating
    if updates.verdict is not None:
        interview.verdict = updates.verdict

    db.commit()
    db.refresh(interview)
    return interview

@router.get("/student")
def get_student_interviews(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.require_role(models.RoleEnum.STUDENT))):
    student = db.query(models.Student).filter(models.Student.user_id == current_user.id).first()
    interviews = db.query(models.Interview).join(models.Application).filter(models.Application.student_id == student.id).all()
    
    return [
        {
            "id": i.id,
            "round_name": i.round_name,
            "scheduled_time": i.scheduled_time,
            "meeting_link": i.meeting_link,
            "company": i.application.drive.company.name,
            "job_title": i.application.drive.job_title,
            "verdict": i.verdict
        } for i in interviews
    ]

@router.get("/recruiter")
def get_recruiter_interviews(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.require_role(models.RoleEnum.RECRUITER))):
    recruiter = db.query(models.Recruiter).filter(models.Recruiter.user_id == current_user.id).first()
    interviews = db.query(models.Interview).join(models.Application).join(models.PlacementDrive).filter(models.PlacementDrive.company_id == recruiter.company_id).all()
    
    return [
        {
            "id": i.id,
            "application_id": i.application_id,
            "student_name": i.application.student.user.full_name,
            "job_title": i.application.drive.job_title,
            "round_name": i.round_name,
            "scheduled_time": i.scheduled_time,
            "meeting_link": i.meeting_link,
            "feedback": i.feedback,
            "rating": i.rating,
            "verdict": i.verdict
        } for i in interviews
    ]
