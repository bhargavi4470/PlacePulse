from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Enum as SQLEnum, Text, Table
from sqlalchemy.orm import relationship
import enum
import datetime
from .database import Base

class RoleEnum(str, enum.Enum):
    STUDENT = "STUDENT"
    ADMIN = "ADMIN"
    RECRUITER = "RECRUITER"

class ApplicationStatus(str, enum.Enum):
    APPLIED = "APPLIED"
    SHORTLISTED = "SHORTLISTED"
    ASSESSMENT = "ASSESSMENT"
    TECHNICAL = "TECHNICAL"
    HR = "HR"
    SELECTED = "SELECTED"
    REJECTED = "REJECTED"

class InterviewVerdict(str, enum.Enum):
    PENDING = "PENDING"
    STRONG_HIRE = "STRONG_HIRE"
    HIRE = "HIRE"
    NO_HIRE = "NO_HIRE"

# Association Tables
student_skill_association = Table('student_skills', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id'), primary_key=True),
    Column('skill_id', Integer, ForeignKey('skills.id'), primary_key=True)
)

drive_skill_association = Table('drive_skills', Base.metadata,
    Column('drive_id', Integer, ForeignKey('placement_drives.id'), primary_key=True),
    Column('skill_id', Integer, ForeignKey('skills.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(SQLEnum(RoleEnum), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    student_profile = relationship("Student", back_populates="user", uselist=False)
    recruiter_profile = relationship("Recruiter", back_populates="user", uselist=False)
    notifications = relationship("Notification", back_populates="user")

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    roll_number = Column(String, unique=True, index=True, nullable=False)
    branch = Column(String, nullable=False)
    graduation_year = Column(Integer, nullable=False)
    cgpa = Column(Float, nullable=False, default=0.0)
    active_backlogs = Column(Integer, nullable=False, default=0)
    historical_backlogs = Column(Integer, nullable=False, default=0)
    tenth_percentage = Column(Float, nullable=True)
    twelfth_percentage = Column(Float, nullable=True)
    resume_url = Column(String, nullable=True)
    github_username = Column(String, nullable=True)
    profile_readiness = Column(Integer, default=0)

    # Relationships
    user = relationship("User", back_populates="student_profile")
    skills = relationship("Skill", secondary=student_skill_association, back_populates="students")
    applications = relationship("Application", back_populates="student")
    placements = relationship("Placement", back_populates="student")

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    website = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)

    recruiters = relationship("Recruiter", back_populates="company")
    drives = relationship("PlacementDrive", back_populates="company")

class Recruiter(Base):
    __tablename__ = "recruiters"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    designation = Column(String, nullable=True)

    user = relationship("User", back_populates="recruiter_profile")
    company = relationship("Company", back_populates="recruiters")

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    students = relationship("Student", secondary=student_skill_association, back_populates="skills")
    drives = relationship("PlacementDrive", secondary=drive_skill_association, back_populates="required_skills")

class PlacementDrive(Base):
    __tablename__ = "placement_drives"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    job_title = Column(String, nullable=False)
    job_description = Column(Text, nullable=True)
    ctc = Column(Float, nullable=False)  # In LPA
    location = Column(String, nullable=True)
    job_type = Column(String, nullable=True) # Full-time, Internship
    status = Column(String, default="DRAFT") # DRAFT, PUBLISHED, COMPLETED
    registration_deadline = Column(DateTime, nullable=False)
    
    # Eligibility Criteria embedded directly or in a separate table
    # Storing basic rules in this table for simpler queries, but complex ones can go to EligibilityRule
    min_cgpa = Column(Float, default=0.0)
    max_active_backlogs = Column(Integer, default=0)
    max_historical_backlogs = Column(Integer, default=0)
    allowed_branches = Column(String, nullable=True) # Comma separated branches like 'CSE,IT'
    min_tenth_percentage = Column(Float, default=0.0)
    min_twelfth_percentage = Column(Float, default=0.0)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    company = relationship("Company", back_populates="drives")
    required_skills = relationship("Skill", secondary=drive_skill_association, back_populates="drives")
    applications = relationship("Application", back_populates="drive")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    drive_id = Column(Integer, ForeignKey("placement_drives.id"))
    status = Column(SQLEnum(ApplicationStatus), default=ApplicationStatus.APPLIED)
    applied_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    student = relationship("Student", back_populates="applications")
    drive = relationship("PlacementDrive", back_populates="applications")
    interviews = relationship("Interview", back_populates="application")
    placement = relationship("Placement", back_populates="application", uselist=False)

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"))
    round_name = Column(String, nullable=False) # Technical Round 1, HR
    scheduled_time = Column(DateTime, nullable=False)
    meeting_link = Column(String, nullable=True)
    interviewer_id = Column(Integer, ForeignKey("recruiters.id"), nullable=True) # Which recruiter
    
    feedback = Column(Text, nullable=True)
    rating = Column(Float, nullable=True)
    verdict = Column(SQLEnum(InterviewVerdict), default=InterviewVerdict.PENDING)

    application = relationship("Application", back_populates="interviews")
    interviewer = relationship("Recruiter")

class Placement(Base):
    __tablename__ = "placements"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    application_id = Column(Integer, ForeignKey("applications.id"), unique=True)
    ctc_offered = Column(Float, nullable=False)
    offer_date = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("Student", back_populates="placements")
    application = relationship("Application", back_populates="placement")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    action_url = Column(String, nullable=True)

    user = relationship("User", back_populates="notifications")
