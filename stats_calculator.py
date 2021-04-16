import pandas as pd
import json
import numpy as np
import warnings
np.seterr(divide = 'ignore')
from file_names import *
import sys
import datetime
#Set warnings as errors
warnings.filterwarnings("error")

def compute_country_stats(show_prints=False):
    '''
    Using covid_data_raw.csv and manual_inputs.json, computes country stats to be shown in dashboard (country_stats.json)
    '''

    try:

       # Import csv file
        df0 = pd.read_csv(RAW_COVID_DATA_FILE, usecols= ['continent','location', 'date', 'total_cases', 'new_cases', 'new_cases_smoothed', 'positive_rate', 'population'])

        # Drop other countries
        ipalist = ['Paraguay', 'Dominican Republic', 'Colombia', 'Peru', 'Mexico', 'Burkina Faso', 'Mali', 'Sierra Leone', 'Liberia', 'Ghana', "Cote d'Ivoire", 'Nigeria', 'Tanzania', 'Zambia', 'Uganda', 'Rwanda', 'Malawi', 'Kenya', 'Myanmar', 'Philippines', 'Bangladesh']
        df1 = df0[df0.location.isin(ipalist)]

        # Sort by date
        df = df1.sort_values(['location', 'date'], ascending=[True, False])


        # First step calculation
        aggregations = {
            "new_cases": [lambda t: t.head(3).mean(), lambda t: t.head(7).mean()],
            "new_cases_smoothed": [lambda t: t.iloc[7].mean()],
            "date": "first",
            "population": "first",
            'total_cases': "max",
            'continent': "first",
            'positive_rate': "first"
        }

        caldata = df.groupby('location', as_index=False).agg(aggregations)

        # Rename columns
        caldata.columns = ["_".join(x) for x in caldata.columns.ravel()]
        caldata.rename(columns = {'new_cases_<lambda_0>': 'caseavg_3day', 'new_cases_<lambda_1>': 'caseavg_7day',
                                  'new_cases_smoothed_<lambda>': 'caseavg_7dayprev', 'date_first': 'date', 'population_first': 'population',
                                  'location_':'location', 'continent_first':'region', 'positive_rate_first':'positive_rate', 'date_first':'date'},
                                  inplace = True)

        # Second step calculation
        caldata["growthrate"] = (caldata['caseavg_7day'] - caldata['caseavg_7dayprev']) *100 / caldata['caseavg_7dayprev']
        caldata["cases_per_100000"] = caldata['total_cases_max']*100000 / caldata['population']
        caldata["douberate"] = (np.log(2) / np.log((1 + caldata['growthrate']/100))).where((caldata.location.str.contains("Paraguay"))
                                                | (caldata.location.str.contains("Dominican Republic")),
                                                (7*70 / caldata['growthrate']))
        caldata["douberate"] = caldata["douberate"].fillna(0)
        caldata["status_3day"] = caldata["caseavg_3day"].apply(lambda x : 1 if x <= 100 else 0)
        caldata["status_dbl"] = caldata["douberate"].apply(lambda x : 1 if (x >= 10 or x <= 0) else 0)
        caldata["status_casepop"] = caldata["cases_per_100000"].apply(lambda x : 1 if x <= 50 else 0)
        caldata["positive_rate_dum"] = caldata["positive_rate"].apply(lambda x : 0 if (x > 0.05) else 1 if (x <= 0.05) else '') 
        caldata['statuscode'] = caldata.status_3day.map(str) + caldata.status_dbl.map(str) + caldata.positive_rate_dum.map(str)


        # Third step - dashboard
        caldata["case_doubling_rate"] = caldata["douberate"].apply(lambda x : '>100' if (x <0 or x > 100) else round(x, 1))
        caldata["new_cases_per_day"] = caldata['caseavg_3day'].round(0).astype(int)
        caldata['status'] = caldata["statuscode"].apply(lambda x : "Yellow" if x == "111" or x == "11" else "Red")
        caldata['cases_per_100000'] = caldata['cases_per_100000'].round(1)
        caldata["positive_rate"] = (caldata['positive_rate'])*100
        caldata["positive_rate"] = caldata['positive_rate'].round(2)
        

        # Final output
        caldata = caldata[['location', 'region', 'status', 'case_doubling_rate',  'new_cases_per_day', 'cases_per_100000', 'positive_rate', 'date']]
        caldata = caldata.applymap(str)
        caldata['positive_rate'] = caldata['positive_rate'].apply(lambda x : '' if x=='nan' else x+'%')
        caldata1 = caldata.sort_values(['region', 'location'], ascending=[True, True])
        caldata = caldata1 

        # Import manual_inputs.json
        with open(MANUAL_INPUTS_FILE) as f:
          manual_inputs = json.load(f)

        #manual_data = pd.json_normalize(manual_inputs)
        manual_data = pd.DataFrame.from_dict(manual_inputs, orient='index')
        manual_data.reset_index(level=0, inplace=True)
        manual_data.rename(columns = {'index': 'location'}, inplace = True)

        # Merge with existing data
        data = caldata.merge(manual_data, on='location')

        # Override status
        data = data.replace('', np.nan)
        data["override_status"] = data['override_status'].fillna(data['status'])
        del data['status']
        data.rename(columns = {'override_status': 'status',
                               'govt.instruction': 'government_restrictions',
                               'outbreak_status': 'subnational_outbreak_status'
                               }
                            , inplace = True)
        data = data.replace(np.nan, '')

        #Remove non-printable chars from columns, given thay are hard to print in map
        for col in ['status', 'government_restrictions', 'subnational_outbreak_status', 'link_local_data']:
            data[col] = data[col].apply(lambda x: ''.join([" " if ord(i) < 32 or ord(i) > 126 else i for i in x]))


        # Creating dictionary and exporting json
        data.set_index(['location'], inplace = True )
        d=data.to_dict('index')

        # Exporting final data file
        with open(COUNTRY_STATS_FILE, "w") as outfile:
            json.dump(d, outfile)

        if show_prints:
            print('Correctly computed country_stats.json', file=sys.stdout)
        return True

    except Exception as e:
        print(f'Error when computing country_stats.json: {e}', file=sys.stdout)
        return False


if __name__ == '__main__':
    compute_country_stats(show_prints=True)


#EOF
