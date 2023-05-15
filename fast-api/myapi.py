from typing import Optional
import string
from fastapi import FastAPI
from pydantic import BaseModel, validator


class Student(BaseModel):
    name: str
    age: int
    year: str

    @validator("name")
    @classmethod
    def username_valid(cls, value):
        if (p in value for p in string.punctuation):
            raise ValueError("Name should not contain any punctuations")


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None

    @validator("name")
    @classmethod
    def username_valid(cls, value):
        if (p in value for p in string.punctuation):
            raise ValueError("Name should not contain any punctuations")


app = FastAPI()

students = {
    1: {"name": "Rakesh", "age": 20, "year": "12"},
    2: {"name": "Ram", "age": 18, "year": "10"},
}


@app.get("/")
def index():
    return {"name": "Home/Index Page"}


@app.get("/get-student/{student_id}")
def getSudent(student_id: int):
    if student_id in students.keys():
        return students[student_id]
    else:
        return {"Error": "No student found"}


@app.get("/get-student-by-name")
def getStudent(name: str):
    for stu_id in students:
        if students[stu_id]["name"] == name:
            return students[stu_id]

    return {"123": "No data found"}


@app.post("/create-student/{student_id}")
def createStudent(student_id: int, student: Student):
    if student_id in students:
        return {"error": "Student with given id already exists"}
    else:
        students[student_id] = student
    return students


@app.put("/update-student/{student_id}")
def updateStudent(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student with given id not found"}
    if student.name is not None:
        students[student_id]["name"] = student.name
    if student.age is not None:
        students[student_id]["age"] = student.age
    if student.year is not None:
        students[student_id]["year"] = student.year
    return students


@app.delete("/delete-student/{student_id}")
def deleteStudent(student_id: int):
    if student_id not in students:
        return {"Error": "Student with given id not found"}
    del students[student_id]
    return {"Data": "Student deleted successfully"}
