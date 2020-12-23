'''
    Module 1: Program to pull data from OWD
    Date created: 11 Dec 2020
'''
import urllib.request
from file_names import RAW_COVID_DATA_FILE
import sys

def download_covid_data(show_prints=False):
    try:
        urllib.request.urlretrieve ("https://covid.ourworldindata.org/data/owid-covid-data.csv", RAW_COVID_DATA_FILE)
        if show_prints:
            print('Succesfully downloaded covid data', file=sys.stdout)
        return True
    except Exception as e:
        print('Error when downloading data', file=sys.stdout)
        print(e, file=sys.stdout)
        return False
