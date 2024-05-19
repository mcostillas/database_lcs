# main.py

from fastapi import FastAPI
from model.acadcoordinator import AcadcoordinatorRouter
from model.user import UserRouter
from model.bookingreq import BookingRouter
from model.laboratory import LaboratoryRouter
from model.log_event import LogsRouter
from model.schedule import ScheduleRouter
from model.teacher import TeacherRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173"
] 

# Include CRUD routes from modules
app.include_router(AcadcoordinatorRouter, prefix="/api")
app.include_router(UserRouter, prefix="/api")
app.include_router(BookingRouter, prefix="/api")
app.include_router(LaboratoryRouter, prefix="/api")
app.include_router(LogsRouter, prefix="/api")
app.include_router(ScheduleRouter, prefix="/api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)   




