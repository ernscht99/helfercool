#!/usr/bin/env python3
import argparse
from getpass import getpass

from excel_parser import parse_helper_forms
from session_commander import Session_commander

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Autoentry")
    parser.add_argument("-d", "--directory", type=str, required=True)
    parser.add_argument("-n", "--username", type=str, required=True)
    parser.add_argument("-f", "--festival", type=str, required=True)
    parser.add_argument("-u", "--url", type=str, required=True)
    args = parser.parse_args()
    shifts_df = parse_helper_forms(args.directory)
    print(shifts_df)
    passwd = getpass()
    sc = Session_commander(args.url, args.festival)
    sc.login_server(args.username, passwd)
    sc.add_jobs(list(set(shifts_df["task"])))
