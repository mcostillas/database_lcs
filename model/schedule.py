# model/users.py
from fastapi import Depends, HTTPException, APIRouter, Form,Path
from .db import get_db
import bcrypt

ScheduleRouter = APIRouter(tags=["Schedule"])

# CRUD operations

@ScheduleRouter.get("/schedule/", response_model=list)
async def read_schedule(
    db=Depends(get_db)
):
    query = "SELECT scheduleid,userid,dayofweek,timein,timeout,roomnumber,participant,status FROM schedule"
    db[0].execute(query)
    schedule = [{"schedule_id": schedule[0], "userid": schedule[1],"dayofweek":schedule[2],"timein":schedule[3],"timeout":schedule[4],"roomnumber":schedule[5],"participant":schedule[6],"status":schedule[7]} for schedule in db[0].fetchall()]
    return schedule

@ScheduleRouter.get("/schedule/{schedule_id}", response_model=dict)
async def read_schedule(
    schedule_id: int, 
    db=Depends(get_db)
):
    query = "SELECT schedule_id, lab_id, teacher_id FROM schedule WHERE schedule_id = %s"
    db[0].execute(query, (schedule_id,))
    schedule = db[0].fetchone()
    if schedule:
        return {"schedule_id": schedule[0], "lab_id": schedule[1], "teacher_id": schedule[2]}
    raise HTTPException(status_code=404, detail="schedule not found")

@ScheduleRouter.post("/schedule/{schedule_id}", response_model=dict)
async def create_schedule(
    schedule_id: int = Path(...), 
    lab_id: int = Form(...), 
    teacher_id: int = Form(...), 
    db=Depends(get_db)
):
    # Hash the password using bcrypt
    

    query = "INSERT INTO schedule (schedule_id, lab_id, teacher_id) VALUES (%s, %s, %s)"
    db[0].execute(query, (schedule_id, lab_id, teacher_id))

    # Retrieve the last inserted ID using LAST_INSERT_ID()
    db[0].execute(" SELECT MAX(schedule_id) FROM schedule")
    new_user_id = db[0].fetchone()[0]
    db[1].commit()

    return {"schedule_id": new_user_id, "lab_id": lab_id, "teacher_id": teacher_id}

@ScheduleRouter.put("/schedule/{schedule_id}", response_model=dict)
async def update_schedule(
    
    schedule_id: int = Path(...),
    lab_id: int = Form(...),
    teacher_id: int = Form(...),
    db=Depends(get_db)
):
    # Hash the password using bcrypt
    
    # Update user information in the database 
    query = "UPDATE schedule SET schedule_id = %s, lab_id = %s, teacher_id = %s WHERE schedule_id = %s"
    db[0].execute(query, (schedule_id,lab_id,teacher_id))

    # Check if the update was successful
    if db[0].rowcount > 0:
        db[1].commit()
        return {"message": "schedule updated successfully"}
    
    # If no rows were affected, user not found
    raise HTTPException(status_code=404, detail="schedule not found")

@ScheduleRouter.delete("/schedule/{schedule_id}", response_model=dict)
async def delete_schedule(
    schedule_id: int,
    db=Depends(get_db)
):
    try:
        # Check if the user exists
        query_check_user = "SELECT schedule_id FROM schedule WHERE schedule_id = %s"
        db[0].execute(query_check_user, (schedule_id,))
        existing_user = db[0].fetchone()

        if not existing_user:
            raise HTTPException(status_code=404, detail="schedule not found")

        # Delete the user
        query_delete_user = "DELETE FROM schedule WHERE schedule_id = %s"
        db[0].execute(query_delete_user, (schedule_id,))
        db[1].commit()

        return {"message": "schedule deleted successfully"}
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
