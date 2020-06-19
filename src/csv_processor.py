"""CSV downloader and data cleaner

This file contains 2 functions, one is to download the daily data
and one is to process it.

This Python file is not invokable but importable.

Notes
-----
It is highly suggested that only parse_data() should be exported.
"""

# Helper function
from helper import normalise_date, print_error as stderr, print_type_error as t_stderr

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
from typing import Any, Dict, List, Union, cast


def fetch_data(date: str, **kwargs: bool) -> Union[List[List[str]], Dict[str, Any]]:
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
    test_flag: bool = kwargs.get("test_flag", False)
    if test_flag != True and test_flag != False:
        t_stderr("test_flag", bool, test_flag)
        return {"err": "test_flag is invalid", "code": 1}

    # Parameters validation
    date = normalise_date(date)
    if date == "":
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
    raw_data: bytes = b""
    try:
        raw_data = urlopen(url).read()
        if len(raw_data) == 0:
            raise Exception("Empty file downloaded!")
    except HTTPError as http_err:
        # Not found
        if http_err.code == 404:
            err = f"No record found for date {date}. " + \
                "Maybe the upstream database is not updated yet?"
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
            return {"err": str(err), "code": -1}
        else:
            stderr(str(err))
            return [[""]]

    # Cast bytes to str
    pre_processed_data: str = str(raw_data, "utf-8")

    # Turn string to data stream
    data_stream: StringIO = StringIO(pre_processed_data)

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


def parse_data(date: str, **kwargs: bool) -> Union[Dict[str, List[int]], Dict[str, Any]]:
    """Parse CSV data and return processed data

    Retrieve CSV data for this date and start parsing it

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
    Dict[str, List]:
        A dictionary of pairs of the country name and its statistics
            Format: Dict[name, List[confirmed, deaths, recovered, active]]

    Dict[str, Any]:
        (Only when test_flag is enabled)
        Return at least the error message and error code:
            * 0 : Ok

            * 1 : Failed validation for 'test_flag'

            * 2 : Failed validation for 'date'

            * 3 : Code is invoked directly

            * 4 : Failed validation of processed data

            * -1: Unexpected error

    Throws
    ------
    Will not throw any error. On handled exceptions, print error message
    and return {"": [""]}. On unhandled exceptions, print error message, log error
    and return {"": [""]}.
    """

    # Acquire and validate control flags
    test_flag: bool = kwargs.get("test_flag", False)
    if test_flag != True and test_flag != False:
        t_stderr("test_flag", bool, test_flag)
        return {"err": "test_flag is invalid", "code": 1}

    # Parameters validation
    date = normalise_date(date)
    if date == "":
        err = f"Your input: {date} is not a valid date. Maybe it is a typo?"
        if test_flag:
            return {"err": err, "code": 2}
        return {"": []}

    # Get absolute path to current source file
    # To be imported only!
    # Will raise an exception if script invokation.
    filename: Path = Path()
    try:
        filename = Path(__file__).absolute()
    except NameError:
        err = f"The script is to be imported only!"
        if test_flag:
            return {"err": err, "code": 3}
        return {"": [""]}

    # Get absolute path to the parent folder
    # Eg. EpidemicVisualiser/
    filename = filename.parents[1]

    # Get absolute path to the cache file (if available)
    filename = filename.joinpath("cache", "".join(date.split("-")) + ".json")

    # Check cache file availability
    if isfile(filename):
        # If available, load it and return
        with open(filename) as f:
            if test_flag:
                return {"err": None, "code": 0}
            return load(f)

    # Fetch pre-processed data
    # Cast union to deterministic type
    data: List[List[str]] = cast(List[List[str]], fetch_data(date))
    data.pop(0)           # Removed the first line (labels)

    data_set: Dict[str, List[int]] = dict()

    # Scanning for each country
    for entry in data:
        try:
            # Get country name
            country_name: str = entry[3]

            # Get statistics
            confirmed: int = int(entry[7])
            death: int = int(entry[8])
            recovered: int = int(entry[9])
            active: int = int(entry[10])

            # Check if countries are recorded already
            # Applicable for countries with states
            if country_name in data_set.keys():
                data_set[country_name][0] += confirmed
                data_set[country_name][1] += death
                data_set[country_name][2] += recovered
                data_set[country_name][3] += active
            else:
                # Newly recorded countries
                data_set[country_name] = [confirmed, death, recovered, active]

        # CSV file format different between 21/3 and 22/3
        except ValueError:
            # Get country name
            country_name: str = entry[1]

            # Get statistics
            confirmed: int = int(entry[3])
            death: int = int(entry[4])
            recovered: int = int(entry[5])
            active: int = confirmed - death - recovered

            # Check if countries are recorded already
            # Applicable for countries with states
            if country_name in data_set.keys():
                data_set[country_name][0] += confirmed
                data_set[country_name][1] += death
                data_set[country_name][2] += recovered
                data_set[country_name][3] += active
            else:
                # Newly recorded countries
                data_set[country_name] = [confirmed, death, recovered, active]

    # Cache the processed data for future use
    with open(filename, "w") as f:
        # Serialise dictionary into JSON string
        json_data: str = dumps(data_set)

        # Write to file
        f.write(json_data)

    # Data set validation
    if len(data_set) != 0:
        if "Singapore" in data_set.keys():
            if len(data_set["Singapore"]) == 4:
                if test_flag:
                    return {"err": None, "code": 0}
                else:
                    return data_set
            else:
                err = f"Invalid data found for {date}."
                if test_flag:
                    return {"err": err, "code": 4}
                else:
                    stderr(err)
                    return {"": []}
        else:
            err = f"Invalid data found for {date}."
            if test_flag:
                return {"err": err, "code": 4}
            else:
                stderr(err)
                return {"": []}
    else:
        err = f"Invalid data found for {date}."
        if test_flag:
            return {"err": err, "code": 4}
        else:
            stderr(err)
            return {"": []}
