# main.py
from fastapi import FastAPI
from model.users import UsersRouter
from model.acadcoordinator import AcadcoordinatorRouter
from model.admin import AdminRouter
from model.booking_activty import BookingRouter
app = FastAPI()

# Include CRUD routes from modules
app.include_router(AcadcoordinatorRouter, prefix="/api")
app.include_router(AdminRouter, prefix="/api")
app.include_router(BookingRouter, prefix="/api")


