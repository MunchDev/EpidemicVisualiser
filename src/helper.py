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


def modify_date(date: str, n: int = 0) -> str:
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
    Uniformed date format, offset if available
    """

    # Create Regex object for matching
    date_re: Pattern[Any] = re.compile(
        r"\s*(\d+)[-/](\d+)[-/](?:20)?(\d+)\s*", re.VERBOSE)    

    # Match the date against the pattern
    # then cast it to the deterministic type
    matching: Match[Any] = cast(Match[Any], date_re.match(date))

    # Take all matching groups
    matching_group: Sequence[Any] = matching.groups()

    # Get formatted string
    # Return if no offset
    formatted_string: str = '{:0>2}-{:0>2}-20{}'.format(*matching_group)
    if n == 0:
        return formatted_string

    # With offset
    else:
        # Turn to datetime object
        datetime_obj: datetime = datetime.strptime(formatted_string, "%d-%m-%Y")

        # Offset
        datetime_obj += timedelta(days=n)

        # Turn to date string
        date = datetime_obj.strftime("%d-%m-%Y")
        
        # Return offset date
        return date


def is_valid_date(date: str) -> bool:
    if len(date) != 10:
        return False
    c = date.split("-")
    if len(c) != 3:
        return False
    if len(c[0]) != 2 or len(c[1]) != 2 or len(c[2]) != 4:
        return False
    if not (c[0].isdigit() and c[1].isdigit() and c[2].isdigit()):
        return False
    return True


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
