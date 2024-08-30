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
    role = Column(String, index=True, nullable=False)
    profile_photo_url = Column(String, nullable=True)
    created_at = Column(
        TIMESTAMP, server_default=func.current_timestamp(), nullable=False
    )

    courses = relationship("Course", back_populates="teacher")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    schedule = Column(String, nullable=True)
    instrument = Column(String, nullable=True)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    teacher = relationship("User", back_populates="courses")
    submissions = relationship("Submission", back_populates="course")


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_url = Column(String, nullable=False)
    uploaded_at = Column(
        TIMESTAMP, server_default=func.current_timestamp(), nullable=False
    )

    course = relationship("Course", back_populates="submissions")
    student = relationship("User")
