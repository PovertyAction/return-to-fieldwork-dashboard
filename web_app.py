from flask import Flask, render_template
import pandas as pd
import json
import numpy as np

app = Flask(__name__)

def load_covid_data():
    global covid_data
    with open('data/covid_data_per_country.json') as f:
        covid_data = json.load(f)

def load_countries_shape():
    global countries_shape
    with open('data/countries_shape.json') as f:
        countries_shape = json.load(f)

@app.route('/reload_covid_data')
def reload_covid_data():
    load_covid_data()

@app.route('/')
def show_dashboard():
    return render_template('index.html', covid_data=covid_data, countries_shape=countries_shape)

if __name__ == '__main__':
    print('Starting server')
    load_covid_data()

    load_countries_shape()

    app.run(debug=True, threaded=True, host='0.0.0.0', port='5000')


'''
DEPRECATED

def pandas_csv_to_json(file):
    #In case the data in save in a csv and not in a json file

    covid_per_country_df = pd.read_csv(file)

    covid_per_country_data = {}
    #For every country in the df, create a new entry in the dictionary
    for country in covid_per_country_df['country'].unique():

        #Filter data for given country
        country_df = covid_per_country_df[covid_per_country_df['country']==country]

        #Create a dict of data for this given country
        country_data = {}
        for info in ['region', 'status', 'new_cases_per_day', 'case_doubling_rate', 'cases_per_100000', 'government_restrictions', 'subnational_outbreak_status', 'link_to_local_case_count_data']:
            country_data[info] = country_df[info].iloc[0]

        #Save country's data in dict
        covid_per_country_data[country] = country_data

    return json.dumps(covid_per_country_data)


'''
