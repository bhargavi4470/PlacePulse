from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import database, models, auth, schemas
from typing import List

router = APIRouter(prefix="/api/recruiter", tags=["recruiter"])

def get_current_recruiter(current_user: models.User = Depends(auth.require_role(models.RoleEnum.RECRUITER)), db: Session = Depends(database.get_db)):
    recruiter = db.query(models.Recruiter).filter(models.Recruiter.user_id == current_user.id).first()
    if not recruiter:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recruiter profile not found")
    return recruiter

@router.get("/drives", response_model=List[schemas.PlacementDrive])
def get_recruiter_drives(recruiter: models.Recruiter = Depends(get_current_recruiter), db: Session = Depends(database.get_db)):
    drives = db.query(models.PlacementDrive).filter(models.PlacementDrive.company_id == recruiter.company_id).all()
    return drives

@router.post("/drives", response_model=schemas.PlacementDrive)
def create_drive(drive_in: schemas.PlacementDriveBase, recruiter: models.Recruiter = Depends(get_current_recruiter), db: Session = Depends(database.get_db)):
    # We use PlacementDriveBase, and manually set company_id to the recruiter's company
    new_drive = models.PlacementDrive(
        company_id=recruiter.company_id,
        status="DRAFT", # Default to draft until published
        **drive_in.model_dump()
    )
    db.add(new_drive)
    db.commit()
    db.refresh(new_drive)
    return new_drive
