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
    )
    student = models.User(
        name="Jane Smith",
        email="student@example.com",
        password_hash="hashedpassword",
        role="student",
    )
    db.add(teacher)
    db.add(student)
    db.commit()

    # 建立課程
    course = models.Course(
        title="Piano Lessons",
        teacher_id=teacher.id,
        schedule="Monday 10:00 AM",
        instrument="Piano",
    )
    db.add(course)
    db.commit()

    # 建立提交紀錄
    submission = models.Submission(
        course_id=course.id, student_id=student.id, file_url="/path/to/file1.mp3"
    )
    db.add(submission)
    db.commit()
