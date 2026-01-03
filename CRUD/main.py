from fastapi import FastAPI, HTTPException, status
from typing import Annotated

from utils import read_data, write_data
from schema import InputModel, UpdateModel, PatchModel
from db_connections import mydb, cursor

app = FastAPI()

# ---------- CREATE ----------
@app.post("/create", status_code=status.HTTP_201_CREATED)
def create_records(payload: InputModel):
    try:
        
        # data = read_data()

        # if any(record["id"] == payload.id for record in data):
        #     raise HTTPException(
        #         status_code=status.HTTP_409_CONFLICT,
        #         detail="Record with thxis ID already exists"
        #     )

        # data.append(payload.dict())
        # write_data(data)

        # return {"message": "Record created successfully", "data": payload}

        cursor.execute(
            "SELECT id FROM records WHERE id = %s",
            (payload.id,)
        )

        existing = cursor.fetchone()
        cursor.fetchall()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Record with this ID already exists"
            )
        
        query = """
        INSERT INTO records (id, name, age, job_profile)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query,(payload.id, payload.name, payload.age, payload.job_profile))
        
        mydb.commit()

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
        # data = read_data()

        # for record in data:
        #     if record["id"] == id:
        #         return record

        # raise HTTPException(
        #     status_code=status.HTTP_404_NOT_FOUND,
        #     detail="Record not found"
        # )

        cursor.execute("select * from records where id = %s",
                       (id,))
        
        data = cursor.fetchone()
        cursor.fetchall()

        if data:
            return {"record":data}
    
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
        # data = read_data()

        # for record in data:
        #     if record["id"] == id:
        #         record["name"] = payload.name
        #         record["age"] = payload.age
        #         record["job_profile"] = payload.job_profile
        #         write_data(data)
        #         return {"message": "Record updated successfully"}
        
        cursor.execute("select id from records where id = %s",
                       (id,))
        
        data = cursor.fetchone()
        cursor.fetchall()

        if data:
            cursor.execute("update records set name = %s, age = %s, job_profile = %s where id = %s",
                           (payload.name,payload.age,payload.job_profile,id))
            
            mydb.commit()

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
        # data = read_data()

        # for record in data:
        #     if record["id"] == id:
        #         if payload.name is not None:
        #             record["name"] = payload.name
        #         if payload.age is not None:
        #             record["age"] = payload.age
        #         if payload.job_profile is not None:
        #             record["job_profile"] = payload.job_profile

        #         write_data(data)
        #         return {"message": "Record partially updated"}

        cursor.execute("select id from records where id = %s",
                       (id,))
        
        data = cursor.fetchone()
        cursor.fetchall()

        if data:
            update_fields = []
            values = []

            if payload.name is not None:
                update_fields.append("name = %s")
                values.append(payload.name)

            if payload.age is not None:
                update_fields.append("age = %s")
                values.append(payload.age)

            if payload.job_profile is not None:
                update_fields.append("job_profile = %s")
                values.append(payload.job_profile)

            if not update_fields:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No fields provided for update"
                )

            query = f"""
            UPDATE records
            SET {', '.join(update_fields)}
            WHERE id = %s
            """
            values.append(id)

            cursor.execute(query, tuple(values))
            mydb.commit()

            return {"message": "Record partially updated successfully"}

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
        # data = read_data()

        # for index, record in enumerate(data):
        #     if record["id"] == id:
        #         data.pop(index)
        #         write_data(data)
        #         return {"message": "Record deleted successfully"}

        cursor.execute("select id from records where id = %s",
                        (id,))
        
        data = cursor.fetchone()
        cursor.fetchall()

        if data:
            cursor.execute("delete from records where id = %s",
                           (id,))
            
            mydb.commit()
            
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
