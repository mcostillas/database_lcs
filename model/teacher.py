# model/users.py
from fastapi import Depends, HTTPException, APIRouter, Form, Path
from .db import get_db

import bcrypt

TeacherRouter = APIRouter(tags=["Teacher"])

# CRUD operations

@TeacherRouter.get("/teacher", response_model=list)
async def read_teacher(
    db=Depends(get_db)
):
    query = "SELECT teacherteacher_id, first_name, last_name FROM teacher"
    db[0].execute(query)
    teacher = [{"teacherr_id": teacher[0], "first_Name": teacher[1],"last_Name": teacher[2]} for teacher in db[0].fetchall()]
    return teacher

@TeacherRouter.get("/teacher/{teacher_id}", response_model=dict)
async def read_teacher(
    teacher_id: int, 
    db=Depends(get_db)
):
    query = "SELECT teacher_id, first_name, last_nameFROM teacher WHERE teacher_id = %s"
    db[0].execute(query, (teacher_id,))
    teacher = db[0].fetchone()
    if  teacher:
        return {"teacher_id": teacher[0], "first_name":teacher[1],"last_name":teacher[2]}
    raise HTTPException(status_code=404, detail="teacher not found")

@TeacherRouter.post("/teacher/{teacher_id}", response_model=dict)
async def create_teacher(
    teacher_id: int = Path(...), 
    first_name: str = Form(...), 
    last_name: str = Form(...), 
    db=Depends(get_db)
):
    # Hash the password using bcrypt

    query = "INSERT INTO teacher(teacher_id, first_name,last_name) VALUES (%s, %s, %s)"
    db[0].execute(query, (teacher_id,first_name,last_name))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute(" SELECT MAX(teacher_id)  FROM teacher")
    new_user_id = db[0].fetchone()[0]
    db[1].commit()

    return {"id": new_user_id, "teacher_id": teacher_id, "first_name": first_name, "last_name": last_name}

@TeacherRouter.put("/teacher/{teacher_id}", response_model=dict)
async def update_teacher(
   
    teacher_id: int = Path(...), 
    first_name: str = Form(...), 
    last_name: str = Form(...), 
    db=Depends(get_db)
):
    # Hash the password using bcrypt
   

    # Update user information in the database 
    query = "UPDATE teacher SET teacher_id = %s, first_name= %s, last_name = %s WHERE teacher_id = %s"
    db[0].execute(query, (teacher_id, first_name,last_name, teacher_id ))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "teacher updated successfully"}
    
    # If no rows were affected, user not found
    raise HTTPException(status_code=404, detail="teacher not found")

@TeacherRouter.delete("/teacher/{teacher_id}", response_model=dict)
async def delete_teacher(
    teacher_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the user exists
        query_check_user = "SELECT teacher_id FROM teacher WHERE teacher_id = %s"
        db[0].execute(query_check_user, (teacher_id,))
        existing_user = db[0].fetchone()

        if not existing_user:
            raise HTTPException(status_code=404, detail="teacher not found")

        # Delete the user
        query_delete_user = "DELETE FROM teacher WHERE teacher_id = %s"
        db[0].execute(query_delete_user, (teacher_id,))
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
