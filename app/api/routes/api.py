from fastapi import APIRouter
from app.api.routes import (tasks) 

router = APIRouter()
# router.include_router(tasks.router, tags=['tasks'], prefix="/tasks")
router.include_router(tasks.router, tags=['tasks'])







