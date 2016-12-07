import logging
import datetime
from dateutil.parser import parse

logger = logging.getLogger(__name__)

DATE_FMT = "%Y-%m-%d %H:%M:%S"


def to_dates(f, t):
    try:
        _from = datetime.datetime.strptime(f, DATE_FMT)
    except Exception as e:
        logger.warn('Ошибка даты: {} ("{}")'.format(e, f))
        _from = datetime.datetime(year=2000, month=1, day=1)
    try:
        _to = datetime.datetime.strptime(t, DATE_FMT)
    except Exception as e:
        logger.warn('Ошибка даты: {} ("{}")'.format(e, t))
        _to = datetime.datetime.now()
    return (_from, _to)

def to_datetime(dt):
    try:
        dt = parse(dt)
    except Exception as e:
        logger.error('to_datetime: {} ("{}")'.format(e, et))
    return dt

