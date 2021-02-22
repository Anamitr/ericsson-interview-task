import datetime
import subprocess
import sys

import numpy as np
import pandas as pd

from date_utils import get_month_name_from_date
from unMergeExcelCell.unMergeExcelCell import unMergeExcelCell

# from service_shift_notifier import engineer_df, moc_info_df

INPUT_EXCEL_FILE_PATH = './input/grafik.xls'
CONVERTED_EXCEL_FILE_PATH = './input/grafik_unmerged.xls'
INPUT_SHEET_NAME = 'Schedule'
HEADER_LENGTH = 3

engineer_df: pd.DataFrame
moc_info_df: pd.DataFrame


def import_data():
    global engineer_df, moc_info_df
    print("Importing data")
    input_excel_file = pd.ExcelFile(CONVERTED_EXCEL_FILE_PATH)
    moc_info_df, engineer_df, engineer_begin_index = load_moc_and_engineers_info(
        input_excel_file)
    moc_calendar_df = load_moc_calendar(input_excel_file, len(moc_info_df))
    engineer_calendar_df = load_engineer_calendar(input_excel_file,
                                                  engineer_begin_index)
    return moc_info_df, engineer_df, moc_calendar_df, engineer_calendar_df


def find_engineer_begin_index(data_df: pd.DataFrame):
    engineer_begin_index = None
    for index, row in data_df.iterrows():
        # print(row[0])
        if str(row[0]).startswith("Engineer"):
            engineer_begin_index = index
            break
    return engineer_begin_index


def load_moc_and_engineers_info(excel_file: pd.ExcelFile):
    print("Loading MoC and engineers info")
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
    moc_calendar_df = input_excel_file.parse(INPUT_SHEET_NAME, header=[2, 4],
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
    header_rows = [header_rows[0], header_rows[2], header_rows[1]]
    engineer_calendar_df = input_excel_file.parse(INPUT_SHEET_NAME,
                                                  header=[16, 18],
                                                  index_col=0)
    # Drop first two columns
    engineer_calendar_df.drop(engineer_calendar_df.columns[[0, 1]], axis=1,
                              inplace=True)
    # Delete additional rows
    engineer_calendar_df = engineer_calendar_df[
        engineer_calendar_df.index.astype(str).str.startswith(
            'Engineer')]
    return engineer_calendar_df


def unmerge_excel_input_file():
    print("Unmerging excel input file")
    # Convert to xls
    subprocess.call("libreoffice --convert-to xls ./input/grafik.xlsx", shell=True)
    subprocess.call("mv grafik.xls ./input/grafik.xls", shell=True)
    # Unmerge cells
    unMergeExcelCell(INPUT_EXCEL_FILE_PATH)
    pass


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
        sys.exit(-1)
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
