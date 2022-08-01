import datetime
from zoneinfo import ZoneInfo
from uuid import UUID

from sqlalchemy.orm import Session

from app.constants import TIMEZONE
from app.database import Base
from app.models import Menu


def get_midnight_today() -> datetime.datetime:
    return datetime.datetime.combine(datetime.datetime.now(ZoneInfo(TIMEZONE)), datetime.time.min)


def get_menu_for_date(db: Session, date_obj: datetime.datetime):
    end_of_day = datetime.datetime.combine(date_obj, datetime.time.max)

    menu_today = db.query(Menu).filter(Menu.created_at >= date_obj, Menu.created_at <= end_of_day).all()
    return menu_today


def is_valid_id(db: Session, model_id: UUID, model: Base):
    return db.query(model).filter(model_id == model.id).first()
