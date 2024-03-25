# model/users.py
from fastapi import Depends, HTTPException, APIRouter, Form, Path
from .db import get_db

import bcrypt

AdminRouter = APIRouter(tags=["Admin"])

# CRUD operations

@AdminRouter.get("/admin/", response_model=list)
async def read_admin(
    db=Depends(get_db)
):
    query = "SELECT admin_id, first_name, last_name FROM admin"
    db[0].execute(query)
    academic_coordinator = [{"admin_id": admin[0], "first_Name": admin[1],"last_Name": admin[2],} for admin in db[0].fetchall()]
    return academic_coordinator

@AdminRouter.get("/admin/{admin_id}", response_model=dict)
async def read_admin(
    admin_id: int, 
    db=Depends(get_db)
):
    query = "SELECT admin_id, first_name, last_name FROM admin WHERE admin_id = %s"
    db[0].execute(query, (admin_id,))
    admin = db[0].fetchone()
    if  admin:
        return {"admin_id": admin[0], "first_name":admin[1],"last_name":admin[2]}
    raise HTTPException(status_code=404, detail="User not found")

@AdminRouter.post("/admin/{admin_id}", response_model=dict)
async def create_admin(
    admin_id: int = Path(...), 
    first_name: str = Form(...), 
    last_name: str = Form(...), 
    db=Depends(get_db)
):
    # Hash the password using bcrypt
   

    query = "INSERT INTO admin (admin_id, first_name,last_name) VALUES (%s, %s, %s)"
    db[0].execute(query, (admin_id,first_name,last_name))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute(" SELECT MAX(admin_id)  FROM admin")
    new_user_id = db[0].fetchone()[0]
    db[1].commit()

    return {"id": new_user_id, "admin_id": admin_id, "first_name": first_name, "last_name": last_name}

@AdminRouter.put("/admin/{admin_id}", response_model=dict)
async def update_admin(
   
    admin_id: int = Path(...), 
    first_name: str = Form(...), 
    last_name: str = Form(...), 
   
    db=Depends(get_db)
):
    # Hash the password using bcrypt
    

    # Update user information in the database 
    query = "UPDATE admin SET admin_id = %s, first_name= %s, last_name = %s WHERE admin_id = %s"
    db[0].execute(query, (admin_id, first_name,last_name, admin_id ))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "User updated successfully"}
    
    # If no rows were affected, user not found
    raise HTTPException(status_code=404, detail="User not found")

@AdminRouter.delete("/admin/{admin_id}", response_model=dict)
async def delete_admin(
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
