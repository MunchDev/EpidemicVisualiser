# Used by static type checker
from typing import List

# Sys path operations
from pathlib import Path
import sys

# Get the absolute path
path: Path = Path(__file__).absolute()

# Get source dir path and append to PATH
path = path.parent.parent
sys.path.append(str(path))

# Import the necessary functions
from helper import is_valid_date, normalise_date

def test_is_valid_date():
    # Valid
    valid_dates: List[str] = ["08-05-2020", "8-5-2020", "08-5-20", "08/05/20"]
    for date in valid_dates:
        assert is_valid_date(date)

    # Invalid
    invalid_dates: List[str] = ["08+05+2020", "08052020", "2020-05-08"]
    for date in invalid_dates:
        assert not is_valid_date(date)

def test_normalise_date():
    pre_dates: List[str] = ["08-05-2020", "8-5-2020", "08-5-20", "08/05/20"]

    # No offset
    dates: List[str] = ["08-05-2020"] * 4    
    for pre, dat in zip(pre_dates, dates):
        assert normalise_date(pre) == dat

    # With offset
    offsets: List[int] = [-2, -1, 1, 2]
    dates = ["06-05-2020", "07-05-2020", "09-05-2020", "10-05-2020"]
    for pre, off, dat in zip(pre_dates, offsets, dates):
        assert normalise_date(pre, off) == dat