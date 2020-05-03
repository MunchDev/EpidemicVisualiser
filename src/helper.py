from datetime import datetime, timedelta

def modify_date(date, n):
    """
    Receive a date (format dd-mm-yyyy) and add a number of days into it.
    Use negative n for substraction.
    """
    date = datetime.strptime(date, "%d-%m-%Y")
    date += timedelta(days=n)
    return date.strftime("%d-%m-%Y")
