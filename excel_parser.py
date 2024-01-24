#!/usr/bin/env python3
from argparse import ArgumentParser
from os import listdir
from os.path import join

from pandas import DataFrame, concat, read_excel

col_names = [
    "task",
    "subtask",
    "start_date",
    "start_time",
    "end_date",
    "end_time",
    "num_helpers",
]


def is_xlsx(file_name: str):
    return file_name.endswith(".xlsx")


def parse_helper_form(xlsx_file: str):
    shifts = read_excel(xlsx_file, skiprows=4, usecols="A:G", names=col_names)
    # drop rows that are completely missshapen
    shifts.drop(subset=["num_helpers"])
    shifts.drop(subset=["task"])
    import pdb

    pdb.set_trace()
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
