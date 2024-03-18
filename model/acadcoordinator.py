# model/users.py
from fastapi import Depends, HTTPException, APIRouter, Form
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

@AcadcoordinatorRouter.post("/users/", response_model=dict)
async def create_user(
    email: str = Form(...), 
    username: str = Form(...), 
    password: str = Form(...), 
    db=Depends(get_db)
):
    # Hash the password using bcrypt
    hashed_password = hash_password(password)

    query = "INSERT INTO users (email, username, password) VALUES (%s, %s, %s)"
    db[0].execute(query, (email, username, hashed_password))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_user_id = db[0].fetchone()[0]
    db[1].commit()

    return {"id": new_user_id, "username": username}

@AcadcoordinatorRouter.put("/users/{user_id}", response_model=dict)
async def update_user(
    user_id: int,
    email: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    db=Depends(get_db)
):
    # Hash the password using bcrypt
    hashed_password = hash_password(password)

    # Update user information in the database 
    query = "UPDATE users SET email = %s, username = %s, password = %s WHERE id = %s"
    db[0].execute(query, (email, username, hashed_password, user_id))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "User updated successfully"}
    
    # If no rows were affected, user not found
    raise HTTPException(status_code=404, detail="User not found")

@AcadcoordinatorRouter.delete("/users/{user_id}", response_model=dict)
async def delete_user(
    user_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the user exists
        query_check_user = "SELECT id FROM users WHERE id = %s"
        db[0].execute(query_check_user, (user_id,))
        existing_user = db[0].fetchone()

        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Delete the user
        query_delete_user = "DELETE FROM users WHERE id = %s"
        db[0].execute(query_delete_user, (user_id,))
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
