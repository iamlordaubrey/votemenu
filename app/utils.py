import datetime
from zoneinfo import ZoneInfo

from app.constants import TIMEZONE


def get_midnight_today() -> datetime.datetime:
    return datetime.datetime.combine(datetime.datetime.now(ZoneInfo(TIMEZONE)), datetime.time.min)
