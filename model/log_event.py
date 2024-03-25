# model/users.py
from fastapi import Depends, HTTPException, APIRouter, Form, Path
from .db import get_db
import bcrypt

LogsRouter = APIRouter(tags=["Log Event"])

# CRUD operations

@LogsRouter.get("/log_event/", response_model=list)
async def read_log(
    db=Depends(get_db)
):
    query = "SELECT log_id, teacher_id,lab_id, timestamp,activity FROM log_event"
    db[0].execute(query)
    log_event = [{"log_id": log_event[0], "teacher_id": log_event[1], "lab_id": log_event[2],"timestamp": log_event[3], "activity": log_event[4] } for log_event in db[0].fetchall()]
    return log_event

@LogsRouter.get("/log_event/{log_id}", response_model=dict)
async def read_log(
    log_id: int, 
    db=Depends(get_db)
):
    query = "SELECT log_id, teacher_id, lab_id, timestamp, activity FROM log_event WHERE log_id = %s"
    db[0].execute(query, (log_id,))
    log_event = db[0].fetchone()
    if log_event:
        return {"log_id": log_event[0], "teacher_id": log_event[1], "lab_id": log_event[2], "timestamp": log_event[3], "activity": log_event[4]}
    raise HTTPException(status_code=404, detail="Logs not found")

@LogsRouter.post("/log_event/{log_id}", response_model=dict)
async def create_log(
    log_id: int = Path(...), 
    teacher_id: int = Form(...), 
    lab_id: int = Form(...),
    timestamp: str = Form(...), 
    activity: str = Form(...),  
    db=Depends(get_db)
):
    # Hash the password using bcrypt
    

    query = "INSERT INTO log_event (log_id,teacher_id,lab_id,timestamp,activity) VALUES (%s, %s, %s, %s, %s)"
    db[0].execute(query, (log_id,teacher_id,lab_id,timestamp,activity))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute(" SELECT MAX(log_id) FROM log_event")
    new_user_id = db[0].fetchone()[0]
    db[1].commit()

    return {"id": new_user_id, "log_id": log_id,"teacher_id":teacher_id,"lab_id":lab_id, "timestamp": timestamp, "activity": activity}

@LogsRouter.put("/log_event/{log_id}", response_model=dict)
async def update_log(
    
    log_id: int = Path(...), 
    teacher_id: int = Form(...), 
    lab_id: int = Form(...),
    timestamp: str = Form(...), 
    activity: str = Form(...), 
    db=Depends(get_db)
):
    # Hash the password using bcrypt
    

    # Update user information in the database 
    query = "UPDATE log_event SET log_id = %s, teacher_id = %s, lab_id = %s, timestamp = %s, activity = %s WHERE log_id = %s"
    db[0].execute(query, (log_id,teacher_id,lab_id,timestamp,activity))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "Logs updated successfully"}
    
    # If no rows were affected, user not found
    raise HTTPException(status_code=404, detail="Logs not found")

@LogsRouter.delete("/log_event/{log_id}", response_model=dict)
async def delete_logs(
    log_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the user exists
        query_check_user = "SELECT log_id FROM log_event WHERE log_id = %s"
        db[0].execute(query_check_user, (log_id,))
        existing_user = db[0].fetchone()

        if not existing_user:
            raise HTTPException(status_code=404, detail="Logs not found")

        # Delete the user
        query_delete_user = "DELETE FROM log_event WHERE log_id = %s"
        db[0].execute(query_delete_user, (log_id,))
        db[1].commit()

        return {"message": "Logs deleted successfully"}
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
