from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from .. import database, models, auth

router = APIRouter(prefix="/api/placements", tags=["placements"])

class PlacementCreate(BaseModel):
    application_id: int
    ctc_offered: float

@router.post("/")
def create_placement(placement: PlacementCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.require_role(models.RoleEnum.RECRUITER))):
    app = db.query(models.Application).filter(models.Application.id == placement.application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    recruiter = db.query(models.Recruiter).filter(models.Recruiter.user_id == current_user.id).first()
    if app.drive.company_id != recruiter.company_id:
        raise HTTPException(status_code=403, detail="Not authorized to make an offer for this application")

    existing_placement = db.query(models.Placement).filter(models.Placement.application_id == placement.application_id).first()
    if existing_placement:
        raise HTTPException(status_code=400, detail="Offer already exists for this application")

    new_placement = models.Placement(
        student_id=app.student_id,
        application_id=placement.application_id,
        ctc_offered=placement.ctc_offered
    )
    db.add(new_placement)
    
    # Also update application status
    app.status = models.ApplicationStatus.OFFERED
    
    db.commit()
    db.refresh(new_placement)
    return new_placement

@router.get("/student")
def get_student_placements(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.require_role(models.RoleEnum.STUDENT))):
    student = db.query(models.Student).filter(models.Student.user_id == current_user.id).first()
    placements = db.query(models.Placement).filter(models.Placement.student_id == student.id).all()
    
    return [
        {
            "id": p.id,
            "company": p.application.drive.company.name,
            "job_title": p.application.drive.job_title,
            "ctc_offered": p.ctc_offered,
            "offer_date": p.offer_date
        } for p in placements
    ]

@router.get("/admin")
def get_all_placements(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.require_role(models.RoleEnum.ADMIN))):
    placements = db.query(models.Placement).all()
    return [
        {
            "id": p.id,
            "student_name": p.student.user.full_name,
            "roll_number": p.student.roll_number,
            "branch": p.student.branch,
            "company": p.application.drive.company.name,
            "job_title": p.application.drive.job_title,
            "ctc_offered": p.ctc_offered,
            "offer_date": p.offer_date
        } for p in placements
    ]
