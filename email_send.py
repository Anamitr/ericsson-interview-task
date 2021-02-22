import pandas as pd
import datetime

from date_utils import WEEK_DAYS
from email_model import EmailModel

EMAIL_TOPIC = "27/7 support - upcoming shift"
EMAIL_BEGINNING = "Hi,\n\n" \
                  "According to the agreeement, You will be part of the 24/7 " \
                  "Support Team during next week.\n"
# EMAIL_BEGINNING = ""
EMAIL_END = "\nBest regards,\nAdmin"


def send_notifications(next_week_engineers_schedule_df: pd.DataFrame,
                       next_week_moc_schedule_df: pd.DataFrame,
                       next_week_engineers_df: pd.DataFrame,
                       next_week_moc_df: pd.DataFrame,
                       current_date: datetime.date = None):
    next_week_moc_name = next_week_moc_df.reset_index().loc[0, "Name"]
    email_list = generate_emails(next_week_engineers_df,
                                 next_week_engineers_schedule_df,
                                 current_date, next_week_moc_name)
    for email in email_list:
        send_email_stub(email)
    return email_list


def generate_emails(next_week_engineers_df, next_week_engineers_schedule_df,
                    current_date: datetime.date = None, next_week_moc_name: str =
                    None):
    # next_week_engineers_schedule_csv = next_week_engineers_schedule_df.to_csv()
    email_list = []
    for index, engineer_row in next_week_engineers_df.iterrows():
        target_email = engineer_row['E-mail']
        # print(target_email)
        engineer_name = engineer_row['Name']
        service_days, num_of_service_days = get_service_days(engineer_name,
                                                             next_week_engineers_schedule_df)
        email_content = EMAIL_BEGINNING
        if current_date is not None:
            email_content += "Week starts " + (current_date + datetime.timedelta(7)) \
                .strftime("%d/%m/%Y") + "\n"
        email_content += "Your service days are: " + \
                         service_days + "\n"
        email_content += "Total number of days: " + str(num_of_service_days) + "\n"
        if next_week_moc_name is not None:
            email_content += next_week_moc_name + "\n"
        email_content += EMAIL_END
        # print(service_days)
        # print(email_content)
        email_list.append(EmailModel(target_email, EMAIL_TOPIC, email_content,
                                     attachment_list=[]))
    return email_list


def get_service_days(engineer_name: str,
                     next_week_engineers_schedule_df: pd.DataFrame):
    service_days_string = ""
    engineer_schedule_series = next_week_engineers_schedule_df.loc[engineer_name, :]
    # print(engineer_schedule_series)
    service_date_list = []
    for i, v in engineer_schedule_series.items():
        # print('index: ', i, 'value: ', v)
        if v == 'x':
            service_date_list.append(WEEK_DAYS[i.weekday()])
    service_days_string = ", ".join(service_date_list)
    return service_days_string, len(service_date_list)


def send_email_stub(email: EmailModel):
    print("Sending email to:", email.target_email)
    print("With topic:", email.email_topic)
    print("With content:\n", email.email_content, end="\n\n")
