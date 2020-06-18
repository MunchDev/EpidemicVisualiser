from data_miner import plot_tally
from csv_processor import fetch_data

def fetch_data_test():
    valid_dates = ["01-04-2020", "01-05-2020", "01-06-2020"]
    for date in valid_dates:
        assert fetch_data(date, test_flag=True).

def plot_tally_test():
    d_country = ["Vietnam", "Singapore", "US", "Malaysia"]
    d_date = "03-05-2020"
    d_timespan = 40
    d_scale = ["linear", "log", "log", "linear"]
    d_plot_type = "cdra"

    assert plot_tally(d_country, d_date, d_timespan, scale=d_scale, plot_type=d_plot_type) == 0
    assert plot_tally(d_country, d_date, d_timespan, scale=d_scale, plot_type=d_plot_type, transpose=True) == 0