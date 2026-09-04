from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import database, models, auth
from typing import List, Dict, Any

router = APIRouter(prefix="/api/admin", tags=["admin"])

def require_admin(current_user: models.User = Depends(auth.require_role(models.RoleEnum.ADMIN))):
    return current_user

@router.get("/analytics")
def get_admin_analytics(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.require_role(models.RoleEnum.ADMIN))):
    total_students = db.query(models.Student).count()
    placed_students = db.query(models.Placement).count()
    total_companies = db.query(models.Company).count()
    total_drives = db.query(models.PlacementDrive).count()
    
    # Placements by branch
    placements = db.query(models.Placement).all()
    branch_stats = {}
    for p in placements:
        branch = p.student.branch
        if branch not in branch_stats:
            branch_stats[branch] = 0
        branch_stats[branch] += 1
        
    return {
        "overview": {
            "total_students": total_students,
            "placed_students": placed_students,
            "unplaced_students": total_students - placed_students,
            "total_companies": total_companies,
            "total_drives": total_drives,
            "placement_rate": round((placed_students / total_students * 100) if total_students > 0 else 0, 1)
        },
        "branch_stats": [
            {"branch": branch, "placed": count} for branch, count in branch_stats.items()
        ]
    }

@router.get("/eligibility/evaluate/{student_id}/{drive_id}")
def evaluate_eligibility(student_id: int, drive_id: int, db: Session = Depends(database.get_db), admin: models.User = Depends(require_admin)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    drive = db.query(models.PlacementDrive).filter(models.PlacementDrive.id == drive_id).first()
    
    if not student or not drive:
        raise HTTPException(status_code=404, detail="Student or Drive not found")

    rules_passed = []
    rules_failed = []
    
    # Check CGPA
    if student.cgpa >= drive.min_cgpa:
        rules_passed.append({"rule": "Minimum CGPA", "required": drive.min_cgpa, "actual": student.cgpa})
    else:
        rules_failed.append({"rule": "Minimum CGPA", "required": drive.min_cgpa, "actual": student.cgpa, "explanation": "CGPA is below cutoff"})

    # Check Active Backlogs
    if student.active_backlogs <= drive.max_active_backlogs:
        rules_passed.append({"rule": "Max Active Backlogs", "required": drive.max_active_backlogs, "actual": student.active_backlogs})
    else:
        rules_failed.append({"rule": "Max Active Backlogs", "required": drive.max_active_backlogs, "actual": student.active_backlogs, "explanation": "Too many active backlogs"})

    # Check Historical Backlogs
    if student.historical_backlogs <= drive.max_historical_backlogs:
        rules_passed.append({"rule": "Max Historical Backlogs", "required": drive.max_historical_backlogs, "actual": student.historical_backlogs})
    else:
        rules_failed.append({"rule": "Max Historical Backlogs", "required": drive.max_historical_backlogs, "actual": student.historical_backlogs, "explanation": "Exceeded allowed historical backlogs"})

    # Check Branch
    if drive.allowed_branches:
        branches = [b.strip() for b in drive.allowed_branches.split(',')]
        if student.branch in branches:
            rules_passed.append({"rule": "Allowed Branches", "required": drive.allowed_branches, "actual": student.branch})
        else:
            rules_failed.append({"rule": "Allowed Branches", "required": drive.allowed_branches, "actual": student.branch, "explanation": "Branch not eligible"})

    # Check Skills
    drive_skills = set([s.name for s in drive.required_skills])
    student_skills = set([s.name for s in student.skills])
    missing_skills = drive_skills - student_skills
    if not missing_skills:
        if drive_skills:
            rules_passed.append({"rule": "Required Skills", "required": ", ".join(drive_skills), "actual": ", ".join(student_skills)})
    else:
        rules_failed.append({"rule": "Required Skills", "required": ", ".join(drive_skills), "actual": ", ".join(student_skills), "explanation": f"Missing skills: {', '.join(missing_skills)}"})

    # Check Existing Offers (Example logic: If they have an offer, they can't apply unless it's a dream company - simple version here)
    if student.placements:
        rules_failed.append({"rule": "No Existing Offer", "required": "Unplaced", "actual": "Placed", "explanation": "Student already holds an offer"})

    # Verdict
    if len(rules_failed) == 0:
        verdict = "ELIGIBLE"
    elif len(rules_failed) == 1 and rules_failed[0]["rule"] == "No Existing Offer":
        verdict = "CONDITIONAL" # Can be reviewed by TPO
    else:
        verdict = "INELIGIBLE"

    return {
        "student_id": student.id,
        "student_name": student.user.full_name,
        "roll_number": student.roll_number,
        "drive_id": drive.id,
        "drive_name": drive.job_title,
        "verdict": verdict,
        "rules_passed": rules_passed,
        "rules_failed": rules_failed
    }

@router.get("/students")
def get_all_students(db: Session = Depends(database.get_db), admin: models.User = Depends(require_admin)):
    students = db.query(models.Student).all()
    return [{"id": s.id, "name": s.user.full_name, "roll_number": s.roll_number, "branch": s.branch, "cgpa": s.cgpa} for s in students]

@router.get("/drives")
def get_all_drives(db: Session = Depends(database.get_db), admin: models.User = Depends(require_admin)):
    drives = db.query(models.PlacementDrive).all()
    return [{"id": d.id, "title": d.job_title, "company": d.company.name, "status": d.status} for d in drives]
