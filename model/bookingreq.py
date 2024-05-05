from datetime import date,time
from fastapi import Depends, HTTPException, APIRouter, Form, Path, Body
from .db import get_db

import bcrypt

BookingRouter = APIRouter(tags=["Booking Requests"])

# CRUD operations

@BookingRouter.get("/bookings/", response_model=list)
async def read_bookings(
    db=Depends(get_db)
):
    query = "SELECT b.DateIn, b.TimeIn, b.TimeOut, g.FirstName, g.LastName, b.Purpose FROM bookings b INNER JOIN guests g ON b.GuestID = g.GuestID"
    db[0].execute(query)
    bookings = [{"DateIN": booking[0], "TimeIn": booking[1], "TimeOut": booking[2],"FirstName": booking[3],"LastName": booking[4],"Purpose": booking[5]} for booking in db[0].fetchall()]
    # Close cursor
    db[0].close()
    return bookings

@BookingRouter.get("/bookings/{requestid}", response_model=dict)
async def read_bookings(
    requestid: int, 
    db=Depends(get_db)
):
    query = "SELECT  requestid, userid ,Firstname, Lastname, purpose, daterequested,status FROM bookings WHERE requestid = %s"
    db[0].execute(query, (requestid,))
    bookings = db[0].fetchone()
    if bookings:
        # Close cursor
        db[0].close()
        return {"requestid": bookings[0], "userid": bookings[1], "Firstname": bookings[2],"Lastname": bookings[3],"purpose": bookings[4],"daterequested": bookings[5],"status": bookings[6]}
    raise HTTPException(status_code=404, detail="bookings not found")

@BookingRouter.post("/bookings/", response_model=dict)
async def create_bookings(
    Firstname: str = Form(...),
    Lastname: str = Form(...),
    purpose: str = Form(...),
    daterequested: str = Form(...),  # Assuming date is provided as a string in the format 'YYYY-MM-DD'
    timeIn: str = Form(...),  # Add timeIn parameter
    timeOut: str = Form(...),  # Add timeOut parameter
    status: str = Form('Pending'),
    db=Depends(get_db)
):
    # Insert the guest record into the database if it doesn't exist
    guest_query = "INSERT IGNORE INTO guests (FirstName, LastName) VALUES (%s, %s)"
    db[0].execute(guest_query, (Firstname, Lastname))
    
    # Retrieve the GuestID of the guest or the existing GuestID if the guest already exists
    guest_id_query = "SELECT GuestID FROM guests WHERE FirstName = %s AND LastName = %s"
    db[0].execute(guest_id_query, (Firstname, Lastname))
    result = db[0].fetchone()
    if result:
        guest_id = result[0]
    else:
        # Handle the case where the guest doesn't exist
        # You can raise an exception or return an error message
        return {"error": "Guest does not exist"}

    # Insert the bookings record into the database
    booking_query = "INSERT INTO bookings (GuestID, DateIn, TimeIn, TimeOut, Purpose, Status) VALUES (%s, %s, %s, %s, %s, %s)"
    db[0].execute(booking_query, (guest_id, daterequested, timeIn, timeOut, purpose, status))
    
    # Commit the transaction
    db[1].commit()
    
    # Close cursor and connection
    db[0].close()
    db[1].close()

    return {
        "requestid": guest_id,
        "Firstname": Firstname,
        "Lastname": Lastname,
        "purpose": purpose,
        "daterequested": daterequested,
        "timeIn": timeIn,
        "timeOut": timeOut,
        "status": status
    }




@BookingRouter.put("/bookings/{requestid}", response_model=dict)
async def update_bookings(
    Firstname: str = Form(...),
    Lastname: str = Form(...),
    purpose: str = Form(...),
    daterequested: str = Form(...),  # Assuming date is provided as a string in the format 'YYYY-MM-DD'
    status: str = Form('Pending'),
    
    db=Depends(get_db)
):
    # Hash the password using bcrypt

    # Update user information in the database 
    query = "UPDATE bookings SET Firstname= %s, Lastname = %s, purpose = %s, daterequested = %s, status = %s WHERE requestid = %s"
    db[0].execute(query, ( Firstname,Lastname, purpose,daterequested,status ))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        # Close cursor and connection
        db[0].close()
        db[1].close()
        return {"message": "bookings updated successfully"}
    
    # If no rows were affected, user not found
    raise HTTPException(status_code=404, detail="bookings not found")

@BookingRouter.delete("/bookings/{requestid}", response_model=dict)
async def delete_bookings(
    requestid: int,
    db=Depends(get_db)
):
    try:
        # Check if the user exists
        query_check_user = "SELECT requestid FROM bookings WHERE requestid = %s"
        db[0].execute(query_check_user, (requestid,))
        existing_user = db[0].fetchone()

        if not existing_user:
            raise HTTPException(status_code=404, detail="bookings not found")

        # Delete the user
        query_delete_user = "DELETE FROM bookings WHERE requestid = %s"
        db[0].execute(query_delete_user, (requestid,))
        db[1].commit()
        
        # Close cursor and connection
        db[0].close()
        db[1].close()

        return {"message": "bookings deleted successfully"}
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor
        db[0].close()
