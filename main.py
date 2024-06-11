import uvicorn
from fastapi import FastAPI, Depends
from sqlmodel import Session, select, func
from db import get_session
from models.students import Students
from models.courses import Courses
from models.enrollments import Enrollments

from models.students import Students
from models.courses import Courses
from models.enrollments import Enrollments

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/students")
def list_students(session: Session = Depends(get_session)):
    statement = select(Students)
    results = session.exec(statement).all()
    return results 

@app.get("/courses")
def list_courses(session: Session = Depends(get_session)):
    statement = select(Courses)
    results = session.exec(statement).all()
    return results 

@app.get("/enrollments/courses")
def list_course_enrollments(session: Session = Depends(get_session)):
    statement = select(
        Courses.name.label('course_name'), 
        func.array_agg(Students.name).label('students')
    ).select_from(
        Enrollments
    ).join(
        Students, Students.id == Enrollments.student_id
    ).join(
        Courses, Courses.id == Enrollments.course_id
    ).group_by(
        Courses.name
    )
    results = session.exec(statement).mappings().all()
    return results 

@app.get("/enrollments/students")
def list_student_enrollments(session: Session = Depends(get_session)):
    statement = select(
        func.array_agg(Courses.name).label('course_name'), 
        Students.name.label('students')
    ).select_from(
        Enrollments
    ).join(
        Students, Students.id == Enrollments.student_id
    ).join(
        Courses, Courses.id == Enrollments.course_id
    ).group_by(
        Students.name
    )
    results = session.exec(statement).mappings().all()
    return results 

if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)