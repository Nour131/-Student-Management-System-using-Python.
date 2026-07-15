from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

import models
import schemas
from database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Management API",
    description="Task 05 - REST API version of the Task 04 Student Management System",
    version="1.0.0",
)


@app.post("/students", response_model=schemas.StudentOut, status_code=status.HTTP_201_CREATED)
def add_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    """Add a new student. Fails with 400 if the ID is already taken."""
    existing = db.query(models.Student).filter(models.Student.id == student.id).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail=f"A student with id {student.id} already exists.")

    new_student = models.Student(**student.model_dump())
    db.add(new_student)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not create student.")
    db.refresh(new_student)
    return new_student


@app.get("/students", response_model=List[schemas.StudentOut])
def view_students(db: Session = Depends(get_db)):
    """Return every student in the database."""
    return db.query(models.Student).all()


@app.get("/students/{student_id}", response_model=schemas.StudentOut)
def search_by_id(student_id: int, db: Session = Depends(get_db)):
    """Fetch one student by ID. 404s if not found."""
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"No student found with id {student_id}.")
    return student


@app.put("/students/{student_id}", response_model=schemas.StudentOut)
def update_student(student_id: int, updates: schemas.StudentUpdate, db: Session = Depends(get_db)):
    """Update one or more fields of an existing student. 404s if not found."""
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"No student found with id {student_id}.")

    
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(student, field, value)

    db.commit()
    db.refresh(student)
    return student


@app.delete("/students/{student_id}", status_code=status.HTTP_200_OK)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """Remove a student by ID. 404s if not found."""
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"No student found with id {student_id}.")

    db.delete(student)
    db.commit()
    return {"message": f"Student {student_id} deleted successfully."}
