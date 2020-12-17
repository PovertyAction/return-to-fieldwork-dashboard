from flask import Flask
import spreadsheet_data_getter
import server_updater

debugging=True

#Flask app to facilitate endpoint
app = Flask(__name__)

#This endpoint will be called from gsheets whenever there is a change in the data
@app.route('/new_spreadsheet_data')
def update_for_new_spreadsheet_data():

    #Download new spreadsheet data
    download_data_status = spreadsheet_data_getter.download_spreadsheet_data("Return to fieldwork", show_prints=debugging)

    if download_data_status:
        update_status = server_updater.update_web_server_country_stats()
        if update_status:
            return 'Success'
        else:
            return 'Error'
    else:
        return 'Error'



if __name__ == '__main__':
    print('Starting new_spreadsheet_data listener')

    app.run(host='0.0.0.0', port='5001')#debug=True, threaded=True,
