from csv_processor import parse_data
from helper import modify_date, clear, is_valid_date
from helper import print_type_error as t_stderr
from helper import print_error as stderr
from numpy import array, linspace
from matplotlib import pyplot as plt

def _get_country_data(country, date, days):  
    entries = []
    for i in range(days-1, -1, -1):
        data = parse_data(modify_date(date, -i)).get(country, None)
        if data == None:   
            return -1
        entries.append(data)
    return entries
def _validate_timespan(ts):
    if type(ts) != int:
        t_stderr("timespan", int, ts)
        return False
    if ts <= 0:
        stderr("Expected positive timespan, but given {}".format(ts)) 
        return False
    return True
def _validate_date(d):
    if type(d) != str:
        t_stderr("date", str, d)
        return False
    if not is_valid_date(d):
        stderr("Expected format for date is 'dd-mm-yyyy', but given {}".format(d))
        return False
    return True
def _validate_scale(s):
    if type(s) != str:
        t_stderr("scale", str, s)
        return False
    if s != "log" and s != "linear":
        stderr("Expected value of scale is either 'log' or 'linear', but given {}".format(s))
        return False
    return True
def _validate_pltype(p):
    if type(p) != str:
        t_stderr("plot_type", str, p)
        return False
    return True
def _validate_country(ct):
    if type(ct) != str:
        if type(ct) == list:
            return True
        else:
            stderr("Expected type of country is <class 'str'> or <class 'list'>, but given {}"\
                   .format(type(country)))
            return -1
    return False
def _transpose_plot(countries, date, timespan, scale, plot_type): 
    for country in countries:
        data = _get_country_data(country, date, timespan)
        if data == -1:
            stderr("'{}' is unavailable!".format(country))
            return -1       
        x_data = linspace(-(timespan-1), 0, num=timespan)        
        plt.plot(x_data, array([x[plot_type] for x in data]), ".-", label=country)   
    ylabel = "Number of " + ["confirmed cases", "deaths", "recovered cases", "active cases"][plot_type]    
    plt.yscale(scale)
    plt.xlabel("Number of days since the latest report")
    plt.ylabel(ylabel)
    plt.title(ylabel + " over the world")
    plt.legend(loc="best")
    plt.show()
    return 0
def plot_tally(country, date, timespan, *args, **kwargs):
    global _test_flag
    _test_flag = kwargs.get("test_flag", False)
    multiple_countries = _validate_country(country)
    if multiple_countries == -1:
        return -1        
    if not _validate_date(date):
        return -1    
    if not _validate_timespan(timespan):
        return -1 
    if not multiple_countries:
        scale = kwargs.get("scale", "log")
        if not _validate_scale(scale):
            return -1           
        plot_type = kwargs.get("plot_type", "cdra")
        if not _validate_pltype(plot_type):
            return -1 
        data = _get_country_data(country, date, timespan)
        if data == -1:
            stderr("'{}' is unavailable!".format(country))
            return -1   
        x_data = linspace(-(timespan-1), 0, num=timespan)       
        plot_enabled = False
        if "c" in plot_type:
            plt.plot(x_data, array([x[0] for x in data]), '.b-', label="Confirmed")
            plot_enabled = True
        if "r" in plot_type:
            plt.plot(x_data, array([x[1] for x in data]), '.g-', label="Recovered")
            plot_enabled = True
        if "d" in plot_type:
            plt.plot(x_data, array([x[2] for x in data]), '.k-', label="Deaths")
            plot_enabled = True
        if "a" in plot_type:
            plt.plot(x_data, array([x[3] for x in data]), '.r-', label="Active")
            plot_enabled = True  
        if not plot_enabled:
            stderr("Expected at least one plot type, but given '{}'".format(plot_type))
            return -1      
        plt.yscale(scale)
        plt.xlabel("Number of days since the latest report")
        plt.ylabel("Number of cases")
        plt.title("COVID-19 tally for " + country)
        plt.legend(loc="best")
        if not test_flag:
            plt.show() 
        return 0
    elif kwargs.get("transpose", False):      
        plot_type = kwargs.get("plot_type", "cdra")
        if not _validate_pltype(plot_type):
            return -1
        n = len(plot_type)
        plot_enabled = False
        scale = kwargs.get("scale", ["log"] * n)
        if type(scale) == str:
            scale = [scale] * n
        if type(scale) != list:
            t_stderr("scale", list, scale)
            return -1
        if len(scale) < n:
            scale += ["log"] * (n - len(scale))
        if "c" in plot_type:
            _transpose_plot(country, date, timespan, scale[0], 0)
            plot_enabled = True
        if "r" in plot_type:
            _transpose_plot(country, date, timespan, scale[1], 1)
            plot_enabled = True
        if "d" in plot_type:
            _transpose_plot(country, date, timespan, scale[2], 2)
            plot_enabled = True
        if "a" in plot_type:
            _transpose_plot(country, date, timespan, scale[3], 3)
            plot_enabled = True  
        if not plot_enabled:
            stderr("Expected at least one plot type, but given '{}'".format(plot_type))
            return -1
        return 0
    else:
        n = len(country)            
        scale = kwargs.get("scale", ["log"] * n)
        if type(scale) == str:
            scale = [scale] * n
        if type(scale) != list:
            t_stderr("scale", list, scale)
            return -1
        if len(scale) < n:
            scale += ["log"] * (n - len(scale))          
        plot_type = kwargs.get("plot_type", ["cdra"] * n)
        if type(plot_type) == str:
            plot_type = [plot_type] * n
        elif type(plot_type) != list:
            stderr("Expected plot type is of <class 'list'> or <class 'str'>, but given {}"\
                   .format(type(plot_type)))
            return -1
        if len(plot_type) < n:
            plot_type += ["log"] * (n - len(scale))           
        for i in range(n):            
            plot_tally(country[i], date, timespan, scale=scale[i], plot_type=plot_type[i])
        return 0  
__all__ = [plot_tally]
