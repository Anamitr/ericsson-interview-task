import pandas as pd

EMAIL_BEGINNING = "HI,\n\n" \
                  "According to the agreeement, You will be part of the 24/7 " \
                  "Support Team during next week.\n"


def get_service_days(engineer_name: str,
                     next_week_engineers_schedule_df: pd.DataFrame):
    service_days_string = ""
    engineer_schedule_df = next_week_engineers_schedule_df.loc[engineer_name, :]
    print(engineer_schedule_df)
    service_date_list = []



    return service_days_string


def send_notifications(next_week_engineers_schedule_df: pd.DataFrame,
                       next_week_moc_schedule_df: pd.DataFrame,
                       next_week_engineers_df: pd.DataFrame,
                       next_week_moc_df: pd.DataFrame):
    print(EMAIL_BEGINNING)

    for index, engineer_row in next_week_engineers_df.iterrows():
        target_email = engineer_row['E-mail']
        print(target_email)
        engineer_name = engineer_row['Name']
        service_days = get_service_days(engineer_name,
                                        next_week_engineers_schedule_df)
        target_message = EMAIL_BEGINNING + "Your service days are: " + service_days
    pass
