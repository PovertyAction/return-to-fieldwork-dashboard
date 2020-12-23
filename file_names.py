#NAME OF FILES
import os

def get_abs_path(relative_path):
   return os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),relative_path))

HASH_COVID_DATA_FILE = get_abs_path('./data/covid_data_md5.txt')

RAW_COVID_DATA_FILE = get_abs_path('./data/covid_data_raw.csv')

MANUAL_INPUTS_FILE = get_abs_path('./data/manual_inputs.json')

GSHEETS_CREDENTIALS = get_abs_path('./credentials/client_secret.json')

COUNTRY_STATS_FILE = get_abs_path('./data/country_stats.json')
