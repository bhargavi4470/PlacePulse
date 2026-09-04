from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class RoleEnum(str, Enum):
    STUDENT = "STUDENT"
    ADMIN = "ADMIN"
    RECRUITER = "RECRUITER"

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[RoleEnum] = None

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: RoleEnum

class UserCreate(UserBase):
    password: str

class StudentRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    roll_number: str
    branch: str
    graduation_year: int
    cgpa: float

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    roll_number: str
    branch: str
    graduation_year: int
    cgpa: float
    active_backlogs: int = 0
    historical_backlogs: int = 0
    tenth_percentage: Optional[float] = None
    twelfth_percentage: Optional[float] = None
    github_username: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class Student(StudentBase):
    id: int
    user_id: int
    profile_readiness: int

    class Config:
        from_attributes = True

class CompanyBase(BaseModel):
    name: str
    description: Optional[str] = None
    website: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int

    class Config:
        from_attributes = True

class PlacementDriveBase(BaseModel):
    job_title: str
    job_description: Optional[str] = None
    ctc: float
    location: Optional[str] = None
    job_type: Optional[str] = None
    registration_deadline: datetime
    min_cgpa: float = 0.0
    max_active_backlogs: int = 0
    max_historical_backlogs: int = 0
    allowed_branches: Optional[str] = None

class PlacementDriveCreate(PlacementDriveBase):
    company_id: int

class PlacementDrive(PlacementDriveBase):
    id: int
    status: str
    company_id: int

    class Config:
        from_attributes = True

class ApplicationBase(BaseModel):
    drive_id: int

class ApplicationCreate(ApplicationBase):
    pass

class Application(ApplicationBase):
    id: int
    student_id: int
    status: str
    applied_at: datetime

    class Config:
        from_attributes = True
