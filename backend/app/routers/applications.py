from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from typing import List, Dict, Any
from .. import database, models, auth, schemas
from pydantic import BaseModel

router = APIRouter(prefix="/api/applications", tags=["applications"])

class ApplicationStatusUpdate(BaseModel):
    status: models.ApplicationStatus

@router.get("/student")
def get_student_applications(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.require_role(models.RoleEnum.STUDENT))):
    student = db.query(models.Student).filter(models.Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    apps = db.query(models.Application).filter(models.Application.student_id == student.id).all()
    
    return [
        {
            "id": app.id,
            "drive_id": app.drive.id,
            "job_title": app.drive.job_title,
            "company": app.drive.company.name,
            "status": app.status,
            "applied_at": app.applied_at
        } for app in apps
    ]

@router.get("/recruiter")
def get_recruiter_applications(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.require_role(models.RoleEnum.RECRUITER))):
    recruiter = db.query(models.Recruiter).filter(models.Recruiter.user_id == current_user.id).first()
    if not recruiter:
        raise HTTPException(status_code=404, detail="Recruiter not found")

    # Get all drives for this company
    drives = db.query(models.PlacementDrive).filter(models.PlacementDrive.company_id == recruiter.company_id).all()
    drive_ids = [d.id for d in drives]

    # Get all applications for these drives
    apps = db.query(models.Application).filter(models.Application.drive_id.in_(drive_ids)).all()

    return [
        {
            "id": app.id,
            "student_id": app.student.id,
            "student_name": app.student.user.full_name,
            "roll_number": app.student.roll_number,
            "cgpa": app.student.cgpa,
            "branch": app.student.branch,
            "resume_url": app.student.resume_url,
            "drive_id": app.drive.id,
            "job_title": app.drive.job_title,
            "status": app.status,
            "applied_at": app.applied_at
        } for app in apps
    ]

@router.put("/{app_id}/status")
def update_application_status(app_id: int, status_update: ApplicationStatusUpdate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.require_role(models.RoleEnum.RECRUITER))):
    recruiter = db.query(models.Recruiter).filter(models.Recruiter.user_id == current_user.id).first()
    
    app = db.query(models.Application).filter(models.Application.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
        
    # Verify the recruiter's company owns this drive
    if app.drive.company_id != recruiter.company_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this application")

    app.status = status_update.status
    db.commit()
    return {"message": "Status updated successfully", "status": app.status}
