from datetime import datetime, timedelta
from os import system, name
from colorama import Fore, Style

def modify_date(date, n):
    """
    Receive a date (format dd-mm-yyyy) and add a number of days into it.
    Use negative n for substraction.
    """
    date = datetime.strptime(date, "%d-%m-%Y")
    date += timedelta(days=n)
    return date.strftime("%d-%m-%Y")

def is_valid_date(date):
    if type(date) != str:
        return False
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

def print_type_error(obj, expected, given):
    print("{0}The expected type of {1} is {2}, but given {3}{4}".format(Fore.RED, obj, typeof(expected), typeof(given), Style.RESET_ALL))
