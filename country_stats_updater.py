from flask import Flask
import requests

#Dashboard modules
import md5_generator
import covid_data_getter
import spreadsheet_data_getter
import stats_calculator
from file_names import * #Import all file names

debugging = True


def print_if_debugging(text):
    if debugging:
        print(text)


def update_web_server_country_stats():
    '''
    Call webserver endpoint to update its country stats
    '''
    try:
        response = requests.get('http://ec2-18-217-4-44.us-east-2.compute.amazonaws.com:5000/reload_covid_data')
        if response.status_code==200:
           print_if_debugging(f'Succes in updating country_stats.json in server. Response {response.text}')
           return True
        else:
           print_if_debugging(f'Error when updating country_stats.json in server. Response: {response}')
           return False
    except Exception as e:
        print('Error when calling web server for country_stats.json update')
        print(e)
        return False



def compute_country_stats_and_let_web_server_know():
    #Else, we do need to do the computations
    result_new_stats = stats_calculator.compute_country_stats(show_prints = debugging)

    #If computation was successful, let web server know that new stats are available
    if result_new_stats:
        update_web_server_country_stats()

def get_hash_old_covid_data():
    #Open file that keeps track of covid_data_hash
    try:
        hash_file = open(HASH_COVID_DATA_FILE,"r")
        hash = hash_file.readlines()[0]
        hash_file.close()
        print_if_debugging(f'Read {HASH_COVID_DATA_FILE} hash: {hash}')
        return hash
    except Exception as e:
        print(e)
        return False

def save_new_covid_data_hash(hash_new_covid_data):
    try:
        file = open(HASH_COVID_DATA_FILE, "w")
        file.write(hash_new_covid_data)
        file.close()
        print_if_debugging(f'Hash {hash_new_covid_data} written to {HASH_COVID_DATA_FILE}')
        return True
    except Exception as e:
        print('Error when saving new hash value')
        print(e)
        return False


def covid_data_has_not_changed(hash_new_covid_data):

    hash_old_covid_data = get_hash_old_covid_data()

    #For the same hash, no need to compute new country stats
    if hash_old_covid_data == hash_new_covid_data:
        print_if_debugging(f'Covid data has not changed, same hash value: {hash_old_covid_data}')
        return True
    else:
        print_if_debugging(f'New covid data. New hash {hash_new_covid_data}, old hash {hash_old_covid_data}')
        return False

def update_for_new_covid_data():
    '''
    This method is in charge of updating country_stats.json based on possible new covid data. In particular, it will

    1. Download new covid data
    2. Check if new covid data is different to old, else, return
    3. Compute new country_stats.json
    4. Tell web server that new stats are available

    A scheduler should run this process every 8 hours
    '''

    #Download new copy
    covid_data_getter.download_covid_data(show_prints=debugging)

    #Get its hash
    hash_new_covid_data = md5_generator.get_file_md5(RAW_COVID_DATA_FILE, show_prints=debugging)

    #Check if new copy is different to previous one
    if covid_data_has_not_changed(hash_new_covid_data):
        return

    #Else, save hash of new copy and compute new stats and let server know
    save_new_covid_data_hash(hash_new_covid_data)

    compute_country_stats_and_let_web_server_know()

# ENDPOINT TO UPDATE DATA WHENEVER THERE IS A CHANGE IN SPREADSHEET

#Flask app to facilitate endpoint
app = Flask(__name__)

#This endpoint will be called from gsheets whenever there is a change in the data
@app.route('/new_spreadsheet_data')
def update_for_new_spreadsheet_data():

    #Download new spreadsheet data
    spreadsheet_data_getter.download_spreadsheet_data("Return to fieldwork", show_prints=debugging)

    compute_country_stats_and_let_web_server_know()

if __name__ == '__main__':
    # app.run()
    update_for_new_covid_data()
