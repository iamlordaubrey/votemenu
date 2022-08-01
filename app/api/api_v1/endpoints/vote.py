from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.auth.jwt import get_current_user
from app.database import get_db
from app.models import User
from app.schemas.vote import BaseVoteSchema, RetrieveVoteSchema
from app.services.crud_db import create_new_vote, get_daily_result

router = APIRouter()


@router.post('', status_code=201, response_model=RetrieveVoteSchema, summary='Creates a vote')
async def create_vote(
        vote: BaseVoteSchema, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    employee = create_new_vote(db=db, vote=vote)
    return jsonable_encoder(employee)


@router.get('/result', status_code=200, summary='Retrieves the current day\'s result')
async def get_result(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = get_daily_result(db=db)
    return jsonable_encoder(result)
