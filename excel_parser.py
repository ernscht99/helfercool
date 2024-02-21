#!/usr/bin/env python3
import datetime as dt
from argparse import ArgumentParser
from os import listdir
from os.path import join

from pandas import DataFrame, concat, read_excel

col_names_24 = [
    "task",
    "subtask",
    "start_date",
    "start_time",
    "end_date",
    "end_time",
    "num_helpers",
    "num_intern_helpers",
    "num_helpers_total",
]

col_names = [
    "task",
    "subtask",
    "start_date",
    "start_time",
    "end_date",
    "end_time",
    "num_helpers",
]


def get_start_datetime(shifts):
    datetime = shifts["start_date"]
    if isinstance(shifts["start_time"], dt.time):
        datetime = datetime.replace(
            hour=shifts["start_time"].hour, minute=shifts["start_time"].minute
        )
    return datetime


def get_end_datetime(shifts):
    if isinstance(shifts["end_date"], dt.datetime):
        datetime = shifts["end_date"]
    else:
        # Assume that the time is supposed to refer to start_date
        datetime = shifts["start_date"]
    if isinstance(shifts["end_time"], dt.time):
        datetime = datetime.replace(
            hour=shifts["end_time"].hour, minute=shifts["end_time"].minute
        )
    return datetime


def is_xlsx(file_name: str):
    return file_name.endswith(".xlsx")


def parse_helper_form(xlsx_file: str, use_v24=False):
    if use_v24:
        shifts = read_excel(
            xlsx_file,
            skiprows=4,
            usecols="A:I",
            names=col_names_24,
        )
        # drop rows that are completely missshapen
        shifts = shifts.dropna(subset=["num_intern_helpers"])

        # convert helpers to int
        shifts = shifts.astype({"num_intern_helpers": "int"})

        # currently droped since irrelevant
        shifts = shifts.drop(["num_helpers_total"], axis=1)
    else:
        shifts = read_excel(
            xlsx_file,
            skiprows=4,
            usecols="A:G",
            names=col_names,
        )
    # drop rows that are completely missshapen
    shifts = shifts.dropna(subset=["num_helpers"])

    # convert helpers to int
    shifts = shifts.astype({"num_helpers": "int"})

    # replace empty subtasks with empty string
    shifts = shifts.fillna(value={"subtask": ""})

    # parse dates
    shifts["start_datetime"] = shifts.apply(get_start_datetime, axis=1)
    shifts["end_datetime"] = shifts.apply(get_end_datetime, axis=1)
    shifts = shifts.drop(
        ["start_time", "start_date", "end_time", "end_date"], axis=1)

    # strip newlines and extra spaces from task titles
    shifts["task"] = shifts["task"].apply(lambda s: s.strip())

    return shifts


def parse_helper_forms(directory: str):
    shifts = DataFrame()

    file_paths = [
        join(directory, file_name)
        for file_name in listdir(directory)
        if is_xlsx(file_name)
    ]

    for path in file_paths:
        shifts = concat((shifts, parse_helper_form(path)), ignore_index=True)

    return shifts


if __name__ == "__main__":
    parser = ArgumentParser(prog="Parser for helper forms")
    parser.add_argument("--forms_dir", "-f", required=True, type=str)
    args = parser.parse_args()
    print(parse_helper_forms(args.forms_dir))
