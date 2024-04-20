# model/users.py
from fastapi import Depends, HTTPException, APIRouter, Form, Path
from .db import get_db

import bcrypt

AdminRouter = APIRouter(tags=["User"])

# CRUD operations


# admin login 

@AdminRouter.post("/admin/login/", response_model=dict)
async def login_administrator(
    username: str = Form(...), 
    password: str = Form(...), 
    db=Depends(get_db)
):
    # Query the database to check if the username exists
    query_check_user = "SELECT username FROM admin WHERE password = %s"
    db[0].execute(query_check_user, (username, password))
    user = db[0].fetchone()

    if user:
        # Retrieve the stored password from the database
        stored_password = user[0]

        if password == stored_password:
            # If username and password are correct, print login successful
             return {"message": "Login successful"}
    
    # If username or password is incorrect, raise an HTTPException
    raise HTTPException(status_code=401, detail="Incorrect username or password")



@AdminRouter.get("/admin/", response_model=list)
async def read_user(
    db=Depends(get_db)
):
    query = "SELECT admin_id, username, password, role FROM admin"
    db[0].execute(query)
    admin = [{"admin_id": admin[0], "username": admin[1],"password": admin[2],"role": admin[3]} for admin in db[0].fetchall()]
    return admin

@AdminRouter.get("/admin/{admin_id}", response_model=dict)
async def read_acad(
    admin_id: int, 
    db=Depends(get_db)
):
    query = "SELECT admin_id, username, password, role FROM admin WHERE admin_id = %s"
    db[0].execute(query, (admin_id,))
    admin = db[0].fetchone()
    if  admin:
        return {"admin_id": admin[0], "username":admin[1],"password":admin[2],"role":admin[3]}
    raise HTTPException(status_code=404, detail="User not found")

@AdminRouter.post("/admin/{admin_id}", response_model=dict)
async def create_user(
    admin_id: int = Path(...), 
    username: str = Form(...), 
    password: str = Form(...), 
    role: str = Form(...), 
    db=Depends(get_db)
):
    # Hash the password using bcrypt
    hashed_password = hash_password(str(password))

    query = "INSERT INTO admin (admin_id, username,password, role) VALUES (%s, %s, %s, %s)"
    db[0].execute(query, (admin_id,username,hashed_password, role))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute(" SELECT MAX(admin_id)  FROM admin")
    new_admin_id = db[0].fetchone()[0]
    db[1].commit()

    return {"id": new_admin_id, "admin_id": admin_id, "username": username, "password": password,"role":role}

@AdminRouter.put("/admin/{admin_id}", response_model=dict)
async def update_user(
   
    admin_id: int = Path(...), 
    username: str = Form(...), 
    password: str = Form(...), 
    role: str = Form(...), 
    db=Depends(get_db)
):
    # Hash the password using bcrypt


    # Update user information in the database 
    query = "UPDATE admin SET admin_id = %s, username= %s, password = %s,role = %s WHERE admin_id = %s"
    db[0].execute(query, (admin_id, username,password, role ))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "User updated successfully"}
    
    # If no rows were affected, user not found
    raise HTTPException(status_code=404, detail="User not found")

@AdminRouter.delete("/admin/{admin_id}", response_model=dict)
async def delete_user(
    admin_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the user exists
        query_check_user = "SELECT admin_id FROM admin WHERE admin_id = %s"
        db[0].execute(query_check_user, (admin_id,))
        existing_user = db[0].fetchone()

        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Delete the user
        query_delete_user = "DELETE FROM admin WHERE admin_id = %s"
        db[0].execute(query_delete_user, (admin_id,))
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

@AdminRouter.post("/admin/login/", response_model=dict)
async def login_administrator(
   username: str = Form(...), 
    password: str = Form(...), 
    db=Depends(get_db)
):
    # Query the database to check if the username exists
    query_check_user = "SELECT password FROM admin WHERE username = %s"
    db[0].execute(query_check_user, (username,))
    user = db[0].fetchone()

    if user:
        # Retrieve the stored password from the database
        stored_password = user[0]

        if password == stored_password:
            # If username and password are correct, print login successful
             return {"message": "Login successful"}
    
    # If username or password is incorrect, raise an HTTPException
    raise HTTPException(status_code=401, detail="Incorrect username or password")