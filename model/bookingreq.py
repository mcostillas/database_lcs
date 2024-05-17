from datetime import date,time
from fastapi import Depends, HTTPException, APIRouter, Form, Path, Body
from .db import get_db
from typing import List

import bcrypt

BookingRouter = APIRouter(tags=["Booking Requests"])

# CRUD operations

@BookingRouter.get("/bookings/", response_model=list)
async def read_bookings(
    db=Depends(get_db)
):
    query = "SELECT CONCAT(g.FirstName, ' ', g.LastName) AS FullName, b.Purpose, b.CreatedAt, b.TimeIn, b.TimeOut, b.bookingid , b.dateIN,  b.Guestid FROM bookings b INNER JOIN guests g ON b.GuestID = g.GuestID"
    db[0].execute(query)
    bookings = [{"Full name": bookings[0], "Purpose": bookings[1], "Created AT": bookings[2], "TimeIN": bookings[3], "TimeOut": bookings[4], "bookingid": bookings[5], "dateIN": bookings[6], "Guestid": bookings[7]} for bookings in db[0].fetchall()]
    # Close cursor
    db[0].close()
    return bookings


@BookingRouter.get("/bookings/history", response_model=List[dict])
async def get_history(db=Depends(get_db)):
    # Perform a JOIN operation between history and adminprofile tables
    query = "SELECT  history.Date, history.FullName, history.Purpose, history.Action, adminprofile.FullName AS AdminFullName FROM history JOIN adminprofile ON history.UserID = adminprofile.UserID "
    db[0].execute(query)
    history_records = db[0].fetchall()

    # Prepare a list of dictionaries to return the result
    result = []
    for record in history_records:
        result.append({
            "Date": record[0],
            "FullName": record[1],
            "Purpose": record[2],
            "Action": record[3],
            "AdminFullName": record[4]
        })

    return result


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

@BookingRouter.delete("/bookings/{bookingid}", response_model=dict)
async def delete_bookings(
    bookingid: int,
    db=Depends(get_db)
):
    try:
        # Check if the booking exists
        query_check_booking = "SELECT guestid FROM bookings WHERE bookingid = %s"
        db[0].execute(query_check_booking, (bookingid,))
        booking = db[0].fetchone()

        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")

        guestid = booking[0]  # Assuming guestid is the first column in the result

        # Delete the booking
        query_delete_booking = "DELETE FROM bookings WHERE bookingid = %s"
        db[0].execute(query_delete_booking, (bookingid,))

        # Delete the guest
        query_delete_guest = "DELETE FROM guests WHERE guestid = %s"
        db[0].execute(query_delete_guest, (guestid,))

        db[1].commit()
        
        return {"message": "Booking and related guest deleted successfully"}
    except HTTPException as e:
        # Raise HTTPException as it is
        raise e
    except Exception as e:
        # Handle other exceptions if necessary
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        # Close the database cursor and connection
        try:
            db[0].close()
        except:
            pass
        try:
            db[1].close()
        except:
            pass
       

