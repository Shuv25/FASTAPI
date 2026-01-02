from pydantic import BaseModel, Field
from typing import Annotated, Optional

# ---------- MODELS ----------
class InputModel(BaseModel):
    id: int = Field(..., description="Enter your id")
    name: str = Field(..., description="Enter your name")
    age: int = Field(..., ge=18, le=100, description="Enter your age")
    job_profile: str = Field(..., description="Enter your job profile")


class UpdateModel(BaseModel):
    name: str
    age: int = Field(ge=18, le=100)
    job_profile: str


class PatchModel(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = Field(default=None, ge=18, le=100)
    job_profile: Optional[str] = None