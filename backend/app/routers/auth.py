from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from .. import models, schemas, auth, database

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "role": user.role}

@router.post("/register")
def register_student(student_in: schemas.StudentRegister, db: Session = Depends(database.get_db)):
    if db.query(models.User).filter(models.User.email == student_in.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if db.query(models.Student).filter(models.Student.roll_number == student_in.roll_number).first():
        raise HTTPException(status_code=400, detail="Roll number already registered")

    # Create User
    new_user = models.User(
        email=student_in.email,
        hashed_password=auth.get_password_hash(student_in.password),
        full_name=student_in.full_name,
        role=models.RoleEnum.STUDENT
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create Student Profile
    new_student = models.Student(
        user_id=new_user.id,
        roll_number=student_in.roll_number,
        branch=student_in.branch,
        graduation_year=student_in.graduation_year,
        cgpa=student_in.cgpa,
        profile_readiness=50 # Base score
    )
    db.add(new_student)
    db.commit()
    
    return {"message": "Registration successful. You can now login."}

@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(auth.get_current_active_user)):
    return current_user
