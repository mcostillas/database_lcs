# main.py
from fastapi import FastAPI
from model.acadcoordinator import AcadcoordinatorRouter
from model.admin import AdminRouter
from model.booking_activty import BookingRouter
from model.guest import GuestRouter
from model.laboratory import LaboratoryRouter
from model.log_event import LogsRouter
from model.schedule import ScheduleRouter
from model.teacher import TeacherRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
] 

# Include CRUD routes from modules
app.include_router(AcadcoordinatorRouter, prefix="/api")
app.include_router(AdminRouter, prefix="/api")
app.include_router(BookingRouter, prefix="/api")
app.include_router(GuestRouter, prefix="/api")
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




