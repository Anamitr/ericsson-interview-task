import datetime
import pandas as pd
import subprocess

from unMergeExcelCell.unMergeExcelCell import unMergeExcelCell

print("Hello")

INPUT_EXCEL_FILE_PATH = './input/grafik.xls'
CONVERTED_EXCEL_FILE_PATH = './input/grafik_unmerged.xls'
INPUT_SHEET_NAME = 'Schedule'


def get_date_stub():
    today_date = datetime.date.today()
    # x = datetime.datetime.now()
    # x2 = datetime.date.today()
    # x3 = x2 - datetime.timedelta(days=30)
    # print(x3)
    return today_date


def load_moc_and_engineers_info(excel_file: pd.ExcelFile):
    print("Loading moc and engineers info")
    meta_info = excel_file.parse(INPUT_SHEET_NAME, header=4, usecols="A:C")
    meta_info.rename(columns={meta_info.columns[1]: "E-mail"}, inplace=True)

    moc_info_df = meta_info[meta_info['Name'].astype(str).str.startswith('MoC')]
    engineer_df = meta_info[meta_info['Name'].astype(str).str.startswith(
        'Engineer')]
    return moc_info_df, engineer_df


def load_moc_calendar(input_excel_file: pd.ExcelFile, num_of_moc: int):
    print("Loading MoC calendar")
    moc_calendar_df = input_excel_file.parse(INPUT_SHEET_NAME, header=[2, 3, 4],
                                             index_col=0)
    # Drop first two columns
    moc_calendar_df.drop(moc_calendar_df.columns[[0, 1]], axis=1, inplace=True)
    # Keep only MoC rows
    moc_calendar_df = moc_calendar_df[:num_of_moc]
    # Keep merged cells
    moc_calendar_df.index = pd.Series(moc_calendar_df.index).fillna(
        method='ffill', axis=0)

    return moc_calendar_df


def import_data():
    input_excel_file = pd.ExcelFile(CONVERTED_EXCEL_FILE_PATH)
    moc_info_df, engineer_df = load_moc_and_engineers_info(input_excel_file)
    moc_calendar_df = load_moc_calendar(input_excel_file, len(moc_info_df))
    return moc_info_df, engineer_df, moc_calendar_df


def unmerge_excel_input_file():
    print("Unmerging excel input file")
    # Convert to xls
    subprocess.call("libreoffice --convert-to xls ./input/grafik.xlsx", shell=True)
    subprocess.call("mv grafik.xls ./input/grafik.xls", shell=True)
    # Unmerge cells
    unMergeExcelCell(INPUT_EXCEL_FILE_PATH)
    pass


# get_date_stub()
# unmerge_excel_input_file()
moc_info_df, engineer_df, moc_calendar_df = import_data()
