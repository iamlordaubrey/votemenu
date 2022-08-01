from fastapi import APIRouter

from app.api.api_v2.endpoints import vote

api_router = APIRouter()
api_router.include_router(vote.router, prefix='/vote', tags=['Vote'])
