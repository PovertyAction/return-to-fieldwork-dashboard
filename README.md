# Return to field work dashboard

Website that present IPA country status for returning to field work.

The system has 3 main components:

* A website that presents the dashboard based on already computed country_stats.json
* A process that collects covid data every 8 hours and re computes country_stats.json
* A process that captures changes in a spreadsheet where users can input data which overrides country_stats.json

## System overview

![](system_components_diagram.png)

### covid data updater

Every 8 hours:

Scheduler will run country_stats_updater.update_for_new_covid_data()

Internally, this will call:

- covid_data_getter.download_covid_data()
- stats_calculator.compute_country_stats()
- update_web_server_country_stats()

### spreadsheet data updater

Whenever there is a change in [this](https://docs.google.com/spreadsheets/d/1xvFTrmbjrJbYDHKej_AsEcCWEwsM7JCGxCdzYPZRQgk/edit#gid=1855212233) spreadsheet, aka, someone manually wrote information, we will trigget a call to country_stats_updater.update_for_spreadsheet_data()

Internally, this will call:

- spreadsheet_data_getter.download_spreadsheet_data()
- stats_calculator.compute_country_stats()
- update_web_server_country_stats()

## Setup

### Setting up aws server

Copy google sheets secret key to server
`scp -i credentials/aws-key-pair.pem client_secret.json ubuntu@ec2-18-217-4-44.us-east-2.compute.amazonaws.com:/home/ubuntu`

ssh to ec2 instance
`chmod 400 credentials/aws-key-pair.pem`
`ssh -i credentials/aws-key-pair.pem ubuntu@ec2-18-217-4-44.us-east-2.compute.amazonaws.com`

Install dependencies in server
`sudo apt update`
`sudo apt install python3-pip`
`sudo apt-get install python3-venv`
`python3 -m venv venv`
`source venv/bin/activate`
`pip3 install -r requirements.txt`
`github clone https://github.com/PovertyAction/return-to-fieldwork-dashboard.git`
`pip3 install -r requirements.txt`
`sudo apt install tmux`

### Setting up sessions for each component using tmux

#### web app
`tmux new -s web_app`
`python3 web_app.py`

Enable TCP calls from anywhere to port 5000 in aws security group associated to this instance.
Rule: Custom TCP TCP 5000 Anywhere

## spreadsheet data updater

`tmux new -s spreadsheet_data_updater`
`python3 spreadsheet_data_updater.py`

Remember to enable TCP calls from anywhere to port 5002 in aws security group associated to this instance.
Rule: Custom TCP TCP 5002 Anywhere

## covid data updater

Setup cron to run `covid_data_updater.py` every 8 hours and keep log in `covid_data_updater_log.txt`

```
crontab -e
#Write down in the end of the crontab file the following line:
0 */8 * * * /usr/bin/python3 /home/ubuntu/return-to-fieldwork-dashboard/covid_data_updater.py >> /home/ubuntu/return-to-fieldwork-dashboard/covid_data_updater_log.txt
```
You can check what has crontab run with:
```
tail /var/log/syslog
```
Remember to use absolute routes
