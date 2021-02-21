import datetime

WEEK_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
             'Saturday', 'Sunday']
CURRENT_YEAR = datetime.date.today().year


def get_date_stub(year, month, day):
    current_date = datetime.datetime(year, month, day)
    return current_date


def get_today_date():
    return datetime.date.today()


def get_month_name_from_date(date: datetime.date):
    return date.strftime("%B")
