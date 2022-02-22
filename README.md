# Epidemic Visualiser

This repository contains a visualiser and prediction model for the COVID-19 situation.

Note: This is a school project, feel free to send me a PR!

__Status__: I'm too busy with school work to continue this project! However, if you stumble
upon this, these are things you can update to make it work again:

- The structure of the file published JHU has changed over the past two years. You need to
update the CSV parser to make it work.

## Go to LiveNotes

|Branch                   |Notebook on Binder                                            |
|-------------------------|--------------------------------------------------------------|
|master (Production ready)|[![Binder](https://mybinder.org/badge_logo.svg)][bd-master-nb]|
|develop (Experimental)   |[![Binder](https://mybinder.org/badge_logo.svg)][bd-dev-nb]   |

## Build status

|Branch                   |Notebook on Binder                                                                        |
|-------------------------|------------------------------------------------------------------------------------------|
|master (Production ready)|[![Build Status](https://travis-ci.com/MunchDev/EpidemicSimulator.svg?branch=master)][ci] |
|develop (Experimental)   |[![Build Status](https://travis-ci.com/MunchDev/EpidemicSimulator.svg?branch=develop)][ci]|

## Usage

### Live notebooks

Click on any [LiveNote](#go-to-livenotes) above to explore our notebooks
without the hassle of downloading or installing anything!
Explore as far as you want, and if you break it?
Go and create another notebook!

### Local machine

If you want to host the notebook on your own computer, follow the instructions:

#### Installation

You need:

* Python 3.5 or above (higher versions are not tested, but highly stable)
* (Optional) ```virtualenv```

and run the following:

```shell
git clone https://github.com/MunchDev/EpidemicSimulator
cd EpidemicSimulator
pip install -r "requirements.txt"
```

*NOTE*: It does not install ```JupyterLab``` for Jupyter Notebook, if you want to use it,
please install it on [their website](https://jupyter.org).

#### Import

Please ***DO AND ONLY DO*** the following:

```python
from data_miner import plot_tally
plot_tally(....)
```

Input validation is only applied in this front-end function. Other functions are hidden by default.
If you want to expose it, ***DO AT YOUR OWN RISK***.

## Documentation

This documentation is only available to front-end functions. Other functions used by those functions are strictly internal and optimised.

### ```data_miner.plot_tally```

Draw the COVID-19 statistics plots of different countries in a period of time, using different scales and types.\
_Return value_: Returns 0 if no errors occured and -1 if at least one error occurs.

#### _Positional arguments_

* _country_: A string or a list of string. Each string is a name of a country you want to plot.
* _date_: A string of date in this format ```dd-mm-yyyy```. This is the date of the latest data to be plotted.
* _timespan_: An integer. This is the period of data to be plotted, from the _date_ backwards.

#### _Keyword arguments_

* _scale_: A string or a list of string. Each string is either "log" or "linear, indicating the type of y-scale of the country to be plotted. Default is "log".
* _plot_type_: A string or a list of string. Each string consists of letter (c)onfirmed cases, (d)eaths, (r)ecovered cases and (a)ctive cases, indicating the type of plot to be drawn.

## Help

### For list of supported countries

[Click HERE](https://github.com/MunchDev/EpidemicSimulator/blob/dev-country/cache/countries.json)

[bd-master-nb]: https://mybinder.org/v2/gh/MunchDev/EpidemicSimulator/master?filepath=src%2Ftally_visualiser.ipynb
[bd-dev-nb]: https://mybinder.org/v2/gh/MunchDev/EpidemicSimulator/develop?filepath=src%2Ftally_visualiser.ipynb
[ci]: https://travis-ci.com/MunchDev/EpidemicSimulator
