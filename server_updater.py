import requests
import sys

debugging=True
def print_if_debugging(text):
    if debugging:
        print(text, file=sys.stdout)

def update_web_server_country_stats():
    '''
    Call webserver endpoint to update its country stats
    '''
    try:
        response_prod = requests.get('http://ec2-18-217-4-44.us-east-2.compute.amazonaws.com:80/reload_country_stats')
        
        response_dev = requests.get('http://ec2-18-217-4-44.us-east-2.compute.amazonaws.com:5000/reload_country_stats')
         
        if response_dev.status_code==200:
           print_if_debugging(f'Succes in updating country_stats.json in dev server. Response {response_dev.text}')
        else:
           print_if_debugging(f'Error when updating country_stats.json in dev server. Response: {response_dev.text}')
        
        if response_prod.status_code==200:
           print_if_debugging(f'Succes in updating country_stats.json in production server. Response {response_prod.text}')
           return True
        else:
           print_if_debugging(f'Error when updating country_stats.json in production server. Response: {response_prod.text}')
           return False
    except Exception as e:
        print('Error when calling web server for country_stats.json update')
        print(e)
        return False
