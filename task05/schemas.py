
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional


class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, description="Student's full name")
    age: int = Field(..., gt=0, le=120, description="Must be a positive, realistic age")
    major: Optional[str] = None
    email: Optional[EmailStr] = None


class StudentCreate(StudentBase):
    """Used for POST /students -- the client must supply an id."""
    id: int = Field(..., gt=0, description="Unique student ID")


class StudentUpdate(BaseModel):
    """
    Used for PUT /students/{id}.
    Every field is optional here, so the client can send just the
    field(s) they want to change (e.g. only 'age') without having to
    resend everything.
    """
    name: Optional[str] = Field(None, min_length=1)
    age: Optional[int] = Field(None, gt=0, le=120)
    major: Optional[str] = None
    email: Optional[EmailStr] = None


class StudentOut(StudentBase):
    """Used for responses -- includes the id, read from the ORM object."""
    id: int

    model_config = ConfigDict(from_attributes=True)  # lets us return a Student ORM object directly
