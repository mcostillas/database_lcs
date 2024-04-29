# model/users.py
from datetime import date,time
from fastapi import Depends, HTTPException, APIRouter, Form, Path,Body
from .db import get_db

import bcrypt

BookingRouter = APIRouter(tags=["Booking Requests"])

# CRUD operations

@BookingRouter.get("/bookingrequests/", response_model=list)
async def read_bookingrequests(
    db=Depends(get_db)
):
    query = "SELECT requestid, userid ,Firstname, Lastname, purpose, daterequested,status FROM bookingrequests"
    db[0].execute(query)
    bookingrequests = [{"requestid": bookingrequests[0], "userid": bookingrequests[1], "Firstname": bookingrequests[2],"Lastname": bookingrequests[3],"purpose": bookingrequests[4],"daterequested": bookingrequests[5],"status": bookingrequests[6]} for bookingrequests in db[0].fetchall()]
    return bookingrequests

@BookingRouter.get("/bookingrequests/{requestid}", response_model=dict)
async def read_bookingrequests(
    requestid: int, 
    db=Depends(get_db)
):
    query = "SELECT  requestid, userid ,Firstname, Lastname, purpose, daterequested,status FROM bookingrequests WHERE requestid = %s"
    db[0].execute(query, (requestid,))
    bookingrequests = db[0].fetchone()
    if  bookingrequests:
        return {"requestid": bookingrequests[0], "userid": bookingrequests[1], "Firstname": bookingrequests[2],"Lastname": bookingrequests[3],"purpose": bookingrequests[4],"daterequested": bookingrequests[5],"status": bookingrequests[6]}
    raise HTTPException(status_code=404, detail="bookingrequests not found")

@BookingRouter.post("/bookingrequests/", response_model=dict)
async def create_bookingrequests(
    Firstname: str = Form(...),
    Lastname: str = Form(...),
    purpose: str = Form(...),
    daterequested: str = Form(...),  # Assuming date is provided as a string in the format 'YYYY-MM-DD'
    status: str = Form('Pending'),
    db=Depends(get_db)
):
    # Hash the password using bcrypt
   
    # Insert the bookingrequests record into the database
    query = "INSERT INTO bookingrequests (Firstname, Lastname, purpose, daterequested,status) VALUES (%s, %s, %s, %s, %s)"
    db[0].execute(query, (Firstname, Lastname, purpose, daterequested,status))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute("SELECT LAST_INSERT_ID()")
    new_requestid = db[0].fetchone()[0]
    db[1].commit()

    return {"requestid": new_requestid, "Firstname": Firstname, "Lastname": Lastname, "purpose":purpose, "daterequested":daterequested, "status": status}



@BookingRouter.put("/bookingrequests/{requestid}", response_model=dict)
async def update_bookingrequests(
    Firstname: str = Form(...),
    Lastname: str = Form(...),
    purpose: str = Form(...),
    daterequested: str = Form(...),  # Assuming date is provided as a string in the format 'YYYY-MM-DD'
    status: str = Form('Pending'),
    
    db=Depends(get_db)
):
    # Hash the password using bcrypt


    # Update user information in the database 
    query = "UPDATE bookingrequests SET Firstname= %s, Lastname = %s, purpose = %s, daterequested = %s, status = %s WHERE requestid = %s"
    db[0].execute(query, ( Firstname,Lastname, purpose,daterequested,status ))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "bookingrequests updated successfully"}
    
    # If no rows were affected, user not found
    raise HTTPException(status_code=404, detail="bookingrequests not found")

@BookingRouter.delete("/bookingrequests/{requestid}", response_model=dict)
async def delete_bookingrequests(
    requestid: int,
    db=Depends(get_db)
):
    try:
        # Check if the user exists
        query_check_user = "SELECT requestid FROM bookingrequests WHERE requestid = %s"
        db[0].execute(query_check_user, (requestid,))
        existing_user = db[0].fetchone()

        if not existing_user:
            raise HTTPException(status_code=404, detail="bookingrequests not found")

        # Delete the user
        query_delete_user = "DELETE FROM bookingrequests WHERE requestid = %s"
        db[0].execute(query_delete_user, (requestid,))
        db[1].commit()

        return {"message": "bookingrequests deleted successfully"}
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
