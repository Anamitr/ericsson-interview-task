import sys, getopt
import datetime

from data_import import import_data, unmerge_excel_input_file, \
    get_next_week_engineers_schedule_df, get_next_week_moc_schedule_df, \
    get_next_week_engineers_and_moc
from date_utils import WEEK_DAYS, get_date_stub, get_today_date
from email_send import send_notifications

NOTIFICATION_WEEK_DAY = 'Monday'

full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]
short_options = "d:"
long_options = ["date-stub="]
try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
except getopt.error as err:
    print(str(err))
    sys.exit(2)

date_stub_string = None
current_date = None
for current_argument, current_value in arguments:
    if current_argument in ("-d", "--date-stub"):
        print("Setting date stub:", current_value)
        date_stub_string = current_value

if date_stub_string is not None:
    date_stub = datetime.datetime.strptime(date_stub_string, "%Y-%m-%d")
    print("Converted date stub:", date_stub)
    current_date = date_stub
else:
    current_date = get_today_date()

# unmerge_excel_input_file()
print("--- 24/7 support - upcoming shift notifier ---")

print("Today is", WEEK_DAYS[current_date.weekday()], current_date.strftime(
    "%Y-%m-%-d"))

if current_date.weekday() == WEEK_DAYS.index(NOTIFICATION_WEEK_DAY) or \
        NOTIFICATION_WEEK_DAY is None:
    print("Sending notifications")
    # sys.exit(0)
    moc_info_df, engineer_df, moc_calendar_df, engineer_calendar_df = import_data()
    next_week_engineers_schedule_df = get_next_week_engineers_schedule_df(
        current_date,
        engineer_calendar_df)
    next_week_moc_schedule_df = get_next_week_moc_schedule_df(current_date,
                                                              moc_calendar_df)

    next_week_engineers_df, next_week_moc_df = get_next_week_engineers_and_moc(
        next_week_engineers_schedule_df, next_week_moc_schedule_df)

    email_list = send_notifications(next_week_engineers_schedule_df,
                                    next_week_moc_schedule_df,
                                    next_week_engineers_df, next_week_moc_df,
                                    current_date)
else:
    print("It's not a day for sending notification, which is", NOTIFICATION_WEEK_DAY)
