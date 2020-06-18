from typing import Dict, Any, List, cast
from csv_processor import fetch_data, parse_data

def test_fetch_data():
    # 0 - Ok
    valid_dates: List[str] = ["01-03-2020", "01-04-2020", "01-05-2020", "01-06-2020"]
    for date in valid_dates:
        assert cast(Dict[str, Any], fetch_data(date, test_flag=True))["code"] == 0

    # 2 - Invalid dates
    invalid_dates: List[str] = ["01-4-2020", "1-05-2020", "01-06-20"]
    for date in invalid_dates:
        assert cast(Dict[str, Any], fetch_data(date, test_flag=True))["code"] == 2

def test_parse_data():
    # 0 - Ok
    valid_dates: List[str] = ["01-03-2020", "01-04-2020", "01-05-2020", "01-06-2020"]
    for date in valid_dates:
        assert cast(Dict[str, Any], parse_data(date, test_flag=True))["code"] == 0

    # 2 - Invalid dates
    invalid_dates: List[str] = ["01-4-2020", "1-05-2020", "01-06-20"]
    for date in invalid_dates:
        assert cast(Dict[str, Any], parse_data(date, test_flag=True))["code"] == 2