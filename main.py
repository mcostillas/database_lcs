# main.py
from fastapi import FastAPI
from model.users import UsersRouter
from model.acadcoordinator import AcadcoordinatorRouter
from model.admin import AdminRouter
from model.booking_activty import BookingRouter
from model.guest import GuestRouter
from model.laboratory import LaboratoryRouter
from model.log_event import LogsRouter
from model.schedule import ScheduleRouter
app = FastAPI()

# Include CRUD routes from modules
app.include_router(AcadcoordinatorRouter, prefix="/api")
app.include_router(AdminRouter, prefix="/api")
app.include_router(BookingRouter, prefix="/api")
app.include_router(GuestRouter, prefix="/api")
app.include_router(LaboratoryRouter, prefix="/api")
app.include_router(LogsRouter, prefix="/api")
app.include_router(ScheduleRouter, prefix="/api")


