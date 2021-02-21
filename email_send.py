import pandas as pd

from date_utils import WEEK_DAYS

EMAIL_BEGINNING = "HI,\n\n" \
                  "According to the agreeement, You will be part of the 24/7 " \
                  "Support Team during next week.\n"


def get_service_days(engineer_name: str,
                     next_week_engineers_schedule_df: pd.DataFrame):
    service_days_string = ""
    engineer_schedule_series = next_week_engineers_schedule_df.loc[engineer_name, :]
    # print(engineer_schedule_series)
    service_date_list = []
    for i, v in engineer_schedule_series.items():
        # print('index: ', i, 'value: ', v)
        if v == 'x':
            service_date_list.append(WEEK_DAYS[i.to_pydatetime().weekday()])
    service_days_string = ", ".join(service_date_list)
    return service_days_string, len(service_date_list)


def send_notifications(next_week_engineers_schedule_df: pd.DataFrame,
                       next_week_moc_schedule_df: pd.DataFrame,
                       next_week_engineers_df: pd.DataFrame,
                       next_week_moc_df: pd.DataFrame):
    print(EMAIL_BEGINNING)

    for index, engineer_row in next_week_engineers_df.iterrows():
        target_email = engineer_row['E-mail']
        print(target_email)
        engineer_name = engineer_row['Name']
        service_days, num_of_service_days = get_service_days(engineer_name,
                                                             next_week_engineers_schedule_df)
        target_message = EMAIL_BEGINNING + "Your service days are: " + \
                         service_days + "\n"
        target_message += "Total number of days: " + str(num_of_service_days)
        # print(service_days)
        print(target_message)
    pass
