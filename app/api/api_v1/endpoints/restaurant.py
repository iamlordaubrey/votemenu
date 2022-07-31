from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.restaurant import RetrieveRestaurantSchema, BaseRestaurantSchema
from app.services.crud_db import create_new_restaurant

router = APIRouter()


@router.post('', status_code=201, response_model=RetrieveRestaurantSchema, summary='Creates a restaurant')
async def create_restaurant(restaurant: BaseRestaurantSchema, db: Session = Depends(get_db)):
    restaurant = create_new_restaurant(db=db, restaurant=restaurant)
    return jsonable_encoder(restaurant)
