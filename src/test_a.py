from data_miner import plot_tally
import pytest

d_country = ["Vietnam", "Singapore", "US", "Malaysia"]
d_date = "03-05-2020"
d_timespan = 40
d_scale = ["linear", "log", "log", "linear"]
d_plot_type = "cdra"

def test_A():
    assert plot_tally(d_country, d_date, d_timespan, scale=d_scale, plot_type=d_plot_type, test_flag=True) == 0

def test_B():
    assert plot_tally(d_country, d_date, d_timespan, scale=d_scale, plot_type=d_plot_type, transpose=True, test_flag=True) == 0
