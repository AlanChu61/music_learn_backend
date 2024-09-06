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
    uploaded_at: str  # Store as string to avoid validation issues
    user_id: int  # ID of the user who made the submission
    user_name: str  # Add this field to display the user's name

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


# Fetch the courses for the current user (teacher or student)
@router.get("/courses", response_model=List[CourseResponse])
def get_courses(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    if current_user.role == "teacher":
        courses = db.query(Course).filter(Course.teacher_id == current_user.id).all()
    elif current_user.role == "student":
        courses = db.query(Course).filter(Course.student_id == current_user.id).all()
    else:
        raise HTTPException(status_code=403, detail="Access forbidden: Invalid role")

    # Convert datetime to ISO 8601 format for all submissions and add user name
    for course in courses:
        for submission in course.submissions:
            submission.uploaded_at = submission.uploaded_at.isoformat()
            submission.user_name = submission.user.name  # Add user name to the response

    return courses


# Fetch a specific course along with its submissions
@router.get("/courses/{course_id}", response_model=CourseResponse)
def get_course_with_submissions(
    course_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Check if the current user is either the teacher or the student in the course
    course = (
        db.query(Course)
        .filter(
            Course.id == course_id,
            (Course.teacher_id == current_user.id)
            | (Course.student_id == current_user.id),
        )
        .first()
    )

    if not course:
        raise HTTPException(
            status_code=404, detail="Course not found or you don't have access to it"
        )

    # Convert datetime to ISO 8601 format for all submissions and add user name
    for submission in course.submissions:
        submission.uploaded_at = submission.uploaded_at.isoformat()
        submission.user_name = submission.user.name  # Add user name to the response

    return course
