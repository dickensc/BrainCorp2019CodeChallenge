import json
import sys
import os
import argparse
import pandas as pd

exit_status = os.EX_OK

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--password", type=str, help="Password file path. Leave blank to default to '/etc/passwd'")
parser.add_argument("-g", "--groups", type=str, help="Groups file path, Leave blank to default to '/etc/groups'")
p = parser.parse_args()


def parse_password_file() -> dict:
    """
    Method for parsing information in password file.
    :return:
    """
    global exit_status

    password_header = ['Username', 'Password', 'UID', 'GID', 'UID Info', 'Home directory', 'Command']

    try:
        password_df = pd.read_table(p.password, sep=':', comment='#', index_col=0, names=password_header)
        assert(not password_df.isnull().any().any())
    except FileNotFoundError as err:
        print(err)
        exit_status = os.EX_DATAERR
        sys.exit(exit_status)
    except (IndexError, AssertionError) as err:
        print(err)
    print(password_df)
    return {}


def main() -> None:
    """
    Driver of password parser program
    :return: None
    """
    global exit_status

    parse_password_file()


if __name__ == "__main__":
    main()
    sys.exit(exit_status)
