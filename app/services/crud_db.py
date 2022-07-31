from uuid import UUID

from sqlalchemy.orm import Session

from app.models import Restaurant


def create_new_restaurant(db: Session, restaurant, db_model):
    new_restaurant = db_model(**restaurant.dict())

    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)

    return new_restaurant


def create_new_employee(db: Session, employee, db_model):
    new_employee = db_model(**employee.dict())
    restaurant = get_restaurant_by_id(db, new_employee.restaurant_id)

    if not restaurant:
        # throw an error
        print('an error occurred')
        return

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


def create_new_menu(db: Session, menu, db_model):
    new_menu = db_model(**menu.dict())
    menu = get_restaurant_by_id(db, new_menu.restaurant_id)

    if not menu:
        print('an error occurred')
        return

    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)

    return new_menu


def get_restaurant_by_id(db: Session, restaurant_id: UUID):
    return db.query(Restaurant).filter(restaurant_id == Restaurant.id).first()
