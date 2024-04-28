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

@GuestRouter.post("/guest/", response_model=dict)
async def create_guest(
    first_name: str = Form(...),
    last_name: str = Form(...),
    date: str = Form(...),  # Assuming date is provided as a string in the format 'YYYY-MM-DD'
    time_in: str = Form(...),
    time_out: str = Form(...),
    db=Depends(get_db)
):
    # Hash the password using bcrypt
   
    # Insert the guest record into the database
    query = "INSERT INTO guest (first_name, last_name, date, time_in, time_out) VALUES (%s, %s, %s, %s, %s)"
    db[0].execute(query, (first_name, last_name, date, time_in, time_out))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_guest_id = db[0].fetchone()[0]
    db[1].commit()

    return {"guest_id": new_guest_id, "first_name": first_name, "last_name": last_name, "date": date, "time_in": time_in, "time_out": time_out}



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
