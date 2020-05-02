from datetime import datetime, timedelta

def modify_date(date, n):
    """
    Receive a date (format dd-mm-yyyy) and add a number of days into it.
    Use negative n for substraction.

    Modified and adapted from: www.pressthered.com/adding_dates_and_times_in_python
    """
    date = datetime.strptime(date, "%d-%m-%Y")
    date += timedelta(days=n)
    return date.strftime("%d-%m-%Y")
