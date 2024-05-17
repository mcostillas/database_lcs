# model/users.py
from fastapi import Depends, HTTPException, APIRouter, Form,Path,FastAPI
from sqlalchemy.orm import Session
import datetime
from .db import get_db
import bcrypt

ScheduleRouter = APIRouter(tags=["Schedule"])

# CRUD operations

@ScheduleRouter.get("/schedule/", response_model=list)
async def read_schedule(
    db=Depends(get_db)
):
    query = "SELECT scheduleid,guestid,dayofweek,timein,timeout,roomnumber,schedSemester,yearCourseandSection,participant,status FROM schedule"
    db[0].execute(query)
    schedule = [{"schedule_id": schedule[0], "guestid": schedule[1],"dayofweek":schedule[2],"timein":schedule[3],"timeout":schedule[4],"roomnumber":schedule[5],"schedSemester": schedule[6],"YearSection": schedule[7], "participant": schedule[8],"status": schedule[9]} for schedule in db[0].fetchall()]
    return schedule

@ScheduleRouter.get("/schedule/{roomnumber}", response_model=list)
async def read_schedule(
    roomnumber: int, 
    db=Depends(get_db)
):
    query = "SELECT scheduleid,guestid,dayofweek,timein,timeout,roomnumber,schedSemester,yearCourseandSection,participant,status FROM schedule WHERE roomnumber= %s"
    db[0].execute(query, (roomnumber,))
    schedules = db[0].fetchall()

    if schedules:
        return [
            {
                "schedule_id": schedule[0], 
                "guestid": schedule[1],
                "dayofweek": schedule[2],
                "timein": schedule[3],
                "timeout": schedule[4],
                "roomnumber": schedule[5],  
                "schedSemester": schedule[6],
                "YearSection": schedule[7],
                "participant": schedule[8],
                "status": schedule[9]
            }
            for schedule in schedules
        ]
    raise HTTPException(status_code=404, detail="Schedules not found for room number")




@ScheduleRouter.post("/schedule/acceptbook", response_model=dict)
async def create_schedule(
    guest_id: int = Form(...),
    day_of_week: str = Form(...),
    time_in: str = Form(...),
    time_out: str = Form(...),
    participant: str = Form(...),
    db: Session = Depends(get_db)
):
    # Insert the schedule record into the database
    schedule_query = "INSERT INTO schedule (GuestID, dayOfWeek, timeIn, timeOut, participant, roomNumber, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    db[0].execute(schedule_query, (
        guest_id, 
        day_of_week, 
        time_in, 
        time_out, 
        participant, 
        "some_room_number",  # Replace with actual room number if available
        "Pending"  # Assuming status is 'Pending' by default
    ))
    
    # Commit the transaction
    db[1].commit()

    return {
        "guest_id": guest_id,
        "day_of_week": day_of_week,
        "time_in": time_in,
        "time_out": time_out,
        "participant": participant,
        "status": "Pending"  # Assuming status is 'Pending' by default
    }


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

@ScheduleRouter.post("/history/add", response_model=dict)
async def add_history(
    guest_id: int = Form(...),
    user_id: int = Form(...),
    booking_id: int = Form(...),
    full_name: str = Form(...),
    purpose: str = Form(...),
    action: str = Form(...),
    db: Session = Depends(get_db)
):
    # Insert the history record into the database
    history_query = """
    INSERT INTO history (Date, UserID, GuestID, BookingID, FullName, Purpose, Action) 
    VALUES (CURDATE(), %s, %s, %s, %s, %s, %s)
    """

    db[0].execute(history_query, (
        user_id,
        guest_id,  # Assuming UserID is the same as guest_id; modify if different
        booking_id, 
        full_name, 
        purpose, 
        action
    ))

    # Commit the transaction
    db[1].commit()

    return {
        "guest_id": guest_id,
        "booking_id": booking_id,
        "full_name": full_name,
        "purpose": purpose,
        "action": action
    }


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
