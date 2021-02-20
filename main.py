import datetime
import pandas as pd
import subprocess

from unMergeExcelCell.unMergeExcelCell import unMergeExcelCell

print("Hello")

INPUT_EXCEL_FILE_PATH = './input/grafik.xls'
CONVERTED_EXCEL_FILE_PATH = './input/grafik_unmerged.xls'
INPUT_SHEET_NAME = 'Schedule'
HEADER_LENGTH = 3


def get_date_stub():
    today_date = datetime.date.today()
    # x = datetime.datetime.now()
    # x2 = datetime.date.today()
    # x3 = x2 - datetime.timedelta(days=30)
    # print(x3)
    return today_date


def find_engineer_begin_index(data_df: pd.DataFrame):
    engineer_begin_index = None
    for index, row in data_df.iterrows():
        print(row[0])
        if str(row[0]).startswith("Engineer"):
            engineer_begin_index = index
            break
    return engineer_begin_index


def load_moc_and_engineers_info(excel_file: pd.ExcelFile):
    print("Loading moc and engineers info")
    meta_info = excel_file.parse(INPUT_SHEET_NAME, header=4, usecols="A:C")
    meta_info.rename(columns={meta_info.columns[1]: "E-mail"}, inplace=True)

    moc_info_df = meta_info[meta_info['Name'].astype(str).str.startswith('MoC')]
    engineer_df = meta_info[meta_info['Name'].astype(str).str.startswith(
        'Engineer')]
    engineer_begin_index = find_engineer_begin_index(excel_file.parse(
        INPUT_SHEET_NAME, usecols="A", header=None))
    print("Found engineer begin index at:", engineer_begin_index)
    return moc_info_df, engineer_df, engineer_begin_index


def load_moc_calendar(input_excel_file: pd.ExcelFile, num_of_moc: int):
    print("Loading MoC calendar")
    moc_calendar_df = input_excel_file.parse(INPUT_SHEET_NAME, header=[2, 3, 4],
                                             index_col=0)
    # Drop first two columns
    moc_calendar_df.drop(moc_calendar_df.columns[[0, 1]], axis=1, inplace=True)
    # Keep only MoC rows
    moc_calendar_df = moc_calendar_df[:num_of_moc]

    return moc_calendar_df


def load_engineer_calendar(input_excel_file: pd.ExcelFile,
                           engineer_begin_index: int):
    print("Loading Engineer calendar")
    header_rows = [engineer_begin_index - i for i in reversed(range(
        1, HEADER_LENGTH + 1))]
    engineer_calendar_df = input_excel_file.parse(INPUT_SHEET_NAME,
                                                  header=header_rows,
                                                  index_col=0)
    # Drop first two columns
    engineer_calendar_df.drop(engineer_calendar_df.columns[[0, 1]], axis=1,
                              inplace=True)
    # Delete additional rows
    engineer_calendar_df = engineer_calendar_df[
        engineer_calendar_df.index.astype(str).str.startswith(
            'Engineer')]
    return engineer_calendar_df


def import_data():
    print("Importing data")
    input_excel_file = pd.ExcelFile(CONVERTED_EXCEL_FILE_PATH)
    moc_info_df, engineer_df, engineer_begin_index = load_moc_and_engineers_info(
        input_excel_file)
    moc_calendar_df = load_moc_calendar(input_excel_file, len(moc_info_df))
    engineer_calendar_df = load_engineer_calendar(input_excel_file,
                                                  engineer_begin_index)
    return moc_info_df, engineer_df, moc_calendar_df, engineer_calendar_df


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
moc_info_df, engineer_df, moc_calendar_df, engineer_calendar_df = import_data()
