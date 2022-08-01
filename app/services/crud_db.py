import datetime
from uuid import UUID

from sqlalchemy import func, desc
from sqlalchemy.orm import Session

from app.models import Restaurant, Employee, Menu, Vote
from app.utils import get_midnight_today


def create_new_restaurant(db: Session, restaurant):
    new_restaurant = Restaurant(**restaurant.dict())

    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)

    return new_restaurant


def create_new_employee(db: Session, employee):
    new_employee = Employee(**employee.dict())

    # Employee must be associated with a restaurant
    valid_restaurant = get_restaurant_by_id(db, new_employee.restaurant_id)
    if not valid_restaurant:
        # throw an error
        print('an error occurred')
        return

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


def create_new_menu(db: Session, menu):
    new_menu = Menu(**menu.dict())

    # Menu must be associated with a restaurant
    valid_restaurant = get_restaurant_by_id(db, new_menu.restaurant_id)
    if not valid_restaurant:
        print('an error occurred')
        return

    # Submit one menu per day
    yesterday = get_midnight_today() - datetime.timedelta(days=1)
    previous_menu_today = db.query(Menu).filter(Menu.created_at > yesterday).first()
    if previous_menu_today:
        print('Menu already submitted today')
        return

    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)

    return new_menu


def create_new_vote(db: Session, vote):
    new_vote = Vote(**vote.dict())

    # Vote must be associated with an employee and a menu
    valid_employee = get_employee_by_id(db, new_vote.employee_id)
    valid_menu = get_menu_by_id(db, new_vote.menu_one_id)
    if not valid_employee or not valid_menu:
        print('Invalid Employee or Menu')
        return

    # Submit one vote per employee per day
    yesterday = get_midnight_today() - datetime.timedelta(days=1)
    previous_votes_today = db.query(Vote).filter(Vote.created_at > yesterday).first()
    previous_vote_by_employee = db.query(Vote).filter(
        new_vote.employee_id == previous_votes_today.employee_id) if previous_votes_today else None

    if previous_vote_by_employee:
        print('Employee already voted today')
        return

    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)

    return new_vote


def get_daily_result(db: Session):
    # Get results for today
    yesterday = get_midnight_today() - datetime.timedelta(days=1)

    query = db.query(Vote.menu_one_id, func.count(Vote.id).label('votes'))
    previous_votes_today_query = query.filter(Vote.created_at > yesterday)
    result = previous_votes_today_query.group_by(Vote.menu_one_id).order_by(desc('votes')).all()
    return result


def get_menu_for_date(db: Session, date_obj: datetime.datetime):
    end_of_day = datetime.datetime.combine(date_obj, datetime.time.max)

    menu_today = db.query(Menu).filter(Menu.created_at >= date_obj, Menu.created_at <= end_of_day).all()
    return menu_today


def get_restaurant_by_id(db: Session, restaurant_id: UUID):
    return db.query(Restaurant).filter(restaurant_id == Restaurant.id).first()


def get_employee_by_id(db: Session, employee_id: UUID):
    return db.query(Employee).filter(employee_id == Employee.id).first()


def get_menu_by_id(db: Session, menu_id: UUID):
    return db.query(Menu).filter(menu_id == Menu.id).first()
