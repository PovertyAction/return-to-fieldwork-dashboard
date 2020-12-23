from flask import Flask
import spreadsheet_data_getter
import server_updater
import stats_calculator
import sys

debugging=True

#Flask app to facilitate endpoint
app = Flask(__name__)

#This endpoint will be called from gsheets whenever there is a change in the data
@app.route('/new_spreadsheet_data')
def update_for_new_spreadsheet_data():

    #Download new spreadsheet data
    download_data_status = spreadsheet_data_getter.download_spreadsheet_data("Return to fieldwork", show_prints=debugging)
    if not download_data_status:
        return 'Error when downloading spreadsheet data'

    #Compute country stats considering there is new data
    result_new_stats = stats_calculator.compute_country_stats(show_prints = debugging)
    if not result_new_stats:
        return 'Error when computing new country stats'

    #Let web server know that new stats are available
    update_status = server_updater.update_web_server_country_stats()
    if update_status:
        return 'Success'
    else:
        return 'Error updating country stats in server'


if __name__ == '__main__':
    print('Starting new_spreadsheet_data listener', file=sys.stdout)
    app.run(host='0.0.0.0', port='5002')
