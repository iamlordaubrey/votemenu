from fastapi import APIRouter

from app.api.api_v1.endpoints import restaurant, employee, menu

api_router = APIRouter()
api_router.include_router(restaurant.router, prefix='/restaurant', tags=['restaurant'])
api_router.include_router(employee.router, prefix='/employee', tags=['employee'])
api_router.include_router(menu.router, prefix='/menu', tags=['menu'])
