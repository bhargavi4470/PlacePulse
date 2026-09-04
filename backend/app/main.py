from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine

from .routers import auth, students, drives, applications, admin, recruiter, interviews, placements, notifications

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="PlacePulse API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(students.router)
app.include_router(drives.router)
app.include_router(applications.router)
app.include_router(admin.router)
app.include_router(recruiter.router)
app.include_router(interviews.router)
app.include_router(placements.router)
app.include_router(notifications.router)

@app.get("/api/health", tags=["system"])
def health_check():
    return {
        "status": "ok",
        "service": "PlacePulse API"
    }

@app.get("/")
def root():
    return {"message": "Welcome to PlacePulse API"}
