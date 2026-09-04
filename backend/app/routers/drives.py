from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, auth, database
from datetime import datetime

router = APIRouter(prefix="/api/drives", tags=["drives"])

@router.get("/", response_model=List[schemas.PlacementDrive])
def get_active_drives(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.require_role(models.RoleEnum.STUDENT))):
    now = datetime.utcnow()
    drives = db.query(models.PlacementDrive).filter(
        models.PlacementDrive.status == "PUBLISHED",
        models.PlacementDrive.registration_deadline > now
    ).all()
    return drives

@router.post("/{drive_id}/apply", response_model=schemas.Application)
def apply_for_drive(drive_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.require_role(models.RoleEnum.STUDENT))):
    student = db.query(models.Student).filter(models.Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")

    drive = db.query(models.PlacementDrive).filter(models.PlacementDrive.id == drive_id).first()
    if not drive or drive.status != "PUBLISHED":
        raise HTTPException(status_code=404, detail="Drive not found or not active")

    # Check if already applied
    existing_app = db.query(models.Application).filter(
        models.Application.student_id == student.id,
        models.Application.drive_id == drive_id
    ).first()
    if existing_app:
        raise HTTPException(status_code=400, detail="Already applied to this drive")

    app = models.Application(
        student_id=student.id,
        drive_id=drive_id,
        status=models.ApplicationStatus.APPLIED
    )
    db.add(app)
    db.commit()
    db.refresh(app)
    return app
