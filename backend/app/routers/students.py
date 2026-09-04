from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from typing import List, Dict, Any
from .. import models, schemas, auth, database
from datetime import datetime

router = APIRouter(prefix="/api/students", tags=["students"])

def get_current_student(current_user: models.User = Depends(auth.require_role(models.RoleEnum.STUDENT)), db: Session = Depends(database.get_db)):
    student = db.query(models.Student).filter(models.Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student profile not found")
    return student

@router.get("/me/dashboard")
def get_student_dashboard(student: models.Student = Depends(get_current_student), db: Session = Depends(database.get_db)):
    now = datetime.utcnow()

    # 1. Pipeline count: Applications that are active (Not Rejected/Selected yet, or maybe Selected is counted)
    active_apps_query = db.query(models.Application).filter(
        models.Application.student_id == student.id,
        models.Application.status.notin_([models.ApplicationStatus.REJECTED, models.ApplicationStatus.SELECTED])
    )
    active_pipeline_count = active_apps_query.count()

    # 2. Offers count
    offers_count = db.query(models.Placement).filter(models.Placement.student_id == student.id).count()

    # 3. Simple Eligibility count (Full rules engine will be in Phase 5, but we do basic DB filtering here)
    # Get all published drives where deadline > now
    active_drives = db.query(models.PlacementDrive).filter(
        models.PlacementDrive.status == "PUBLISHED",
        models.PlacementDrive.registration_deadline > now
    ).all()

    eligible_count = 0
    for drive in active_drives:
        # Basic check
        if student.cgpa >= drive.min_cgpa and student.active_backlogs <= drive.max_active_backlogs:
            if not drive.allowed_branches or student.branch in drive.allowed_branches:
                eligible_count += 1

    return {
        "profile": {
            "full_name": student.user.full_name,
            "roll_number": student.roll_number,
            "branch": student.branch,
            "graduation_year": student.graduation_year,
            "cgpa": student.cgpa,
            "active_backlogs": student.active_backlogs,
            "profile_readiness": student.profile_readiness
        },
        "metrics": {
            "eligible_drives_count": eligible_count,
            "active_pipeline_count": active_pipeline_count,
            "offers_count": offers_count
        }
    }

@router.get("/me", response_model=schemas.Student)
def get_my_profile(student: models.Student = Depends(get_current_student)):
    return student

@router.put("/me", response_model=schemas.Student)
def update_my_profile(profile_update: schemas.StudentBase, student: models.Student = Depends(get_current_student), db: Session = Depends(database.get_db)):
    for key, value in profile_update.model_dump().items():
        setattr(student, key, value)
    
    # Calculate profile readiness (simple logic)
    score = 50 # Base score
    if student.github_username: score += 10
    if student.tenth_percentage: score += 10
    if student.twelfth_percentage: score += 10
    if student.resume_url: score += 20
    student.profile_readiness = score

    db.commit()
    db.refresh(student)
    return student
