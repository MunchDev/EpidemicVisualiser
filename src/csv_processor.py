from helper import print_error as stderr
from urllib.request import urlopen
from os.path import isfile
from json import load, dumps
from csv import reader
from io import StringIO

def fetch_data(date):
    url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master"
    url += "/csse_covid_19_data/csse_covid_19_daily_reports/"
    url += date[3:5] + "-" + date[:2] + "-" + date[6:] + ".csv"
    try:
        return list(reader(StringIO("\n".join(list(map(lambda a: str(a, "utf-8")[:-1], list(urlopen(url))))))))
    except:
        stderr("No dataset found for {}.".format(date))
        return -1 
def parse_data(date):
    filename = "../cache/" + "".join(date.split("-")) + ".json"
    if isfile(filename):
        with open(filename) as f:
            return load(f)	
    data = fetch_data(date).pop(0)
    data_set = dict()
    for entry in data:
        country_name = entry[3]
        if country_name in data_set.keys():
            data_set[country_name][0] += int(entry[7])
            data_set[country_name][1] += int(entry[8])
            data_set[country_name][2] += int(entry[9])
            data_set[country_name][3] += int(entry[10])
        else:
            data_set[country_name] = [int(entry[7]), int(entry[8]), int(entry[9]), int(entry[10])]	
    with open("../cache/" + "".join(date.split("-")) + ".json", "w") as f:
        f.write(dumps(data_set))
    return data_set
