import datetime
from typing import List
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.constants import TIMEZONE
from app.database import get_db
from app.schemas.menu import RetrieveMenuSchema, BaseMenuSchema
from app.services.crud_db import create_new_menu, get_menu_for_date

router = APIRouter()


@router.post('', status_code=201, response_model=RetrieveMenuSchema, summary='Creates a menu')
async def create_menu(menu: BaseMenuSchema, db: Session = Depends(get_db)):
    menu = create_new_menu(db=db, menu=menu)
    return jsonable_encoder(menu)


@router.get('', response_model=List, summary='Returns all the menu for today')
async def get_menu(date: str = None, db: Session = Depends(get_db)):
    datetime_object = datetime.datetime.fromisoformat(date).replace(tzinfo=ZoneInfo(TIMEZONE))

    menu_today = get_menu_for_date(db=db, date_obj=datetime_object)
    return jsonable_encoder(menu_today)
