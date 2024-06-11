from sqlmodel import Field, Relationship

from .base import Base
class Enrollments(Base, table=True):
    __tablename__ = 'enrollments'

    student_id: int | None = Field(default=None, foreign_key='students.id')
    course_id: int | None = Field(default=None, foreign_key='courses.id')