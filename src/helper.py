from datetime import datetime, timedelta
from os import system, name
from colorama import Fore, Style

def modify_date(date, n):
    return (datetime.strptime(date, "%d-%m-%Y") + timedelta(days=n)).strftime("%d-%m-%Y")
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
    print_error("The expected type of {0} is {1}, but given {2}".format(obj, type(expected), type(given)))
    return
def print_error(err):
    print("{0}{1}{2}".format(Fore.RED, err, Style.RESET_ALL))
    return
