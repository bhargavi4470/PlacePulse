# 🎓 PlacePulse - Smart Campus Placement Management Platform

<p align="center">

![Angular](https://img.shields.io/badge/Angular-20+-DD0031?style=for-the-badge&logo=angular&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5+-3178C6?style=for-the-badge&logo=typescript&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=for-the-badge)
![JWT](https://img.shields.io/badge/JWT-Authentication-000000?style=for-the-badge&logo=jsonwebtokens)
![Gemini](https://img.shields.io/badge/Google%20Gemini-AI-4285F4?style=for-the-badge&logo=google)
![GitHub API](https://img.shields.io/badge/GitHub-API-181717?style=for-the-badge&logo=github)

</p>

<p align="center">
A full-stack Smart Campus Placement Management Platform that connects students, placement officers, and recruiters while managing the complete placement lifecycle from eligibility evaluation to final selection.
</p>

---

# 📖 Project Overview

**PlacePulse** is a full-stack campus placement management platform designed to simplify and digitize the placement process within educational institutions.

The platform connects three major users:

- 👨‍🎓 Students
- 👨‍💼 Placement Officers / Administrators
- 🏢 Recruiters / Companies

PlacePulse manages the complete placement workflow, including student profiles, company drives, eligibility verification, applications, candidate shortlisting, interview scheduling, feedback, offers, and placement analytics.

The system also includes a **rule-based Eligibility Engine** that evaluates students against company-specific placement criteria and provides clear explanations for eligibility or rejection.

The platform is designed as a production-style SaaS application with a modern Angular frontend and a FastAPI backend.

---

# ✨ Key Features

## 👨‍🎓 Student Features

- Student registration and login
- JWT-based authentication
- Student profile management
- Academic information management
- Skills management
- Project management
- Certification management
- Resume upload and management
- GitHub profile integration
- Placement drive discovery
- Eligibility verification
- One-click application
- Application status tracking
- Interview schedule tracking
- Interview feedback viewing
- Offer tracking
- Placement status
- Notifications
- Smart job/drive recommendations

---

## 👨‍💼 Placement Officer / Admin Features

- Admin dashboard
- Student registry
- Company management
- Recruiter management
- Placement drive management
- Eligibility Engine
- Eligibility rule creation and editing
- Batch eligibility evaluation
- Candidate verification
- Application management
- Interview management
- Offer and selection management
- Placement tracking
- Placement analytics
- Notifications
- Resume verification
- Reports
- Audit logs
- College settings

---

## 🏢 Recruiter Features

- Recruiter registration and login
- Company profile management
- Placement drive creation
- Job requirement management
- Candidate discovery
- Eligibility-based candidate filtering
- Candidate profile viewing
- Resume viewing
- Candidate shortlisting
- Candidate rejection
- Interview scheduling
- Interview rescheduling
- Interview feedback
- Candidate ratings
- Candidate selection
- Selected candidate management

Recruiters can access only the candidates and placement drives belonging to their company.

---

# 🧠 Eligibility Engine

One of the core features of PlacePulse is its **Rule-Based Eligibility Engine**.

Placement officers can define company-specific eligibility criteria.

Example:

```text
Company: ABC Technologies

CGPA >= 8.0
Active Backlogs = 0
Department IN [CSE, IT, AI&DS]
10th Percentage >= 75%
12th Percentage >= 75%
Required Skill = Java
Graduation Year = 2027
