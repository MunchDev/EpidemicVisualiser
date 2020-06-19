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
from helper import modify_date

def test_modify_date():
    pre_dates: List[str] = ["08-05-2020", "8-5-2020", "08-5-20", "08/05/20"]

    # No offset
    dates: List[str] = ["08-05-2020"] * 4    
    for pre, dat in zip(pre_dates, dates):
        assert modify_date(pre) == dat

    # With offset
    offsets: List[int] = [-2, -1, 1, 2]
    dates = ["06-05-2020", "07-05-2020", "09-05-2020", "10-05-2020"]
    for pre, off, dat in zip(pre_dates, offsets, dates):
        assert modify_date(pre, off) == dat