# model/users.py
from datetime import date,time
from fastapi import Depends, HTTPException, APIRouter, Form, Path,Body
from .db import get_db

import bcrypt

GuestRouter = APIRouter(tags=["Guest"])

# CRUD operations

@GuestRouter.get("/guest/", response_model=list)
async def read_guest(
    db=Depends(get_db)
):
    query = "SELECT guest_id, First_name, last_name FROM guest"
    db[0].execute(query)
    guest = [{"guest_id": guest[0], "first_name": guest[1],"last_name": guest[2]} for guest in db[0].fetchall()]
    return guest

@GuestRouter.get("/guest/{guest_id}", response_model=dict)
async def read_guest(
    guest_id: int, 
    db=Depends(get_db)
):
    query = "SELECT  guest_id, first_name, last_name FROM guest WHERE guest_id = %s"
    db[0].execute(query, (guest_id,))
    guest = db[0].fetchone()
    if  guest:
        return {"guest_id": guest[0], "first_name":guest[1],"last_name":guest[2]}
    raise HTTPException(status_code=404, detail="Guest not found")

@GuestRouter.post("/guest/{guest_id}", response_model=dict)
async def create_guest(
    guest_id: int = Path(...), 
    first_name: str = Form(...),
    last_name: str = Form(...),
    db=Depends(get_db)
):
    # Hash the password using bcrypt
   

    query = "INSERT INTO guest (guest_id, first_name , last_name) VALUES (%s, %s, %s)"
    db[0].execute(query, (guest_id,first_name,last_name))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute(" SELECT MAX(guest_id)  FROM guest")
    new_user_id = db[0].fetchone()[0]
    db[1].commit()

    return {"id": new_user_id, "guest_id": guest_id, "first_name": first_name, "last_name": last_name}


@GuestRouter.put("/guest/{guest_id}", response_model=dict)
async def update_guest(
   
    guest_id: int = Path(...), 
    first_name: str = Form(...), 
    last_name: str = Form(...), 
    
    db=Depends(get_db)
):
    # Hash the password using bcrypt


    # Update user information in the database 
    query = "UPDATE guest SET guest = %s, first_name= %s, last_name = %s WHERE guest_id = %s"
    db[0].execute(query, (guest_id, first_name,last_name, guest_id ))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "guest updated successfully"}
    
    # If no rows were affected, user not found
    raise HTTPException(status_code=404, detail="guest not found")

@GuestRouter.delete("/guest/{guest_id}", response_model=dict)
async def delete_guest(
    guest_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the user exists
        query_check_user = "SELECT guest_id FROM guest WHERE guest_id = %s"
        db[0].execute(query_check_user, (guest_id,))
        existing_user = db[0].fetchone()

        if not existing_user:
            raise HTTPException(status_code=404, detail="guest not found")

        # Delete the user
        query_delete_user = "DELETE FROM guest WHERE guest_id = %s"
        db[0].execute(query_delete_user, (guest_id,))
        db[1].commit()

        return {"message": "guest deleted successfully"}
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
