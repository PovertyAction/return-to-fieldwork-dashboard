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



# Setting up aws server

Copy google sheets secret key to server
`scp -i credentials/aws-key-pair.pem client_secret.json ubuntu@ec2-18-217-4-44.us-east-2.compute.amazonaws.com:/home/ubuntu`

ssh to ec2 instance
`chmod 400 credentials/aws-key-pair.pem`
`ssh -i credentials/aws-key-pair.pem ubuntu@ec2-18-217-4-44.us-east-2.compute.amazonaws.com`

`sudo apt update`

`sudo apt install python3-pip`

`github clone https://github.com/PovertyAction/return-to-fieldwork-dashboard.git`

`pip3 install -r requirements.txt`

install tmux (only first time)
`sudo apt install tmux`

## Setting up web app

create a tmux session for the web app and run in
`tmux web_app`
`python3 web_app.py`

Remember to enable TCP calls from anywhere to port 5000 in aws security group associated to this instance.
Rule: Custom TCP	TCP	5000 Anywhere
