from typing import Dict, Any, List, cast
from csv_processor import fetch_data

def test_fetch_data():
    valid_dates: List[str] = ["01-04-2020", "01-05-2020", "01-06-2020"]
    for date in valid_dates:
        assert cast(Dict[str, Any], fetch_data(date, test_flag=True))["code"] == 0

    invalid_dates: List[str] = ["01-4-2020", "1-05-2020", "01-06-20"]
    for date in invalid_dates:
        assert cast(Dict[str, Any], fetch_data(date, test_flag=True))["code"] == 0