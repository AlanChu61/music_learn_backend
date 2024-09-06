from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Course, Submission, User
from ..crud import get_current_user
from pydantic import BaseModel

router = APIRouter()


# Response models for Course and Submission
class SubmissionResponse(BaseModel):
    id: int
    file_url: str
    uploaded_at: datetime  # Use datetime instead of string
    user_id: int  # ID of the user who made the submission

    class Config:
        orm_mode = True


class CourseResponse(BaseModel):
    id: int
    title: str
    schedule: str
    instrument: str
    submissions: List[SubmissionResponse]

    class Config:
        orm_mode = True


# Fetch the courses for the current teacher along with submissions
@router.get("/courses", response_model=List[CourseResponse])
def get_teacher_courses(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=403, detail="Access forbidden: You are not a teacher"
        )

    courses = db.query(Course).filter(Course.teacher_id == current_user.id).all()

    return courses


# Fetch a specific course along with its submissions
@router.get("/courses/{course_id}", response_model=CourseResponse)
def get_course_with_submissions(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    course = (
        db.query(Course)
        .filter(Course.id == course_id, Course.teacher_id == current_user.id)
        .first()
    )

    if not course:
        raise HTTPException(
            status_code=404, detail="Course not found or you don't have access to it"
        )

    return course
