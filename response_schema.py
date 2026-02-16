from typing import Optional,List
from datetime import date,datetime
from pydantic import BaseModel, EmailStr


class TeacherProfileResponse(BaseModel):
    qualification:str
    experience_years : int

    class ConfigDict:
        from_attributes=True

class TeacherResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    department_id: Optional[int]
    department_name:Optional[str]=None
    teacher_profile:Optional[TeacherProfileResponse]

    class ConfigDict:
        from_attributes=True


class DepartmentResponse(BaseModel):
    id: int
    name: str

    class ConfigDict:
        from_attributes=True




class CourseResponse(BaseModel):
    id: int
    title: str
    credits: int

    class ConfigDict:
        from_attributes=True

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    semester: int
    enroll_at: datetime

    class ConfigDict:
        from_attributes=True

class StudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    enrollments: List[EnrollmentResponse] = []
    class ConfigDict:
        from_attributes=True


