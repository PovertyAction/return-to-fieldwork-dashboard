'''
    Module 1: Program to pull data from OWD
    Date created: 11 Dec 2020
'''
import urllib.request

def download_covid_data():
    urllib.request.urlretrieve ("https://covid.ourworldindata.org/data/owid-covid-data.csv", "covid_data_raw.csv")
