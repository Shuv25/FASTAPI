from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Annotated, Optional
from utils import read_data, write_data

app = FastAPI()


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


# ---------- CREATE ----------
@app.post("/create", status_code=status.HTTP_201_CREATED)
def create_records(payload: InputModel):
    try:
        data = read_data()

        if any(record["id"] == payload.id for record in data):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Record with this ID already exists"
            )

        data.append(payload.dict())
        write_data(data)

        return {"message": "Record created successfully", "data": payload}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ---------- READ ----------
@app.get("/read/{id}")
def read_records(id: Annotated[int, "Enter your id"]):
    try:
        data = read_data()

        for record in data:
            if record["id"] == id:
                return record

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ---------- PUT (FULL UPDATE) ----------
@app.put("/large_update/{id}")
def update_records(id: int, payload: UpdateModel):
    try:
        data = read_data()

        for record in data:
            if record["id"] == id:
                record["name"] = payload.name
                record["age"] = payload.age
                record["job_profile"] = payload.job_profile
                write_data(data)
                return {"message": "Record updated successfully"}

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ---------- PATCH (PARTIAL UPDATE) ----------
@app.patch("/small_update/{id}")
def patch_records(id: int, payload: PatchModel):
    try:
        data = read_data()

        for record in data:
            if record["id"] == id:
                if payload.name is not None:
                    record["name"] = payload.name
                if payload.age is not None:
                    record["age"] = payload.age
                if payload.job_profile is not None:
                    record["job_profile"] = payload.job_profile

                write_data(data)
                return {"message": "Record partially updated"}

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ---------- DELETE ----------
@app.delete("/delete/{id}", status_code=status.HTTP_200_OK)
def delete_record(id: int):
    try:
        data = read_data()

        for index, record in enumerate(data):
            if record["id"] == id:
                data.pop(index)
                write_data(data)
                return {"message": "Record deleted successfully"}

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Record not found"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
