import datetime
import logging
from typing import List, Tuple

from fastapi import status, HTTPException
from sqlalchemy import func, desc
from sqlalchemy.orm import Session

from app.models import Restaurant, Employee, Menu, Vote
from app.schemas.employee import BaseEmployeeSchema
from app.schemas.menu import BaseMenuSchema
from app.schemas.restaurant import BaseRestaurantSchema
from app.schemas.vote import BaseVoteSchema
from app.settings import settings
from app.utils import get_midnight_today, is_valid_id

logger = logging.getLogger(__name__)
logger.setLevel(settings.log_level)


def create_new_restaurant(db: Session, restaurant: BaseRestaurantSchema) -> Restaurant:
    new_restaurant = Restaurant(**restaurant.dict())

    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)

    return new_restaurant


def create_new_employee(db: Session, employee: BaseEmployeeSchema) -> Employee:
    new_employee = Employee(**employee.dict())

    # Employee must be associated with a restaurant
    valid_restaurant = is_valid_id(db, new_employee.restaurant_id, Restaurant)
    if not valid_restaurant:
        # log error and raise exception
        logger.info('Invalid Restaurant ID', extra=dict(
            type='invalid_id',
        ))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Restaurant ID')

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


def create_new_menu(db: Session, menu: BaseMenuSchema) -> Menu:
    new_menu = Menu(**menu.dict())

    # Menu must be associated with a restaurant
    valid_restaurant = is_valid_id(db, new_menu.restaurant_id, Restaurant)
    if not valid_restaurant:
        # log error and raise exception
        logger.info('Invalid Restaurant ID', extra=dict(
            type='invalid_id',
        ))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Restaurant ID')

    # A restaurant should submit one menu per day
    yesterday = get_midnight_today() - datetime.timedelta(days=1)
    previous_menu_today = db.query(Menu).filter(Menu.created_at > yesterday).first()
    previous_menu_by_restaurant = db.query(Menu).filter(
        new_menu.restaurant_id == Menu.restaurant_id).first() if previous_menu_today else None

    if previous_menu_by_restaurant:
        # log error and raise exception
        logger.info('Menu already submitted today, daily limit reached', extra=dict(
            type='menu_already_submitted',
        ))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Menu already submitted today, daily limit reached')

    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)

    return new_menu


def create_new_vote(db: Session, vote: BaseVoteSchema) -> Vote:
    new_vote = Vote(**vote.dict())

    # Vote must be associated with an employee and a menu
    valid_employee = is_valid_id(db, new_vote.employee_id, Employee)
    valid_menu = is_valid_id(db, new_vote.menu_one_id, Menu)
    if not valid_employee or not valid_menu:
        logger.info('Invalid Employee ID or Menu ID', extra=dict(
            type='invalid_id',
        ))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Employee ID or Menu ID')

    # An employee should submit one vote per day
    yesterday = get_midnight_today() - datetime.timedelta(days=1)
    previous_votes_today = db.query(Vote).filter(Vote.created_at > yesterday).first()
    previous_vote_by_employee = db.query(Vote).filter(
        new_vote.employee_id == Vote.employee_id).first() if previous_votes_today else None

    if previous_vote_by_employee:
        logger.info('Employee already voted today, daily limit reached', extra=dict(
            type='employee_already_voted',
        ))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Employee already voted today, daily limit reached')

    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)

    return new_vote


def get_daily_result(db: Session) -> List[Tuple]:
    # Get results for today
    yesterday = get_midnight_today() - datetime.timedelta(days=1)

    query = db.query(Vote.menu_one_id.label('menu_id'), func.count(Vote.id).label('votes'))
    previous_votes_today_query = query.filter(Vote.created_at > yesterday)
    result = previous_votes_today_query.group_by(Vote.menu_one_id).order_by(desc('votes')).all()
    return result
