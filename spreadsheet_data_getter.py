#Reference https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
#Then I had to change scope accoring to https://github.com/burnash/gspread/issues/513
#Lastly I also had to enable Google Sheets API in the console

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from file_names import *
import warnings



def get_gspread_client():
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name(GSHEETS_CREDENTIALS, scope)
    client = gspread.authorize(creds)
    return client


def create_dictionary_with_countries(workbook, sheet_name):
    countries_info = {}

    sheet = workbook.worksheet(sheet_name)
    #First row contains countries names
    countries_names_row = sheet.get_all_values()[0]

    #For each country, create an empty dictionary where we will save data
    for index, country_name in enumerate(countries_names_row):
        #Skip first element (Date (m/d/yyyy))
        if index == 0:
            continue
        countries_info[country_name] = {}

    return countries_info

def add_data_from_sheet(workbook, sheet_name, countries_dict):

    sheet = workbook.worksheet(sheet_name)#"Outbreak_status" or "Govt.Instruction"

    #Get first row (header), which contains countries names
    countries_names_row = sheet.get_all_values()[0]

    #Get last row, which contains latest info
    last_row = sheet.get_all_values()[-1]

    for index, country_name in enumerate(countries_names_row):
        #Skip first element (Date (m/d/yyyy))
        if index == 0:
            continue
        #Save info in dictionary
        countries_dict[country_name][sheet_name.lower()] = last_row[index]

    return countries_dict


def add_override_status(workbook, sheet_name, countries_info):

    sheet = workbook.worksheet(sheet_name)

    pairs_country_and_override_status = sheet.get_all_values()

    for index, country_status in enumerate(pairs_country_and_override_status):
        #Skip header
        if index == 0:
            continue

        #Get country and status from data
        country = country_status[0]
        status = country_status[1]

        #Write info in dict
        countries_info[country]['override_status'] = status

    return countries_info

def save_dict_to_json_file(dict, file_name):
    with open(file_name, 'w') as fp:
        json.dump(dict, fp)

def download_spreadsheet_data(workbook_name, show_prints=False):

    #Removing gspread warnings
    warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

    try:
        #Get access to workbook
        client = get_gspread_client()
        workbook = client.open(workbook_name)

        #Dictionary where to keep all collected information
        countries_info = create_dictionary_with_countries(workbook, "Outbreak_status")

        #Add data from different sheets in workbook
        countries_info = add_data_from_sheet(workbook, "Outbreak_status", countries_info)
        countries_info = add_data_from_sheet(workbook, "Govt.Instruction", countries_info)
        countries_info = add_override_status(workbook, "Override Status", countries_info)

        #Save dict to json
        save_dict_to_json_file(countries_info, MANUAL_INPUTS_FILE)

        if show_prints:
            print('Correctly downloaded and saved manual_inputs from speadsheet')
            # print(countries_info)

        # client.close()
        return True
    except Exception as e:
        print('Error when downloading manual_inputs from spreadsheet')
        print(e)
        return False

if __name__ == '__main__':

    download_spreadsheet_data("Return to fieldwork")
