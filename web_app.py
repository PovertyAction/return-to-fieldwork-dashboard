from flask import Flask, render_template
import pandas as pd
import json
import numpy as np

app = Flask(__name__)

def load_covid_data(show_prints=False):
    global covid_data
    try:
        with open('data/covid_data_per_country.json') as f:
            covid_data = json.load(f)
        if show_prints:
            print('Correctly loaded covid_data_per_country.json [NEED TO CHANGE THIS TO country_stats.json]')
        return 'True'
    except Exception as e:
        print('Error when downloading covid_data_per_country/country_stats.json')
        print(e)
        return 'False'

def load_countries_shape():
    global countries_shape
    with open('data/countries_shape.json') as f:
        countries_shape = json.load(f)

@app.route('/reload_covid_data')
def reload_covid_data():
    print('Reloading covid data')
    load_result = load_covid_data()
    return load_result

@app.route('/')
def show_dashboard():
    return render_template('index.html', covid_data=covid_data, countries_shape=countries_shape)

if __name__ == '__main__':
    print('Starting web_app')
    load_covid_data()
    load_countries_shape()
    app.run(host='0.0.0.0', port='5000')
