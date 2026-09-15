from datetime import datetime, date
from dateutil.relativedelta import relativedelta


def parse_date(date_str):
    if isinstance(date_str, date):
        return date_str
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def add_one_month(start_date):
    return start_date + relativedelta(months=1) - relativedelta(days=1)


def format_date(d):
    if d is None:
        return None
    if isinstance(d, str):
        return d
    return d.strftime("%Y-%m-%d")