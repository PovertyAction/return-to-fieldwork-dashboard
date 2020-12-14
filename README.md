# Update country_stats for new covid data

Every 8 hours:

Scheduler will run country_stats_updater.update_for_new_covid_data()

Internally, this will call:
- covid_data_getter.download_covid_data()
- stats_calculator.compute_country_stats()
- update_web_server_country_stats()

# Update country_stats for new manual inputs

Whenever there is a change in the spreadsheet, aka, someone manually wrote information, we will trigget a call to country_stats_updater.update_for_spreadsheet_data()

Internally, this will call:
- spreadsheet_data_getter.download_spreadsheet_data()
- stats_calculator.compute_country_stats()
- update_web_server_country_stats()

<!-- # Modules

## pull_spreadsheet_data.py

https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html -->

# Setup

`python3 web_app.py`
