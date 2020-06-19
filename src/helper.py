"""A set of helper functions to be used by EpidemicVisualiser

This Python file is not invokable but importable.
"""
# Used by modify_date
import re
from datetime import datetime, timedelta

# Used by OS-related operations (screen buffer, path)
from os import system, name

# Used by static type checker
from typing import Any, Match, Pattern, Sequence, Type, cast

# Used for date checking
# Credit: Ofir Luzon
# Link: https://stackoverflow.com/questions/15491894/regex-to-validate-date-format-dd-mm-yyyy
valid_date_re: Pattern[Any] = re.compile(
    r"^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(" +
    r"?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2)" +
    r")(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-" +
    r"|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]" +
    r"|[2468][048]|[13579][26])|(?:(?:16|[2468][" +
    r"048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[" +
    r"0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4" +
    r"(?:(?:1[6-9]|[2-9]\d)?\d{2})$", re.VERBOSE)

date_format_re: Pattern[Any] = re.compile(r"^(\d+)[-/.](\d+)[-/.](?:20)?(\d+)$", re.VERBOSE)

def is_valid_date(date: str) -> bool:
    """Check if the date format is valid

    Parameters
    ----------
    str:
        The date in any OS-supported format

    Returns
    -------
    bool
        Whether it is a valid date or not
    """

    # Match the date against the pattern
    if valid_date_re.match(date) == None:
        return False
    return True


def normalise_date(date: str, n: int = 0) -> str:
    """Take any arbitrary date format and convert it to a uniform format

    (Optional) Offset the date by a number of days

    Parameters
    ----------
    str:
        The date in any OS-supported format
    int:
        The offset

    Returns
    -------
    str:
        Uniformed date format, offset if available
    """

    # Input validation
    if not is_valid_date(date):
        return ""

    # Match the date against the pattern
    # then cast it to the deterministic type
    matching: Match[Any] = cast(Match[Any], date_format_re.match(date))

    # Take all matching groups
    # Can be None when date format is unrecognisable
    matching_group: Sequence[Any] = []
    try:
        matching_group = matching.groups()

    # When None, return empty string
    except AttributeError:
        return ""

    # Get formatted string
    # Return if no offset
    formatted_string: str = '{:0>2}-{:0>2}-20{}'.format(*matching_group)
    if n == 0:
        return formatted_string

    # With offset
    else:
        # Turn to datetime object
        datetime_obj: datetime = datetime.strptime(
            formatted_string, "%d-%m-%Y")

        # Offset
        datetime_obj += timedelta(days=n)

        # Turn to date string
        date = datetime_obj.strftime("%d-%m-%Y")

        # Return offset date
        return date


def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
    return True


def print_type_error(obj: Any, expected: Type[Any], given: Any):
    print_error("The expected type of {0} is {1}, but given {2}".format(
        obj, expected, type(given)))
    return


def print_error(err: str):
    print("{0}{1}{2}".format("\33[31m", err, "\33[37m"))
    return
