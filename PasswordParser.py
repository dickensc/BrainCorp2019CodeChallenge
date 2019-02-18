import json
import sys
import os
import argparse

exit_status = os.EX_OK

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--password", type=str, help="passwd file path. Leave blank to default to ")
parser.add_argument("-g", "--groups", type=str, help="group file path")
p = parser.parse_args()


def main() -> None:
    """
    Driver of password parser program
    :return: None
    """
    global exit_status


if __name__ == "__main__":
    main()
    sys.exit(exit_status)
