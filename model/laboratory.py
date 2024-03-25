# model/users.py
from fastapi import Depends, HTTPException, APIRouter, Form, Path
from .db import get_db

import bcrypt

LaboratoryRouter = APIRouter(tags=["Laboratory"])

# CRUD operations

@LaboratoryRouter.get("/laboratory/", response_model=list)
async def read_laboratory(
    db=Depends(get_db)
):
    query = "SELECT lab_id, capacity  FROM laboratory"
    db[0].execute(query)
    laboratory = [{"lab_id": laboratory[0], "capacity": laboratory[1]} for laboratory in db[0].fetchall()]
    return laboratory

@LaboratoryRouter.get("/laboratory/{lab_id}", response_model=dict)
async def read_laboratory(
    lab_id: int, 
    db=Depends(get_db)
):
    query = "SELECT lab_id,capacity FROM laboratory WHERE lab_id = %s"
    db[0].execute(query, (lab_id,))
    laboratory= db[0].fetchone()
    if  laboratory:
        return {"lab_id": laboratory[0], "capacity":laboratory[1]}
    raise HTTPException(status_code=404, detail="laboratory not found")

@LaboratoryRouter.post("/laboratory/{lab_id}", response_model=dict)
async def create_lab(
    lab_id: int = Path(...), 
    capacity: int = Form(...), 
    db=Depends(get_db)
):
    # Hash the password using bcrypt
    

    query = "INSERT INTO laboratory (lab_id, capacity) VALUES (%s, %s)"
    db[0].execute(query, (lab_id, capacity))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute(" SELECT MAX(lab_id)  FROM laboratory")
    new_user_id = db[0].fetchone()[0]
    db[1].commit()

    return {"id": new_user_id, "lab_id": lab_id, "capacity": capacity}

@LaboratoryRouter.put("/laboratory/{lab_id}", response_model=dict)
async def update_laboratory(
   
    lab_id: int = Path(...), 
    capacity: int = Form(...), 
    db=Depends(get_db)
):
    # Hash the password using bcrypt
  

    # Update user information in the database 
    query = "UPDATE laboratory SET lab_id = %s, capacity = %s WHERE lab_id = %s"
    db[0].execute(query, (lab_id, capacity, lab_id ))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Laboratory updated successfully"}
    
    # If no rows were affected, user not found
    raise HTTPException(status_code=404, detail="Laboratory not found")

@LaboratoryRouter.delete("/laboratory/{lab_id}", response_model=dict)
async def delete_laboratory(
    lab_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the user exists
        query_check_user = "SELECT lab_id FROM laboratory WHERE lab_id = %s"
        db[0].execute(query_check_user, (lab_id,))
        existing_user = db[0].fetchone()

        if not existing_user:
            raise HTTPException(status_code=404, detail="Laboratory not found")

        # Delete the user
        query_delete_user = "DELETE FROM laboratory WHERE lab_id = %s"
        db[0].execute(query_delete_user, (lab_id,))
        db[1].commit()

        return {"message": "Laboratory deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()

# Password hashing function using bcrypt
def hash_password(password: str):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')  # Decode bytes to string for storage
