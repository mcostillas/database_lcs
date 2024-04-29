# model/users.py
from fastapi import Depends, HTTPException, APIRouter, Form, Path
from .db import get_db



LaboratoryRouter = APIRouter(tags=["Laboratory"])

# CRUD operations

@LaboratoryRouter.get("/labstatus/", response_model=list)
async def read_labstatus(
    db=Depends(get_db)
):
    query = "SELECT labstatusid, labname,occupied,lastupdated  FROM labstatus"
    db[0].execute(query)
    labstatus = [{"labstatusid": labstatus[0], "labname": labstatus[1], "occupied": labstatus[2], "lastupdated": labstatus[3]} for labstatus in db[0].fetchall()]
    return labstatus

@LaboratoryRouter.get("/labstatus/{labstatusid}", response_model=dict)
async def read_labstatus(
    labstatusid: int, 
    db=Depends(get_db)
):
    query = "SELECT labstatusid,labname,occupied,lastupdated FROM labstatus WHERE labstatusid = %s"
    db[0].execute(query, (labstatusid,))
    labstatus= db[0].fetchone()
    if  labstatus:
        return {"labstatusid": labstatus[0], "labname": labstatus[1], "occupied": labstatus[2], "lastupdated": labstatus[3]}
    raise HTTPException(status_code=404, detail="labstatus not found")

@LaboratoryRouter.post("/labstatus/{labstatusid}", response_model=dict)
async def create_lab(
    labname: str = Form(...), 
    db=Depends(get_db)
):
    # Hash the password using bcrypt
    

    query = "INSERT INTO labstatus (labname) VALUES (%s)"
    db[0].execute(query, (labname))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute(" SELECT MAX(labstatusid)  FROM labstatus")
    new_user_id = db[0].fetchone()[0]
    db[1].commit()

    return {"id": new_user_id,"labname": labname}

@LaboratoryRouter.put("/labstatus/{labstatusid}", response_model=dict)
async def update_labstatus(
    labname: int = Form(...), 
    occupied: int = Form(...),
    db=Depends(get_db)
):
    # Hash the password using bcrypt
  

    # Update user information in the database 
    query = "UPDATE labstatus SET labname = %s , occupied = %s WHERE labstatusid = %s"
    db[0].execute(query, (labname, occupied ))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "labstatus updated successfully"}
    
    # If no rows were affected, user not found
    raise HTTPException(status_code=404, detail="labstatus not found")

@LaboratoryRouter.delete("/labstatus/{labstatusid}", response_model=dict)
async def delete_labstatus(
    labstatusid: int,
    db=Depends(get_db)
):
    try:
        # Check if the user exists
        query_check_user = "SELECT labstatusid FROM labstatus WHERE labstatusid = %s"
        db[0].execute(query_check_user, (labstatusid,))
        existing_user = db[0].fetchone()

        if not existing_user:
            raise HTTPException(status_code=404, detail="labstatus not found")

        # Delete the user
        query_delete_user = "DELETE FROM labstatus WHERE labstatusid = %s"
        db[0].execute(query_delete_user, (labstatusid,))
        db[1].commit()

        return {"message": "labstatus deleted successfully"}
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
