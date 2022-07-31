import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.models import Restaurant, Employee, Menu
from app.utils import get_midnight_today


def create_new_restaurant(db: Session, restaurant):
    new_restaurant = Restaurant(**restaurant.dict())

    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)

    return new_restaurant


def create_new_employee(db: Session, employee):
    new_employee = Employee(**employee.dict())
    employee_restaurant = get_restaurant_by_id(db, new_employee.restaurant_id)

    if not employee_restaurant:
        # throw an error
        print('an error occurred')
        return

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


def create_new_menu(db: Session, menu):
    new_menu = Menu(**menu.dict())
    menu_restaurant = get_restaurant_by_id(db, new_menu.restaurant_id)

    if not menu_restaurant:
        print('an error occurred')
        return

    yesterday = get_midnight_today() - datetime.timedelta(days=1)
    previous_menu_today = db.query(Menu).filter(Menu.created_at > yesterday).first()
    print(previous_menu_today)
    if previous_menu_today:
        print('Menu already submitted today')
        return

    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)

    return new_menu


def get_menu_for_date(db: Session, date_obj: datetime.datetime):
    end_of_day = datetime.datetime.combine(date_obj, datetime.time.max)

    menu_today = db.query(Menu).filter(Menu.created_at >= date_obj, Menu.created_at <= end_of_day).all()
    return menu_today


def get_restaurant_by_id(db: Session, restaurant_id: UUID):
    return db.query(Restaurant).filter(restaurant_id >= Restaurant.id).first()
