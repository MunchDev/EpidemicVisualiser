"""Console application for Epidemic Visualiser

This script contains the CLI implementation for Epidemic Visualiser.
It includes instructions, help messages, etc.

Parameters
----------
This script is invokable without any parameters.

Returns
-------
int
    Indicates whether the script ran successfully or not.
    Returns 0 on succeed, otherwise, returns -1 with error messages printed out.

Throws
------
RuntimeError
    Thrown when the list of countries cannot be read.
"""

# Primary API to be used
from data_miner import plot_tally

# Helper functions
from helper import clear, is_valid_date
from helper import print_error as stderr

# OS-related libraries (I/O operations, syscalls)
from sys import exit
from pathlib import Path

# JSON parser
from json import loads

# Static type checking
from typing import Any, Callable, List, Dict

# Create a list of country as accepted inputs
countries: List[str] = []
try:
    # Read the file from '../cache/countries.json'
    path: Path = Path(__file__).absolute().parents[1].joinpath(
        "cache", "countries.json")
    with open(path) as f:
        countries = loads(f.read())

    # Data validation
    if countries == None or len(countries) == 0:
        stderr("Unable to load countries! Aborting...")
        input("Press Enter to continue...")
        raise RuntimeError("Unable to load countries!")
except:
    # The script is not expected to run unless countries' names are loaded.
    # Return -1 on exit with error message as above.
    exit(-1)


def main() -> int:
    """Entry point of the script

    Parameters
    ----------
    None

    Returns
    -------
    int
        Indicates whether the script ran successfully or not.
        Returns 0 on succeed, otherwise, returns -1 with error messages printed out.

    Notes
    -----
    This function acquires user's first input then calls to another function
    to collect parameters
    """

    # Available options as the first input
    # Users will get to choose either.
    welcome_options: List[str] = [
        "Show country tally plot",
        "Tranposed version of the above"
    ]

    # Dummy placeholder for the second option
    # The second option is a tranposed version of the first one.
    def w_plot() -> int:
        return ct_plot(True)

    # Corresponds to available options
    f: List[Callable[[], int]] = [ct_plot, w_plot]

    # Collects user's option
    option: int = welcome_screen_option(welcome_options)

    # Calls the required option then returns its return value
    return f[option]()


def ct_plot(transpose: bool = False) -> int:
    """API wrapper call for plotting

    Collects the required parameters from the user then passes it to
    an imported API.

    Parameters
    ----------
    bool
        Indicates the first or the second option.
        To be passed by the call earlier in main().

    Returns
    -------
    int
        Indicates whether the script ran successfully or not.
        Returns 0 on succeed, otherwise, returns -1 with error messages printed out.
    """
    def get_ct() -> List[str]:
        """A sub-function collecting countries from the user"""

        # Loop control flag
        flag: bool = False
        countries_list: List[str] = []

        # Loop to do validation check and collect multiple countries
        while True:
            clear()

            # Print instructions and where to get help
            print("Step 1: Choose the countries you want to plot\n")
            print("Country -- The country to be plotted")
            print("Now supported multiple countries! You can put any countries in a list")
            print("and it will be drawn.\n")
            print("For the full list of available countries, please go to:")
            print("https://github.com/MunchDev/EpidemicSimulator\n")
            print("Leave empty to proceed to Step 2.\n")

            # Check flag for failed validation check previously
            if flag:
                print("Country name is invalid! Try again.\n")

            # Read user's input and reset the flag
            country: str = input("Enter country name > ")
            flag = False

            # Start input validation
            if country == "":
                # Empty input is used to exit, if at least
                # one country has been provided.
                # Otherwise, reports an error and redoes.
                if len(countries_list) == 0:
                    clear()
                    print(
                        "You did not enter any valid country! Please enter at least one.")
                    input("Press Enter to go back and try again")
                else:
                    break
            elif country not in countries:
                # Check for failed validation and set the flag
                flag = True
            else:
                countries_list.append(country)
        clear()
        return countries_list

    def get_date() -> str:
        """A sub-function collecting the date from the user"""

        # Loop control flag
        flag: bool = False
        date: str = str()

        # Loop to do validation check and collect multiple countries
        while True:
            clear()

            # Print instructions
            print("Step 2: Choose a date")
            print("Date -- The latest date to be plotted (in dd-mm-yyyy format)")
            print("Please note that there are delays between the real-time report")
            print("and this compiled report. If there is no report available")
            print("for today, please switch to the previous date.")

            # Check flag for failed validation check previously
            if flag:
                print("\nDate is invalid! Try again.\n")

            # Read user input and reset the flag
            date: str = input("Enter date > ")
            flag = False

            # Input validation
            if is_valid_date(date):
                break
            else:
                # Check for failed validation and set the flag
                flag = True
        return date

    def get_ts() -> int:
        """A sub-function collecting a timespan from the user"""

        # Loop control flag
        flag: bool = False
        ts: int = 0

        # Loop to do validation check and collect multiple countries
        while True:
            clear()

            # Print instructions
            print("Step 3: Choose a suitable timespan")
            print("Timespan -- The period of data plotted")
            print("Please choose a suitable timespan, so that the earliest")
            print("date is no earlier than 22-03-2020.")

            # Check flag for failed validation check
            if flag:
                print("\nTimespan is invalid! Try again.\n")

            # Read user input and reset the flag
            ts_str: str = input("Enter timespan > ")
            flag = False

            # Input validation
            if ts_str.isdigit():
                ts = int(ts_str)
                if 0 < ts < 0x7fffffff:
                    break

            # Check for failed validation and set the flag
            flag = True
        return ts

    def get_scale() -> List[str]:
        """A sub-function collecting a scale from the user"""

        # Loop control flag
        flag: bool = False
        scale: List[str] = []

        while True:
            clear()

            # Print instructions
            print("Step 4: Choose the scale you will be using")
            print(
                "Scale -- Set to 'linear' for linear scale or 'log' for logarithmic scale")
            print(
                "Support multiple countries. If only one string of scale is provided, it")
            print(
                "will used across all plots. If the number of scale is smaller than the")
            print('number of countries, the rest will be taken as default of "log".\n')
            print("Leave empty to proceed to Step 5.\n")

            # Check flag for failed validation check
            if flag:
                print("Scale is invalid! Try again.\n")

            # Read user input and reset the flag
            s: str = input("Enter scale name ('log' or 'linear') > ")
            flag = False

            # Input validation
            if s == "":
                # Empty input is used to exit, if at least
                # one scale has been provided.
                # Otherwise, reports an error and redoes.
                if len(scale) == 0:
                    clear()
                    print(
                        "You did not enter any valid scale! Please enter at least one.")
                    input("Press Enter to go back and try again")
                else:
                    break
            elif s != "log" and s != "linear":
                # Check for failed validation and set the flag
                flag = True
            else:
                scale.append(s)
        clear()
        return scale

    def get_pltype() -> List[str]:
        """A sub-function collecting plot type(s) from the user"""

        # Loop control flag
        flag: bool = False
        pltype: List[str] = []
        while True:
            clear()

            # Print instructions
            print("Step 5: Choose the plot type(s) you will be using")
            print(
                "Plot type -- Show plot of confirmed cases (c), deaths (d), recovered cases (r),")
            print("active cases (a) or any combination of these.")
            print(
                "Support multiple countries. If only one string of plot type is provided, it")
            print(
                "will used across all plots. If the number of plot type is smaller than")
            print(
                'the number of countries, the rest will be taken as default of "cdra".\n')
            print("Leave empty to proceed to finish.\n")

            # Check flag for failed validation check
            if flag:
                print("Plot type is invalid! Try again.\n")

            # Read user input and reset the flag
            p: str = input("Enter plot type > ")
            flag = False

            # Input validation
            if p == "":
                if len(pltype) == 0:
                    clear()
                    print(
                        "You did not enter any valid plot type! Please enter at least one.")
                    input("Press Enter to go back and try again")
                else:
                    break
            elif ("c" not in p) and ("d" not in p) and ("r" not in p) and ("a" not in p):
                flag = True
            else:
                pltype.append(p)
        clear()
        return pltype

    # Collect all parameters once
    data: Dict[str, Any] = {"c": get_ct(), "d": get_date(), "t": get_ts(),
                            "s": get_scale(), "p": get_pltype()}

    # Define a dummy function for static type coherence
    def dummy_opt():
        """A dummy function"""
        pass

    # Ask user to verify and confirm the input.
    opt: Callable[[], Any] = dummy_opt
    while True:
        # Ask for any changes
        p: str = input(
            "Do you want to change (c)ountries, (t)imespan, (s)cale, (p)lot type or are you (o)kay? > ").lower()

        # Determine what to change and call the particular sub-function
        possible_options: Dict[str, Callable[[], Any]] = {
            "c": get_ct, "d": get_date, "t": get_ts, "s": get_scale, "p": get_pltype}
        opt = possible_options.get(p, dummy_opt)

        # User confirmed the input
        if p == "o":
            break

        # Input validation
        if opt.__name__ == dummy_opt.__name__:
            continue

        # Make the change
        if type(opt) != str:
            data[p] = opt()

    # Make the call to an internal API.
    return plot_tally(data["c"], data["d"], data["t"],
                      scale=data["s"], plot_type=data["p"], transpose=transpose)


def welcome_screen_option(options: List[str]) -> int:
    """Print landing screen and collect an option from the user

    Parameters
    ----------
    List[str]
        A list of options for users to choose from.

    Returns
    -------
    int
        The index of the chosen option.
    """
    i: int = -1
    while True:
        clear()

        # Print options
        print("Welcome to Epidemic Simulator -- Console version")
        print("What do you like to do? (-1 to exit)\n")
        for i, option in zip(range(len(options)), options):
            print("({0}) {1}".format(i + 1, option))

        # Read user input
        i_str = input("Your option > ")

        # On exit
        if i_str == "-1":
            exit(0)

        # Input validation
        if i_str.isdigit() and 0 < int(i) <= len(options):
            i = int(i_str)
            break
    clear()

    # The given options are one-indexed.
    # Convert back to zero-indexed
    return i - 1


# Program entry point
# Call to the main() function
if __name__ == "__main__":
    main()
