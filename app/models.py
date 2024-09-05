from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, index=True, nullable=False)  # 'teacher' or 'student'
    instrument = Column(String, nullable=True)
    created_at = Column(
        TIMESTAMP, server_default=func.current_timestamp(), nullable=False
    )

    # 添加这行，定义 submissions 与 Submission 模型的关系
    submissions = relationship("Submission", back_populates="user")

    # 指定外键 teacher_id 的关系
    teacher_courses = relationship(
        "Course", back_populates="teacher", foreign_keys="Course.teacher_id"
    )

    # 指定外键 student_id 的关系
    student_courses = relationship(
        "Course", back_populates="student", foreign_keys="Course.student_id"
    )


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    schedule = Column(String, nullable=True)
    instrument = Column(String, nullable=True)

    # 关联到 User 表中的 teacher_id
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # 关联到 User 表中的 student_id
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # 反向关系，指定相应的外键
    teacher = relationship(
        "User", back_populates="teacher_courses", foreign_keys=[teacher_id]
    )
    student = relationship(
        "User", back_populates="student_courses", foreign_keys=[student_id]
    )

    submissions = relationship("Submission", back_populates="course")


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=False
    )  # teacher or student
    file_url = Column(String, nullable=False)
    uploaded_at = Column(
        TIMESTAMP, server_default=func.current_timestamp(), nullable=False
    )

    course = relationship("Course", back_populates="submissions")
    user = relationship("User", back_populates="submissions")
