import datetime
import pandas as pd
import numpy as np

from data_import import import_data
from date_utils import WEEK_DAYS, get_date_stub, get_month_name_from_date
from email_send import send_notifications

NOTIFICATION_WEEK_DAY = 'Monday'


def get_next_week_engineers_schedule_df(current_date: datetime.date,
                                        engineer_calendar_df: pd.DataFrame):
    next_week_date = current_date + datetime.timedelta(7)
    next_week_engineer_lists = [
        engineer_calendar_df[get_month_name_from_date(next_week_date +
                                                      datetime.timedelta(i)),
                             (next_week_date + datetime.timedelta(i)).day] for
        i in range(0, 7)]
    next_week_engineer_headers = [(next_week_date + datetime.timedelta(i)) for i
                                  in range(0, 7)]
    next_week_engineer_schedule_df = pd.DataFrame(
        np.column_stack([next_week_engineer_lists]).T,
        columns=next_week_engineer_headers,
        index=engineer_calendar_df.index).dropna(axis=0, how="all")
    return next_week_engineer_schedule_df


def get_next_week_moc_schedule_df(current_date: datetime.date,
                                  moc_calendar_df: pd.DataFrame):
    next_week_date = current_date + datetime.timedelta(7)
    next_week_moc_lists = [
        moc_calendar_df[get_month_name_from_date(next_week_date +
                                                 datetime.timedelta(i)),
                        (next_week_date + datetime.timedelta(i)).day] for
        i in range(0, 7)]
    next_week_moc_headers = [(next_week_date + datetime.timedelta(i)) for i
                             in range(0, 7)]
    next_week_moc_schedule_df = pd.DataFrame(
        np.column_stack([next_week_moc_lists]).T,
        columns=next_week_moc_headers,
        index=moc_calendar_df.index).dropna()
    return next_week_moc_schedule_df


def get_next_week_moc_name(next_week_moc_df: pd.DataFrame):
    next_week_moc_name = None
    moc_list = [moc for moc in next_week_moc_df.index]
    if len(moc_list) != 1:
        print("Next week MoC list is not 1! Actual value:", len(moc_list))
        exit(1)
    else:
        next_week_moc_name = moc_list[0]
    return next_week_moc_name


def get_next_week_engineers_and_moc(next_week_engineers_schedule_df: pd.DataFrame,
                                    next_week_moc_schedule_df: pd.DataFrame):
    next_week_engineer_name_list = [engineer for engineer in
                                    next_week_engineers_schedule_df.index]
    next_week_moc_name = get_next_week_moc_name(next_week_moc_schedule_df)
    next_week_engineers_df = engineer_df.loc[
        engineer_df['Name'].isin(next_week_engineer_name_list)]
    next_week_moc_schedule_df = moc_info_df[
        moc_info_df['Name'] == next_week_moc_name]
    return next_week_engineers_df, next_week_moc_schedule_df


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
