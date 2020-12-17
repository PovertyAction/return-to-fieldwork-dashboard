import requests

debugging=True
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
