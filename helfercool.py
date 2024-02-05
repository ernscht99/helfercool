#!/usr/bin/env python3
import argparse
from getpass import getpass

from session_commander import Session_commander


def main(url, user_name, skip_network=False, use_login_file=False):
    print(
        """
    ---------------------------------------------------
                    Welcome to HELFERCOOL!
    Your tool to save time working with the helfertool
    ---------------------------------------------------

    PLS LOG IN :D
    """
    )
    password = getpass("Password: ")

    if not skip_network:
        sc = Session_commander(url)

    # Log in at helfertool
    sc.login_server(user_name, password)

    while True:
        print(
            """
            OPTIONS:
            1. SHOW JOB List
            2. SHOW SHIFTS for a given JOB
            3. ADD JOB
            4. ADD SHIFT(S)
            5. VALIDITY CHECK SHIFTS
            6. CHANGE JOB
            7. CHANGE SHIFT
            69. END
            """
        )
        selection_str = input("What do you want to do?\n")
        try:
            selection = int(selection_str)
        except ValueError:
            print("Invalid selection")
            continue

        if selection == 69:
            print("NICE!!! also end")
            break
        elif selection == 1:
            # show job list
            pass
        elif selection == 2:
            # show shift list
            pass
        elif selection == 3:
            # add job
            pass
        elif selection == 4:
            # add shifts
            pass
        elif selection == 5:
            # VALIDITY CHECK SHIFTS
            pass
        elif selection == 6:
            # CHANGE JOB
            pass
        elif selection == 7:
            # CHANGE SHIFT
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Helfercool", description="Command line frontend for helfertool"
    )
    parser.add_argument("-u", "--url", type=str, required=True)
    parser.add_argument("-n", "--username", type=str, required=True)
    args = parser.parse_args()
    main(args.url, args.username)
