# main.py
from fastapi import FastAPI
from model.users import UsersRouter
from model.categories import CategoriesRouter
from model.expenses import ExpensesRouter
from model.acadcoordinator import AcadcoordinatorRouter

app = FastAPI()

# Include CRUD routes from modules
app.include_router(AcadcoordinatorRouter, prefix="/api")

app.include_router(CategoriesRouter, prefix="/api")
app.include_router(ExpensesRouter, prefix="/api")