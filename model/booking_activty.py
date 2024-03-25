# model/users.py
from datetime import date,time
from fastapi import Depends, HTTPException, APIRouter, Form, Path,Body
from .db import get_db

import bcrypt

BookingRouter = APIRouter(tags=["Booking Activity"])

# CRUD operations

@BookingRouter.get("/booking_activity/", response_model=list)
async def read_booking(
    db=Depends(get_db)
):
    query = "SELECT booking_id, guest_id, date, time FROM booking_activity"
    db[0].execute(query)
    booking_activity = [{"booking_id": booking_activity[0], "guest_id": booking_activity[1],"date": booking_activity[2],"time": booking_activity[3]} for booking_activity in db[0].fetchall()]
    return booking_activity

@BookingRouter.get("/booking_activity/{booking_id}", response_model=dict)
async def read_booking(
    booking_id: int, 
    db=Depends(get_db)
):
    query = "SELECT booking_id, guest_id, date , time FROM booking_activity WHERE booking_id = %s"
    db[0].execute(query, (booking_id,))
    booking_activity = db[0].fetchone()
    if  booking_activity:
        return {"booking_id": booking_activity[0], "guest_id":booking_activity[1],"date":booking_activity[2],"time":booking_activity[3]}
    raise HTTPException(status_code=404, detail="Booking not found")

@BookingRouter.post("/booking_activity/{booking_id}", response_model=dict)
async def create_booking(
    booking_id: int = Path(...), 
    guest_id: int = Form(...), 
    date_input: date = Body(...),
    time_input: time = Body(...),
    db=Depends(get_db)
):
    # Hash the password using bcrypt
   

    query = "INSERT INTO booking_activity (booking_id, guest_id, date , time) VALUES (%s, %s, %s, %s)"
    db[0].execute(query, (booking_id,guest_id,date_input, time_input))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute(" SELECT MAX(booking_id)  FROM booking_activity")
    new_user_id = db[0].fetchone()[0]
    db[1].commit()

    return {"id": new_user_id, "booking_id": booking_id, "guest_id": guest_id, "date": date_input,"time":time_input}


@BookingRouter.put("/booking_activity/{booking_id}", response_model=dict)
async def update_booking(
   
    booking_id: int = Path(...), 
    guest_id: int = Form(...), 
    date_input: date = Body(...),
    time_input: time = Body(...),

    db=Depends(get_db)
):
    # Hash the password using bcrypt

    # Update user information in the database 
    query = "UPDATE booking_activity SET booking_id = %s, guest_id= %s, date = %s,time = %s WHERE booking_id = %s"
    db[0].execute(query, (booking_id, guest_id,date, time,booking_id ))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Booking updated successfully"}
    
    # If no rows were affected, user not found
    raise HTTPException(status_code=404, detail="Booking not found")

@BookingRouter.delete("/booking_activity/{booking_id}", response_model=dict)
async def delete_booking(
    booking_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the user exists
        query_check_user = "SELECT booking_id FROM booking_activity WHERE booking_id = %s"
        db[0].execute(query_check_user, (booking_id,))
        existing_user = db[0].fetchone()

        if not existing_user:
            raise HTTPException(status_code=404, detail="booking not found")

        # Delete the user
        query_delete_user = "DELETE FROM booking_activity WHERE booking_id = %s"
        db[0].execute(query_delete_user, (booking_id,))
        db[1].commit()

        return {"message": "Booking deleted successfully"}
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
