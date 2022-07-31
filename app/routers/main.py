from pathlib import Path

from fastapi import APIRouter, Request, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Restaurant, Employee, Menu
from app.schemas.menu import BaseMenuSchema, RetrieveMenuSchema
from app.schemas.restaurant import BaseRestaurantSchema, RetrieveRestaurantSchema
from app.schemas.employee import BaseEmployeeSchema, RetrieveEmployeeSchema
from app.services.crud_db import create_new_restaurant, create_new_employee, create_new_menu
from app.settings import settings

router = APIRouter()
templates = Jinja2Templates(directory=Path(settings.root_dir, 'templates'))


@router.get('/', response_class=HTMLResponse)
async def index(request: Request):
    """
    Display the input field and submit button
    :param request: N/A
    :return: Renders a page
    """
    return templates.TemplateResponse('index.html', {'request': request})


@router.post('/restaurant', response_model=RetrieveRestaurantSchema, summary='Creates a restaurant')
async def create_restaurant(restaurant: BaseRestaurantSchema, db: Session = Depends(get_db)):
    restaurant = create_new_restaurant(db=db, restaurant=restaurant)
    return jsonable_encoder(restaurant)


@router.post('/employee', response_model=RetrieveEmployeeSchema, summary='Creates an employee')
async def create_employee(employee: BaseEmployeeSchema, db: Session = Depends(get_db)):
    employee = create_new_employee(db=db, employee=employee)
    return jsonable_encoder(employee)


@router.post('/menu', response_model=RetrieveMenuSchema, summary='Creates a menu')
async def create_menu(menu: BaseMenuSchema, db: Session = Depends(get_db)):
    menu = create_new_menu(db=db, menu=menu)
    return jsonable_encoder(menu)
