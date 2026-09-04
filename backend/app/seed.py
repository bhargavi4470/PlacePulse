from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random

from .database import SessionLocal, engine
from . import models, auth

models.Base.metadata.create_all(bind=engine)

def seed_db():
    db = SessionLocal()
    try:
        # 1. Create Skills
        skills = ["Java", "Python", "React", "Angular", "Spring Boot", "SQL", "C++", "Data Structures", "System Design"]
        skill_objs = {}
        for skill_name in skills:
            if not db.query(models.Skill).filter_by(name=skill_name).first():
                s = models.Skill(name=skill_name)
                db.add(s)
                db.commit()
                db.refresh(s)
                skill_objs[skill_name] = s
            else:
                skill_objs[skill_name] = db.query(models.Skill).filter_by(name=skill_name).first()

        # 2. Create Admin
        if not db.query(models.User).filter_by(email="admin@college.edu").first():
            admin = models.User(
                email="admin@college.edu",
                hashed_password=auth.get_password_hash("admin123"),
                full_name="Dr. Aris Thorne",
                role=models.RoleEnum.ADMIN
            )
            db.add(admin)
            db.commit()

        # 3. Create Companies and Recruiters
        companies_data = [
            {"name": "Microsoft", "description": "Tech giant", "website": "microsoft.com"},
            {"name": "Amazon", "description": "E-commerce and cloud computing", "website": "amazon.com"},
            {"name": "TCS", "description": "IT services", "website": "tcs.com"},
            {"name": "Zscaler", "description": "Cloud security", "website": "zscaler.com"}
        ]
        company_objs = {}
        for c in companies_data:
            comp = db.query(models.Company).filter_by(name=c["name"]).first()
            if not comp:
                comp = models.Company(**c)
                db.add(comp)
                db.commit()
                db.refresh(comp)
            company_objs[c["name"]] = comp

            recruiter_email = f"recruiter@{c['name'].lower()}.com"
            if not db.query(models.User).filter_by(email=recruiter_email).first():
                r_user = models.User(
                    email=recruiter_email,
                    hashed_password=auth.get_password_hash("recruiter123"),
                    full_name=f"Recruiter {c['name']}",
                    role=models.RoleEnum.RECRUITER
                )
                db.add(r_user)
                db.commit()
                db.refresh(r_user)
                
                r_profile = models.Recruiter(
                    user_id=r_user.id,
                    company_id=comp.id,
                    designation="Talent Acquisition"
                )
                db.add(r_profile)
                db.commit()

        # 4. Create Placement Drives
        drives_data = [
            {
                "job_title": "Software Development Engineer - 1",
                "company_id": company_objs["Microsoft"].id,
                "ctc": 44.0,
                "location": "Bengaluru / Hyderabad",
                "registration_deadline": datetime.utcnow() + timedelta(days=5),
                "min_cgpa": 8.0,
                "max_active_backlogs": 0,
                "max_historical_backlogs": 1,
                "allowed_branches": "CSE,IT",
                "status": "PUBLISHED"
            },
            {
                "job_title": "Systems Engineer",
                "company_id": company_objs["TCS"].id,
                "ctc": 9.0,
                "location": "Pan India",
                "registration_deadline": datetime.utcnow() + timedelta(days=10),
                "min_cgpa": 6.5,
                "max_active_backlogs": 1,
                "max_historical_backlogs": 2,
                "allowed_branches": "CSE,IT,ECE,MECH",
                "status": "PUBLISHED"
            },
            {
                "job_title": "Cloud Solutions Engineer",
                "company_id": company_objs["Zscaler"].id,
                "ctc": 18.5,
                "location": "Pune",
                "registration_deadline": datetime.utcnow() - timedelta(days=1), # Expired drive
                "min_cgpa": 7.5,
                "max_active_backlogs": 0,
                "max_historical_backlogs": 0,
                "allowed_branches": "CSE,IT",
                "status": "COMPLETED"
            }
        ]
        
        drive_objs = []
        for d in drives_data:
            drive = db.query(models.PlacementDrive).filter_by(job_title=d["job_title"], company_id=d["company_id"]).first()
            if not drive:
                drive = models.PlacementDrive(**d)
                db.add(drive)
                db.commit()
                db.refresh(drive)
                
                if d["job_title"] == "Software Development Engineer - 1":
                    drive.required_skills.extend([skill_objs["Java"], skill_objs["Data Structures"]])
                db.commit()
            drive_objs.append(drive)

        # 5. Create Students with Edge Cases
        students_data = [
            {"name": "Rahul Sharma", "roll": "21CSE1084", "branch": "CSE", "cgpa": 8.84, "act_b": 0, "hist_b": 0, "skills": ["Java", "Spring Boot", "React", "Data Structures"], "desc": "fully eligible student"},
            {"name": "Priya Nair", "roll": "21CSE1042", "branch": "CSE", "cgpa": 7.92, "act_b": 0, "hist_b": 0, "skills": ["Java", "Data Structures"], "desc": "student below CGPA cutoff"},
            {"name": "Devansh Verma", "roll": "21IT2818", "branch": "IT", "cgpa": 8.00, "act_b": 0, "hist_b": 0, "skills": ["C++", "System Design"], "desc": "exactly at CGPA cutoff"},
            {"name": "Ananya Sundaram", "roll": "21AI0432", "branch": "AI", "cgpa": 8.41, "act_b": 0, "hist_b": 0, "skills": ["Python"], "desc": "wrong branch (AI not in CSE,IT)"},
            {"name": "Rohan Kulkarni", "roll": "21ECE0891", "branch": "ECE", "cgpa": 8.12, "act_b": 1, "hist_b": 2, "skills": ["SQL"], "desc": "active backlog and wrong branch (multiple failed rules)"},
            {"name": "Sneha Mukherjee", "roll": "21ECE045", "branch": "ECE", "cgpa": 9.45, "act_b": 0, "hist_b": 1, "skills": ["Java", "Data Structures"], "desc": "historical backlog (allowed for Microsoft)"},
            {"name": "Aditya Verma", "roll": "21CSE094", "branch": "CSE", "cgpa": 9.12, "act_b": 0, "hist_b": 0, "skills": ["Python", "SQL"], "desc": "missing required skill (Java for MSFT)"},
            {"name": "Tarun Tejashwi", "roll": "21CSE142", "branch": "CSE", "cgpa": 8.65, "act_b": 0, "hist_b": 0, "skills": ["Java", "React"], "desc": "student with existing offer (we will add placement)"},
        ]

        student_objs = []
        for s in students_data:
            email = f"{s['roll'].lower()}@college.edu"
            u = db.query(models.User).filter_by(email=email).first()
            if not u:
                u = models.User(
                    email=email,
                    hashed_password=auth.get_password_hash("student123"),
                    full_name=s["name"],
                    role=models.RoleEnum.STUDENT
                )
                db.add(u)
                db.commit()
                db.refresh(u)
                
                sp = models.Student(
                    user_id=u.id,
                    roll_number=s["roll"],
                    branch=s["branch"],
                    graduation_year=2025,
                    cgpa=s["cgpa"],
                    active_backlogs=s["act_b"],
                    historical_backlogs=s["hist_b"],
                    tenth_percentage=85.0,
                    twelfth_percentage=88.0,
                    profile_readiness=92
                )
                db.add(sp)
                db.commit()
                db.refresh(sp)
                
                # Add skills
                for sk in s["skills"]:
                    if sk in skill_objs:
                        sp.skills.append(skill_objs[sk])
                db.commit()
            else:
                sp = db.query(models.Student).filter_by(roll_number=s["roll"]).first()
            student_objs.append(sp)

        # 6. Create Applications & Placements (to simulate student with existing offer)
        msft_drive = db.query(models.PlacementDrive).filter_by(job_title="Software Development Engineer - 1").first()
        tcs_drive = db.query(models.PlacementDrive).filter_by(job_title="Systems Engineer").first()
        zscaler_drive = db.query(models.PlacementDrive).filter_by(job_title="Cloud Solutions Engineer").first()

        tarun = db.query(models.Student).filter_by(roll_number="21CSE142").first()
        
        # Tarun placed in Zscaler
        if tarun and zscaler_drive:
            app = db.query(models.Application).filter_by(student_id=tarun.id, drive_id=zscaler_drive.id).first()
            if not app:
                app = models.Application(
                    student_id=tarun.id,
                    drive_id=zscaler_drive.id,
                    status=models.ApplicationStatus.SELECTED
                )
                db.add(app)
                db.commit()
                db.refresh(app)
                
                place = models.Placement(
                    student_id=tarun.id,
                    application_id=app.id,
                    ctc_offered=18.5
                )
                db.add(place)
                db.commit()

        # Add Rahul applying to Microsoft
        rahul = db.query(models.Student).filter_by(roll_number="21CSE1084").first()
        if rahul and msft_drive:
            app2 = db.query(models.Application).filter_by(student_id=rahul.id, drive_id=msft_drive.id).first()
            if not app2:
                app2 = models.Application(
                    student_id=rahul.id,
                    drive_id=msft_drive.id,
                    status=models.ApplicationStatus.TECHNICAL
                )
                db.add(app2)
                db.commit()
                db.refresh(app2)
                
                # Interview schedule for Rahul
                msft_recruiter = db.query(models.Recruiter).filter_by(company_id=msft_drive.company_id).first()
                intv = models.Interview(
                    application_id=app2.id,
                    round_name="Technical Round 1",
                    scheduled_time=datetime.utcnow() + timedelta(days=1),
                    interviewer_id=msft_recruiter.id if msft_recruiter else None
                )
                db.add(intv)
                db.commit()

        print("Seed data successfully added!")

    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
