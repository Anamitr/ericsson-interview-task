from data_import import import_data, unmerge_excel_input_file, \
    get_next_week_engineers_schedule_df, get_next_week_moc_schedule_df, \
    get_next_week_engineers_and_moc
from date_utils import WEEK_DAYS, get_date_stub
from email_send import send_notifications

NOTIFICATION_WEEK_DAY = 'Monday'

# get_date_stub()

# unmerge_excel_input_file()
print("--- 24/7 support - upcoming shift notifier ---")
# current_date = get_today_date()
current_date = get_date_stub()

print("Today is", WEEK_DAYS[current_date.weekday()])

if current_date.weekday() == WEEK_DAYS.index(NOTIFICATION_WEEK_DAY):
    print("Sending notifications")
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
                                    next_week_engineers_df, next_week_moc_df)


else:
    print("It's not a day for sending notification, which is", NOTIFICATION_WEEK_DAY)
