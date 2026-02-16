from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, model_validator


class TeacherCreate(BaseModel):
    name: str
    email: EmailStr
    department_id: int
    qualification: str
    experience_years: int


class DepartmentCreate(BaseModel):
    name: str


class StudentCreate(BaseModel):
    name: str
    email: EmailStr


class CourseCreate(BaseModel):
    title: str
    credits: int


class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int
    semester: int
    enroll_at: Optional[datetime] = None

    @model_validator(mode="before")
    @classmethod
    def set_enroll_at(cls, values):
        if values.get("enroll_at") is None:
            values["enroll_at"] = datetime.now()
        return values
