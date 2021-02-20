import datetime

from data_import import import_data

WEEK_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
             'Saturday', 'Sunday']
NOTIFICATION_WEEK_DAY = 'Monday'
CURRENT_YEAR = datetime.date.today().year


def get_date_stub():
    today_date = datetime.date.today() + datetime.timedelta(days=2)
    # x = datetime.datetime.now()
    # x2 = datetime.date.today()
    # x3 = x2 - datetime.timedelta(days=30)
    # print(x3)
    return today_date


def get_today_date():
    return datetime.date.today()


def get_month_name_from_date(date: datetime.date):
    return date.strftime("%B")


def send_notifications():
    pass
    moc_info_df, engineer_df, moc_calendar_df, engineer_calendar_df = import_data()


# get_date_stub()
# unmerge_excel_input_file()
print("--- 24/7 support - upcoming shift notifier ---")
# current_date = get_today_date()
current_date = get_date_stub()
print("Today is", WEEK_DAYS[current_date.weekday()])
if current_date.weekday() == WEEK_DAYS.index(NOTIFICATION_WEEK_DAY):
    print("Sending notifications")
    # send_notifications()
    moc_info_df, engineer_df, moc_calendar_df, engineer_calendar_df = import_data()
    # next_week_date = current_date + datetime.timedelta(7)
    current_month_name = get_month_name_from_date(current_date)
    ngineer_calendar_df[current_month_name, current_date.day]
else:
    print("It's not a day for sending notification, which is", NOTIFICATION_WEEK_DAY)
