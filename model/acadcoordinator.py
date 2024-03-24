# model/users.py
from fastapi import Depends, HTTPException, APIRouter, Form, Path
from .db import get_db

import bcrypt

AcadcoordinatorRouter = APIRouter(tags=["Academic Coordinator"])

# CRUD operations

@AcadcoordinatorRouter.get("/academic_coordinator/", response_model=list)
async def read_acad(
    db=Depends(get_db)
):
    query = "SELECT coordinator_id, first_name, last_name, schedule_id FROM academic_coordinator"
    db[0].execute(query)
    academic_coordinator = [{"coordinator_id": academic_coordinator[0], "first_Name": academic_coordinator[1],"last_Name": academic_coordinator[2],"schedule_id": academic_coordinator[3]} for academic_coordinator in db[0].fetchall()]
    return academic_coordinator

@AcadcoordinatorRouter.get("/academic_coordinator/{coordinator_id}", response_model=dict)
async def read_acad(
    coordinator_id: int, 
    db=Depends(get_db)
):
    query = "SELECT coordinator_id, first_name, last_name, schedule_id FROM academic_coordinator WHERE coordinator_id = %s"
    db[0].execute(query, (coordinator_id,))
    academic_coordinator = db[0].fetchone()
    if  academic_coordinator:
        return {"coordinator_id": academic_coordinator[0], "first_name":academic_coordinator[1],"last_name":academic_coordinator[2],"schedule_id":academic_coordinator[3]}
    raise HTTPException(status_code=404, detail="User not found")

@AcadcoordinatorRouter.post("/academic_coordinator/{coordinator_id}", response_model=dict)
async def create_user(
    coordinator_id: int = Path(...), 
    first_name: str = Form(...), 
    last_name: str = Form(...), 
    schedule_id: int = Form(...), 
    db=Depends(get_db)
):
    # Hash the password using bcrypt
    hashed_scheduleid = hash_password(schedule_id)

    query = "INSERT INTO academic_coordinator (coordinator_id, first_name,last_name, schedule_id) VALUES (%s, %s, %s, %s)"
    db[0].execute(query, (coordinator_id,first_name,last_name, hashed_scheduleid))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute(" SELECT MAX(coordinator_id)  FROM academic_coordinator")
    new_user_id = db[0].fetchone()[0]
    db[1].commit()

    return {"id": new_user_id, "coordinator_id": coordinator_id, "first_name": first_name, "last_name": last_name,"schedule_id":schedule_id}

@AcadcoordinatorRouter.put("/academic_coordinator/{coordinator_id}", response_model=dict)
async def update_user(
   
    coordinator_id: int = Path(...), 
    first_name: str = Form(...), 
    last_name: str = Form(...), 
    schedule_id: int = Form(...), 
    db=Depends(get_db)
):
    # Hash the password using bcrypt
    hashed_scheduleid = hash_password(str(schedule_id))

    # Update user information in the database 
    query = "UPDATE academic_coordinator SET coordinator_id = %s, first_name= %s, last_name = %s,schedule_id = %s WHERE id = %s"
    db[0].execute(query, (coordinator_id, first_name,last_name, hashed_scheduleid,coordinator_id ))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "User updated successfully"}
    
    # If no rows were affected, user not found
    raise HTTPException(status_code=404, detail="User not found")

@AcadcoordinatorRouter.delete("/academic_coordinator/{coordinator_id}", response_model=dict)
async def delete_user(
    coordinator_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the user exists
        query_check_user = "SELECT coordinator_id FROM academic_coordinator WHERE id = %s"
        db[0].execute(query_check_user, (coordinator_id,))
        existing_user = db[0].fetchone()

        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Delete the user
        query_delete_user = "DELETE FROM academic_coordinator WHERE id = %s"
        db[0].execute(query_delete_user, (coordinator_id,))
        db[1].commit()

        return {"message": "User deleted successfully"}
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
