from flask import Flask, render_template
import pandas as pd
import json
import numpy as np
import sys

app = Flask(__name__)

def load_country_stats(show_prints=False):
    global country_stats
    try:
        with open('data/country_stats.json') as f:
            country_stats = json.load(f)
        if show_prints:
            print('Correctly loaded country_stats', file=sys.stdout)
        return 'True'
    except Exception as e:
        print('Error when downloading country_stats.json', file=sys.stdout)
        print(e, file=sys.stdout)
        return 'False'

def load_countries_shape():
    global countries_shape
    with open('data/countries_shape.json') as f:
        countries_shape = json.load(f)

@app.route('/reload_country_stats')
def reload_covid_data():
    print('Reloading country_stats')
    load_result = load_country_stats()
    return load_result

@app.route('/')
def show_dashboard():
    load_country_stats()
    return render_template('index.html', country_stats=country_stats, countries_shape=countries_shape)

load_country_stats()
load_countries_shape()

if __name__ == '__main__':
    print('Starting web_app', file=sys.stdout)
    app.run(host='0.0.0.0', port='5000')
