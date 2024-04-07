# model/users.py
from fastapi import Depends, HTTPException, APIRouter, Form, Path
from .db import get_db

import bcrypt

UserRouter = APIRouter(tags=["User"])

# CRUD operations

@UserRouter.get("/user_credential/", response_model=list)
async def read_user(
    db=Depends(get_db)
):
    query = "SELECT user_id, username, password, role FROM user_credential"
    db[0].execute(query)
    user_credential = [{"user_id": user_credential[0], "username": user_credential[1],"password": user_credential[2],"role": user_credential[3]} for user_credential in db[0].fetchall()]
    return user_credential

@UserRouter.get("/user_credential/{user_id}", response_model=dict)
async def read_acad(
    user_id: int, 
    db=Depends(get_db)
):
    query = "SELECT user_id, username, password, role FROM user_credential WHERE user_id = %s"
    db[0].execute(query, (user_id,))
    user_credential = db[0].fetchone()
    if  user_credential:
        return {"user_id": user_credential[0], "username":user_credential[1],"password":user_credential[2],"role":user_credential[3]}
    raise HTTPException(status_code=404, detail="User not found")

@UserRouter.post("/user_credential/{user_id}", response_model=dict)
async def create_user(
    user_id: int = Path(...), 
    username: str = Form(...), 
    password: str = Form(...), 
    role: str = Form(...), 
    db=Depends(get_db)
):
    # Hash the password using bcrypt
    hashed_password = hash_password(str(password))

    query = "INSERT INTO user_credential (user_id, username,password, role) VALUES (%s, %s, %s, %s)"
    db[0].execute(query, (user_id,username,hashed_password, role))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute(" SELECT MAX(user_id)  FROM user_credential")
    new_user_id = db[0].fetchone()[0]
    db[1].commit()

    return {"id": new_user_id, "user_id": user_id, "username": username, "password": password,"role":role}

@UserRouter.put("/user_credential/{user_id}", response_model=dict)
async def update_user(
   
    user_id: int = Path(...), 
    username: str = Form(...), 
    password: str = Form(...), 
    role: str = Form(...), 
    db=Depends(get_db)
):
    # Hash the password using bcrypt
    hashed_password = hash_password(str(password))

    # Update user information in the database 
    query = "UPDATE user_credential SET user_id = %s, username= %s, password = %s,role = %s WHERE user_id = %s"
    db[0].execute(query, (user_id, username ,hashed_password , role, user_id ))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "User updated successfully"}
    
    # If no rows were affected, user not found
    raise HTTPException(status_code=404, detail="User not found")

@UserRouter.delete("/user_credential/{user_id}", response_model=dict)
async def delete_user(
    user_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the user exists
        query_check_user = "SELECT user_id FROM user_credential WHERE user_id = %s"
        db[0].execute(query_check_user, (user_id,))
        existing_user = db[0].fetchone()

        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Delete the user
        query_delete_user = "DELETE FROM user_credential WHERE user_id = %s"
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
