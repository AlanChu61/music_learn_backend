from sqlalchemy.orm import Session
from . import models


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
        password_hash="hashedpassword",
        role="teacher",
        instrument="Piano",
    )
    teacher01 = models.User(
        name="teacher01",
        email="teacher01@example.com",
        password_hash="123",
        role="teacher",
        instrument="Violin",
    )
    student = models.User(
        name="Jane Smith",
        email="student@example.com",
        password_hash="hashedpassword",
        role="student",
        instrument="Guitar",
    )
    student01 = models.User(
        name="student01",
        email="student01@example.com",
        password_hash="123",
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


def get_current_user(db: Session = Depends(database.get_db)):
    # 通过用户的认证信息（如 email 或 token）获取当前用户
    current_user_email = "current_user_email"  # 你需要替换为实际的逻辑
    user = db.query(models.User).filter(models.User.email == current_user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
