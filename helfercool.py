#!/usr/bin/env python3
import argparse
from getpass import getpass

from session_commander import Session_commander


def main(url, user_name, festival_id, skip_network=False, use_login_file=False):
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
        sc = Session_commander(url,festival_id)

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
            6. REMOVE JOB
            7. REMOVE SHIFT
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
            data = {
                "name_de": "test suff team",
                "name_en": "test suff team",
                "description_de": "<p>test suff beschreibung</p>\r\n",
                "description_en": "<p>test suff beschreibung in englisch</p>\r\n",
                "important_notes_de": "<p>need saufen und fahren</p>\r\n",
                "important_notes_en": "<p>dont drinken and driven</p>\r\n",
                "public": "on",
                "infection_instruction": "on",
                # prerequesits fehlen
            }
            sc.add_job(data)
        elif selection == 4:
            print("Adding shift(s)")
            data = {
                "name": "Suff2",
                "begin_0": "2024-01-25",
                "begin_1": "11:00",
                "end_0": "2024-01-25",
                "end_1": "14:00",
                "number": "6",
            }
            sc.add_shift(data, 1)
        elif selection == 5:
            # VALIDITY CHECK SHIFTS
            pass
        elif selection == 6:
            print("Remove Job")
            sc.remove_job(1)
        elif selection == 7:
            # CHANGE SHIFT
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Helfercool", description="Command line frontend for helfertool"
    )
    parser.add_argument("-u", "--url", type=str, required=True)
    parser.add_argument("-n", "--username", type=str, required=True)
    parser.add_argument("-f", "--festival", type=str, required=True)
    args = parser.parse_args()
    main(args.url, args.username, args.festival)
