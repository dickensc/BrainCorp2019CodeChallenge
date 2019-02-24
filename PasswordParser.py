import sys
import os
import json
import argparse
import pandas as pd

exit_status = os.EX_OK
p = None
passwd_header = ['Username', 'Password', 'uid', 'GID', 'full_name', 'Home directory', 'Command']
group_header = ['Group', 'Password', 'GID', 'groups']


def _parse_file(file_type: str = 'passwd') -> pd.DataFrame:
    """
    Method for parsing information in the passwd or group file.
    :param file_type: string defining the file type that is being parsed. Either 'passwd' or 'group'. Default 'passwd'.
    :type file_type: str
    :return: A pandas DataFrame of the data parsed from the file.
    """
    global exit_status, p, passwd_header, group_header

    assert((file_type is 'passwd') or (file_type is 'group'))

    if file_type is 'passwd':
        header = passwd_header
        file = p.passwd_file
    else:
        header = group_header
        file = p.group_file

    try:
        file_df = pd.read_table(file, sep=':', comment='#', index_col=0, names=header)

        # simple check to ensure file is formatted correctly
        if file_type is 'passwd':
            assert(not file_df[header[2]].isnull().any())
        else:
            assert(not file_df[header[2]].isnull().any())

    except FileNotFoundError as err:
        print(err)
        exit_status = os.EX_DATAERR
        sys.exit(exit_status)

    except (AssertionError, IndexError):
        if file_type is 'passwd':
            print("The passwd file {} may not be formatted according to Unix standards.".format(p.passwd_file))
        else:
            print("The group file {} may not be formatted according to Unix standards.".format(p.group_file))
        exit_status = os.EX_DATAERR
        sys.exit(exit_status)

    return file_df


def _build_password_df(passwd_df: pd.DataFrame, group_df: pd.DataFrame) -> pd.DataFrame:
    """
    Function for building desired password dataframe from the data stored in the passwd and group file.
    :param passwd_df: The data stored in the passwd file
    :type passwd_df: pd.DataFrame
    :param group_df: The data stored in the group file
    :type group_df: pd.DataFrame
    :return: The DataFrame containing the group list along with the desired fields for each user.
    """
    username_groups_df = passwd_df.loc[:, ['uid', 'full_name']]
    username_groups_df.loc[:, 'groups'] = ''

    # drop groups without users in the 'groups' field from Series
    groups_series = group_df['groups'].str.split(',').dropna()

    # keep track of users that are in 'groups'
    users_in_groups = set()

    # iterate through non-empty group lists and append group to each user 'Group List' field
    for group in groups_series.index:
        username_groups_df.loc[groups_series[group], 'groups'] += ", {}".format(group)
        users_in_groups.update(groups_series[group])

    # remove leading ', ' in 'Group List' column
    username_groups_df.loc[list(users_in_groups), 'groups'] = (
        username_groups_df.loc[list(users_in_groups), 'groups'].str.replace('^, ', '', regex=True)
    )

    # split strings on ',' in 'Group List' column
    username_groups_df.loc[list(users_in_groups), 'groups'] = (
        username_groups_df.loc[list(users_in_groups), 'groups'].str.split(',')
    )

    return username_groups_df


def main() -> None:
    """
    Driver of password parser program.
    :return: None
    """
    global exit_status, p

    if not p.passwd_file:
        p.passwd_file = '/etc/passwd'

    if not p.group_file:
        p.group_file = '/etc/group'

    passwd_df = _parse_file(file_type='passwd')
    group_df = _parse_file(file_type='group')

    username_groups_df = _build_password_df(passwd_df, group_df)

    print(json.dumps(username_groups_df.to_dict(orient='index'), indent=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--passwd_file", type=str,
                        help="Password file path. Leave blank to default to '/etc/passwd'")
    parser.add_argument("-g", "--group_file", type=str,
                        help="Group file path, Leave blank to default to '/etc/group'")
    p = parser.parse_args()

    main()
    sys.exit(exit_status)
