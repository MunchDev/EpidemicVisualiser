# Epidemic Simulator
This repository contains visualiser and prediction model for the COVID-19 situation.

Note: This is a school project, feel free to send my a PR!
## Go to LiveNotes
|Branch                 |Notebook on Binder                                            |
|-----------------------|--------------------------------------------------------------|
|master (Stable release)|[![Binder](https://mybinder.org/badge_logo.svg)][bd-master-nb]|
|rc (Approved release)  |[![Binder](https://mybinder.org/badge_logo.svg)][bd-rc-nb]    |
|dev (Experimental)     |[![Binder](https://mybinder.org/badge_logo.svg)][bd-dev-nb]   |
## Build status
|Branch                 |Notebook on Binder                                                                       |
|-----------------------|-----------------------------------------------------------------------------------------|
|master (Stable release)|[![Build Status](https://travis-ci.com/MunchDev/EpidemicSimulator.svg?branch=master)][ci]|
|rc (Approved release)  |[![Build Status](https://travis-ci.com/MunchDev/EpidemicSimulator.svg?branch=rc)][ci]    |
|dev (Experimental)     |[![Build Status](https://travis-ci.com/MunchDev/EpidemicSimulator.svg?branch=dev)][ci]   |
## Usage
### Live notebooks
Click on any [LiveNote](#go-to-livenotes) above to explore our notebooks,
without the hassle of downloading or installing anything! Explore as far as you want, and if you break it?
Go and create another notebook!
### Local machine
If you want to host the notebook on your own computer, follow the instructions:
#### Installation
You need:
* Python 3.5 or above (higher versions are not tested, but highly stable)
* (Optional) ```virtualenv```
and run the followings:
```shell
$ git clone https://github.com/MunchDev/EpidemicSimulator
$ cd EpidemicSimulator
$ pip install -r "requirements.txt"
```
*NOTE*: It does not install ```JupyterLab``` for Jupyter Notebook, if you still want to use,
please install it as on [their website](https://jupyter.org).
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
_Return value_: Returns 0 if no errors occured and -1 if at least one error occurs.\
##### _Positional arguments_:
* _country_: A string or a list of string. Each string is a name of a country you want to plot.
* _date_: A string of date in this format ```dd-mm-yyyy```. This is the date of the latest data to be plotted.
* _timespan_: An integer. This is the period of data to be plotted, from the _date_ backwards.
##### _Keyword arguments_:
* _scale_: A string or a list of string. Each string is either "log" or "linear, indicating the type of y-scale of the country to be plotted. Default is "log".
* _plot_type_: A string or a list of string. Each string consists of letter (c)onfirmed cases, (d)eaths, (r)ecovered cases and (a)ctive cases, indicating the type of plot to be drawn. 

## List of supported countries

### Countries List

##### These are the countries supported for now, and for it to work, they must be inputted **exactly the same**.
#####[CASE-SENSITIVE]

•  Afghanistan
•  Albania  
•  Algeria  
•  Andorra
•  Angola  
•  Antigua and Barbuda  
•  Argentina 
•  Armenia  
•  Australia  
•  Austria  
•  Azerbaijan  
•  Bahamas  
•  Bahrain  
•  Bangladesh  
•  Barbados  
•  Belarus  
•  Belgium  
•  Belize
•  Benin  
•  Bhutan  
•  Bolivia
•  Bosnia and Herzegovina  
•  Botswana  
•  Brazil  
•  Brunei  
•  Bulgaria
•  Burkina Faso
•  Burma
•  Burundi  
•  Cabo Verde 
•  Cambodia  
•  Cameroon  
•  Canada  
•  Central African Republic  
•  Chad  
•  Chile  
•  China  
•  Colombia
•  Comoros  
•  Congo (Brazzaville)  
•  Congo (Kinshasa)  
•  Costa Rica
•  Cote d'Ivoire  
•  Croatia
•  Cuba  
•  Cyprus  
•  Czechia 
•  Denmark  
•  Djibouti  
•  Dominica
•  Dominican Republic  
•  Ecuador  
•  Egypt  
•  El Salvador
•  Equatorial Guinea  
•  Eritrea  
•  Estonia  
•  Eswatini  
•  Ethiopia
•  Fiji  
•  Finland
•  France  
•  Gabon  
•  Gambia  
•  Georgia
•  Germany  
•  Ghana  
•  Greece  
•  Grenada 
•  Guatemala
•  Guinea  
•  Guinea-Bissau  
•  Guyana  
•  Haiti  
•  Holy See
•  Honduras  
•  Iceland  
•  India  
•  Indonesia  
•  Iran  
•  Iraq  
•  Ireland  
•  Israel  
•  Italy  
•  Jamaica
•  Japan  
•  Jordan  
•  Kazakhstan  
•  Kenya  
•  Korea, South  
•  Kosovo
•  Kuwait  
•  Hungary  
•  Kyrgyzstan  
•  Laos  
•  Latvia  
•  Lebanon  
•  Liberia  
•  Libya
•  Liechtenstein  
•  Lithuania  
•  Luxembourg
•  Madagascar  
•  Malawi  
•  Malaysia  
•  Maldives  
•  Mali 
•  Malta
•  Mauritania
•  Mauritius
•  Mexico  
•  Moldova  
•  Monaco  
•  Mongolia  
•  Montenegro
•  Morocco  
•  Mozambique
•  Namibia  
•  Nepal  
•  Netherlands  
•  New Zealand  
•  Nicaragua
•  Niger  
•  Nigeria  
•  North Macedonia  
•  Norway  
•  Oman  
•  Pakistan  
•  Panama  
•  Papua New Guinea  
•  Paraguay  
•  Peru  
•  Philippines  
•  Poland  
•  Portugal  
•  Qatar  
•  Romania  
•  Russia  
•  Rwanda  
•  Saint Kitts and Nevis
•  Saint Lucia  
•  Saint Vincent and the Grenadines  
•  San Marino  
•  Sao Tome and Principe  
•  Saudi Arabia  
•  Senegal  
•  Serbia  
•  Seychelles
•  Sierra Leone  
•  Singapore  
•  Slovakia  
•  Slovenia  
•  Somalia
•  South Africa  
•  South Sudan  
•  Spain  
•  Sri Lanka  
•  Sudan
•  Suriname  
•  Sweden  
•  Switzerland
•  Syria  
•  Taiwan*  
•  Tajikistan  
•  Tanzania  
•  Thailand  
•  Timor-Leste  
•  Togo  
•  Trinidad and Tobago  
•  Tunisia
•  Turkey  
•  Uganda
•  Ukraine
•  United Arab Emirates  
•  United Kingdom  
•  Uruguay  
•  US
•  Uzbekistan  
•  Venezuela  
•  Vietnam  
•  West Bank and Gaza  
•  Western Sahara  
•  Yemen 
•  Zambia  
•  Zimbabwe

[bd-master-nb]: https://mybinder.org/v2/gh/MunchDev/EpidemicSimulator/master?filepath=src%2Ftally_visualiser.ipynb
[bd-rc-nb]: https://mybinder.org/v2/gh/MunchDev/EpidemicSimulator/rc?filepath=src%2Ftally_visualiser.ipynb
[bd-dev-nb]: https://mybinder.org/v2/gh/MunchDev/EpidemicSimulator/dev?filepath=src%2Ftally_visualiser.ipynb
[ci]: https://travis-ci.com/MunchDev/EpidemicSimulator
