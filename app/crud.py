from sqlalchemy.orm import Session
from . import models
from fastapi import Depends, HTTPException
from .models import User
from .database import get_db


def create_dummy_data(db: Session):
    # 清空資料
    db.query(models.Submission).delete()
    db.query(models.Course).delete()
    db.query(models.User).delete()
    db.commit()

    # 建立測試使用者
    teacher = models.User(
        name="John Doe",
        email="teacher@example.com",
        password="hashedpassword",
        role="teacher",
        instrument="Piano",
    )
    teacher01 = models.User(
        name="teacher01",
        email="teacher01@example.com",
        password="123",
        role="teacher",
        instrument="Violin",
    )
    student = models.User(
        name="Jane Smith",
        email="student@example.com",
        password="hashedpassword",
        role="student",
        instrument="Guitar",
    )
    student01 = models.User(
        name="student01",
        email="student01@example.com",
        password="123",
        role="student",
        instrument="Drums",
    )

    db.add(teacher)
    db.add(teacher01)
    db.add(student)
    db.add(student01)
    db.commit()

    # 建立課程
    course = models.Course(
        title="Music Theory",
        teacher_id=teacher.id,
        student_id=student.id,
        instrument="Piano",
        schedule="Monday 10:00 AM",
    )
    course01 = models.Course(
        title="Violin Lessons",
        teacher_id=teacher01.id,
        student_id=student01.id,
        instrument="Violin",
        schedule="Tuesday 11:00 AM",
    )

    db.add(course)
    db.add(course01)
    db.commit()

    # 建立提交紀錄
    submission_teacher = models.Submission(
        course_id=course.id, user_id=teacher.id, file_url="/path/to/teacher-file.mp3"
    )
    submission_student = models.Submission(
        course_id=course.id, user_id=student.id, file_url="/path/to/student-file.mp3"
    )
    submission_teacher01 = models.Submission(
        course_id=course01.id,
        user_id=teacher01.id,
        file_url="/path/to/teacher01-file.mp3",
    )
    submission_student01 = models.Submission(
        course_id=course01.id,
        user_id=student01.id,
        file_url="/path/to/student01-file.mp3",
    )

    db.add(submission_teacher)
    db.add(submission_student)
    db.add(submission_teacher01)
    db.add(submission_student01)
    db.commit()


from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from . import models, database


def get_current_user(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
