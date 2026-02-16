import datetime

from pydantic import EmailStr
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base,engine,SessionLocal


class Teacher(Base):
    __tablename__ = "teacher"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)

    department_id = Column(
        Integer, ForeignKey("department.id", ondelete="SET NULL"), nullable=True
    )

    teacher_profile = relationship(
        "TeacherProfile",
        back_populates="teacher",
        uselist=False,
        cascade="all,delete-orphan"
    )

    department = relationship("Department", back_populates="teacher")


class TeacherProfile(Base):

    __tablename__ = "teacher_profile"

    id = Column(Integer, primary_key=True, index=True)
    qualification = Column(String)
    experience_years = Column(Integer)

    teacher_id = Column(
        Integer, ForeignKey("teacher.id", ondelete="CASCADE"), unique=True
    )

    teacher = relationship("Teacher", back_populates="teacher_profile")


class Department(Base):

    __tablename__ = "department"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    teacher = relationship("Teacher", back_populates="department")


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    enrollments = relationship(
        "Enrollment", back_populates="student", cascade="all,delete-orphan"
    )


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    credits = Column(Integer)
    enrollments = relationship(
        "Enrollment", back_populates="course", cascade="all,delete-orphan"
    )


class Enrollment(Base):
    __tablename__ = "enrollment"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"))
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"))
    semester = Column(Integer)
    enroll_at = Column(DateTime, default=datetime.datetime.now())
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()