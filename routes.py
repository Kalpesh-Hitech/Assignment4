from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from urllib3 import HTTPResponse
from sqlalchemy.orm import joinedload  

from create_schemas import (
    CourseCreate,
    DepartmentCreate,
    EnrollmentCreate,
    StudentCreate,
    TeacherCreate,
)
from models import get_db
from models import (
    Course,
    Department,
    Enrollment,
    Student,
    Teacher,
    TeacherProfile,
)
from response_schema import (
    CourseResponse,
    DepartmentResponse,
    EnrollmentResponse,
    StudentResponse,
    TeacherResponse,
)

router = APIRouter()


@router.post("/teachers", response_model=TeacherResponse)
def teacher_create(teachers: TeacherCreate, db: Session = Depends(get_db)):
    valid_department_id = (
        db.query(Department).filter(Department.id == teachers.department_id).first()
    )
    if valid_department_id is None:
        raise HTTPException(
            status_code=404, detail="please enter the valid department id"
        )
    teacher = Teacher(
        name=teachers.name,
        email=teachers.email,
        department_id=teachers.department_id
    )
    teacherprofile=TeacherProfile(
        qualification=teachers.qualification,
        experience_years=teachers.experience_years,
        teacher=teacher
    )
    db.add_all([teacher,teacherprofile])
    db.commit()
    db.refresh(teacher)
    return teacher


@router.post("/department", response_model=DepartmentResponse)
def create_department(department_info: DepartmentCreate, db: Session = Depends(get_db)):
    db_department = Department(**department_info.model_dump())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


@router.post("/students", response_model=StudentResponse)
def create_student(student_info: StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(**student_info.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@router.post("/courses", response_model=CourseResponse)
def create_course(courses_info: CourseCreate, db: Session = Depends(get_db)):
    db_course = Course(**courses_info.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@router.post("/enrollement", response_model=EnrollmentResponse)
def create_enroll(enrollment_info: EnrollmentCreate, db: Session = Depends(get_db)):
    db_student = (
        db.query(Student).filter(Student.id == enrollment_info.student_id).first()
    )
    if db_student is None:
        raise HTTPException(status_code=404, detail="student id in invaild")
    db_course = db.query(Course).filter(Course.id == enrollment_info.course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="course id in invaild")
    db_enrollment = Enrollment(**enrollment_info.model_dump())

    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment

from sqlalchemy.orm import joinedload

@router.get("/lazy/teachers/{id}", response_model=TeacherResponse)
def get_teacher(id: int, db: Session = Depends(get_db)):
    db_teacher = (
        db.query(Teacher)
        .options(
            joinedload(Teacher.teacher_profile),
            joinedload(Teacher.department)
        )
        .filter(Teacher.id == id)
        .first()
    )
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Please enter a valid teacher id!")

    db_teacher.department_name = (
        db_teacher.department.name if db_teacher.department else None
    )

    return db_teacher


@router.get("/lazy/students/{student_id}")
def get_student(student_id:int, db:Session=Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
 
    return {
        "name": student.name,
        "courses": [{"title":c.course.title, "semester":c.semester} for c in student.enrollments]
    }

@router.get("/lazy/courses/{id}")
def get_course_student(id:int,db:Session=Depends(get_db)):
    course = db.query(Course).filter(Course.id == id).first()
 
    return {
        "courses": course.title,
        "students": [c.student.name for c in course.enrollments]
    }