import datetime

WEEK_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
             'Saturday', 'Sunday']
CURRENT_YEAR = datetime.date.today().year


def get_date_stub():
    # today_date = datetime.date.today() - datetime.timedelta(days=13)
    today_date = datetime.datetime(2021, 1, 11)
    # x = datetime.datetime.now()
    # x2 = datetime.date.today()
    # x3 = x2 - datetime.timedelta(days=30)
    # print(x3)
    return today_date


def get_today_date():
    return datetime.date.today()


def get_month_name_from_date(date: datetime.date):
    return date.strftime("%B")