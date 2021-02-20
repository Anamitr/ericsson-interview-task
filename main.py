import datetime
import pandas as pd

print("Hello")

INPUT_SHEET_NAME = 'Schedule'


def get_date_stub():
    today_date = datetime.date.today()
    # x = datetime.datetime.now()
    # x2 = datetime.date.today()
    # x3 = x2 - datetime.timedelta(days=30)
    # print(x3)
    return today_date


def load_moc_and_engineers_info(excel_file: pd.ExcelFile):
    meta_info = excel_file.parse(INPUT_SHEET_NAME, header=4, usecols="A:C")
    meta_info.rename(columns={meta_info.columns[1]: "E-mail"}, inplace=True)

    moc_info_df = meta_info[meta_info['Name'].astype(str).str.startswith('MoC')]
    engineer_df = meta_info[meta_info['Name'].astype(str).str.startswith(
        'Engineer')]
    return moc_info_df, engineer_df


def import_data():
    input_excel_file = pd.ExcelFile('./input/grafik.xlsx')
    moc_info_df, engineer_df = load_moc_and_engineers_info(input_excel_file)
    return moc_info_df, engineer_df


get_date_stub()
moc_info_df, engineer_df = import_data()
