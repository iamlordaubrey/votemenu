from fastapi import APIRouter

from app.api.api_v1.endpoints import restaurant, employee, menu, vote

api_router = APIRouter()
api_router.include_router(restaurant.router, prefix='/restaurant', tags=['Restaurant'])
api_router.include_router(employee.router, prefix='/employee', tags=['Employee'])
api_router.include_router(menu.router, prefix='/menu', tags=['Menu'])
api_router.include_router(vote.router, prefix='/vote', tags=['Vote'])
