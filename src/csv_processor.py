"""CSV downloader and data cleaner

This file contains 2 functions, one is to download the daily data
and one is to process it.

This Python file is not invokable but importable.

Notes
-----
It is highly suggested that only parse_data() should be exported.
"""

# Helper function
from helper import is_valid_date, print_error as stderr, print_type_error as t_stderr

# Used to download CSV file
# And HTTP operations
from urllib.request import urlopen
from urllib.error import HTTPError

# Used to read and process CSV data
from csv import reader
from io import StringIO

# OS-related libraries (I/O, JSON)
from os.path import isfile
from json import load, dumps
from pathlib import Path

# Static type checking
from typing import Any, List, Dict, Union


def fetch_data(date: str, **kwargs: Dict[str, bool]) -> Union[List[List[str]], Dict[str, Any]]:
    """Fetch CSV database from an open-source GitHub repo

    Download the file from CSSEGISandData then turn it into a list of entries.

    Parameters
    ----------
    str:
        The date of data to be fetched. Shoud be in this format: "dd-mm-YYYY"

    Dict[str, bool]:
        Control flags (used in testing and experimenting):
        * test_flag: bool = False
            Enabled only when testing.

    Returns
    -------
    List[List[str]]:
        A list of each entries in the CSV file.

    Dict[str, Any]:
        (Only when test_flag is enabled)
        Return at least the error message and error code:
            * 0 : Ok

            * 1 : Failed validation for 'test_flag'

            * 2 : Failed validation for 'date'
            
            * 3 : Failed download of CSV file
            
            * 4 : Failed validation of processed data
            
            * -1: Unexpected error

    Throws
    ------
    Will not throw any error. On handled exceptions, print error message
    and return [["]]. On unhandled exceptions, print error message, log error
    and return [["]].

    Notes
    -----
    The project can be found at https://github.com/CSSEGISandData/COVID-19
    """

    # Acquire and validate control flags
    test_flag = kwargs.get("test_flag", False)
    if type(test_flag) != bool:
        t_stderr("test_flag", bool, test_flag)
        return {"err": "test_flag is invalid", "code": 1}

    # Parameters validation
    if not is_valid_date(date):
        err = f"Your input: {date} is not a valid date. Maybe it is a typo?"
        if test_flag:
            return {"err": err, "code": 2}
        return [[""]]

    # Crafting URL
    url: str = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master"
    url += "/csse_covid_19_data/csse_covid_19_daily_reports/"

    # Filename
    # Because the format of the filename is mm-dd-YYYY
    # Need to convert to this format
    url += date[3:5] + "-" + date[:2] + "-" + date[6:] + ".csv"

    # Download raw data
    # High chances that newest data is not available
    # Or filename format changed.
    # Try-catch wrapper catch this error (HTTP Error 404)
    raw_data: List[str] = []
    try:
        raw_data = list(urlopen(url))
        if len(raw_data) == 0:
            raise Exception("Empty file downloaded!")
    except HTTPError as http_err:
        # Not found
        if http_err.code == 404:
            err = f"No record found for date {date}. " + "Maybe the upstream database is not updated yet?"
            if test_flag:
                return {"err": err, "code": 3}
            else:
                stderr(err)
                return [[""]]
        # Other HTTP exceptions
        else:
            err = f"Unexpected error: {http_err}"
            if test_flag:
                return {"err": err, "code": 3}
            else:
                stderr(err)
                return [[""]]
    except Exception as err:
        # Non-HTTP exceptions
        if test_flag:
            return {"err": err, "code": -1}
        else:
            stderr(err)
            return [[""]]

    # Remove unnecessary escape characters and
    # apply Python-default encoding
    pre_processed_data: List[str] = list(map(lambda a: str(a)[:-1], raw_data))

    # Join pre-processed data again into lines and
    # turn them into a data stream
    data_stream: StringIO = StringIO("\n".join(pre_processed_data))

    # Use CSV processor to break down each entry into separate rows an
    # then list-ify it to a list of lists of tokens.
    result_data: List[List[str]] = list(reader(data_stream))

    # Data validation check
    if len(result_data) != 0:
        if len(result_data[0]) != 0:
            if len(result_data[0][0]) != 0:
                if test_flag:
                    return {"err": None, "code": 0}
                return result_data
            else:
                err = f"Invalid data found for {date}."
                if test_flag:
                    return {"err": err, "code": 4}
                else:
                    stderr(err)
                    return [[""]]
        else:
            err = f"Invalid data found for {date}."
            if test_flag:
                return {"err": err, "code": 4}
            else:
                stderr(err)
                return [[""]]
    else:
        err = f"Invalid data found for {date}."
        if test_flag:
            return {"err": err, "code": 4}
        else:
            stderr(err)
            return [[""]]

def parse_data(date):
    filename = Path(__file__).absolute().parents[1].joinpath(
        "cache", "".join(date.split("-")) + ".json")
    if isfile(filename):
        with open(filename) as f:
            return load(f)
    data = fetch_data(date) 
    data = data.pop(0)
    data_set = dict()
    for entry in data:
        country_name = entry[3]
        if country_name in data_set.keys():
            data_set[country_name][0] += int(entry[7])
            data_set[country_name][1] += int(entry[8])
            data_set[country_name][2] += int(entry[9])
            data_set[country_name][3] += int(entry[10])
        else:
            data_set[country_name] = [int(entry[7]), int(
                entry[8]), int(entry[9]), int(entry[10])]
    with open(filename, "w") as f:
        f.write(dumps(data_set))
    return data_set
