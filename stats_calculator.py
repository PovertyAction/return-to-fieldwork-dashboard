import pandas as pd
import json
import numpy as np

from file_names import *

def compute_country_stats(show_prints=False):
    '''
    Using covid_data_raw.csv and manual_inputs.json, computes country stats to be shown in dashboard (country_stats.json)
    '''

    try:

        # Import csv file
        df0 = pd.read_csv(RAW_COVID_DATA_FILE, usecols= ['continent','location', 'date', 'total_cases', 'new_cases', 'new_cases_smoothed', 'positive_rate', 'population'])

        # Drop other countries
        ipalist = ['Paraguay', 'Dominican Republic', 'Colombia', 'Peru', 'Mexico', 'Burkina Faso', 'Mali', 'Sierra Leone', 'Liberia', 'Ghana', "Cote d'Ivoire", 'Nigeria', 'Tanzania', 'Zambia', 'Uganda', 'Rwanda', 'Malawi', 'Kenya', 'Myanmar', 'Philippines', 'Bangladesh']
        df = df0[df0.location.isin(ipalist)]

        # Sort by date
        df.sort_values(['location', 'date'], ascending=[True, False], inplace=True)


        # First step calculation
        aggregations = {
            "new_cases": [lambda t: t.head(3).mean(), lambda t: t.head(7).mean()],
            "new_cases_smoothed": [lambda t: t.iloc[7].mean()],
            "date": "first",
            "population": "first",
            'total_cases': "max",
            'continent': "first"
        }

        caldata = df.groupby('location', as_index=False).agg(aggregations)

        # Rename columns
        caldata.columns = ["_".join(x) for x in caldata.columns.ravel()]
        caldata.rename(columns = {'new_cases_<lambda_0>': 'caseavg_3day', 'new_cases_<lambda_1>': 'caseavg_7day', 'new_cases_smoothed_<lambda>': 'caseavg_7dayprev',
                                  'date_first': 'date', 'population_first': 'population', 'location_':'location', 'continent_first':'region'},
                                  inplace = True)

        # Second step calculation
        caldata["growthrate"] = (caldata['caseavg_7day'] - caldata['caseavg_7dayprev']) *100 / caldata['caseavg_7dayprev']
        caldata["cases_per_100000"] = caldata['total_cases_max']*100000 / caldata['population']
        caldata["douberate"] = pd.np.where((caldata.location.str.contains("Paraguay")) | (caldata.location.str.contains("Dominican Republic")),
                                              (np.log(2) / np.log((1 + caldata['growthrate']/100))), (7*70 / caldata['growthrate']))
        caldata["douberate"] = caldata["douberate"].fillna(0)
        caldata["status_3day"] =  np.where(caldata['caseavg_3day']<100, 1, 0)
        caldata["status_dbl"] =  np.where((caldata['douberate'] >=10) | (caldata['douberate']<=0), 1, 0)
        caldata["status_casepop"] =  np.where((caldata['cases_per_100000'] <50), 1, 0)
        caldata['statuscode'] = caldata.status_3day.map(str) + caldata.status_dbl.map(str) + caldata.status_casepop.map(str)

        # Third step - dashboard
        caldata["case_doubling_rate"] =  np.where((caldata["douberate"]<0) | (caldata["douberate"]>100), '>100', (caldata["douberate"].round()))
        caldata["new_cases_per_day"] = caldata['caseavg_3day'].astype(int)
        caldata['status'] = np.where(caldata.statuscode.str.contains("111"), "Yellow", "Red")
        caldata['cases_per_100000'] = caldata['cases_per_100000'].round(1)

        # Final output
        caldata = caldata[['location', 'region', 'status', 'case_doubling_rate', 'new_cases_per_day', 'cases_per_100000']]
        caldata = caldata.applymap(str)

        # Creating dictionary and exporting json
        caldata.set_index(['location'], inplace = True )
        d=caldata.to_dict('index')
        with open(COUNTRY_STATS_FILE, "w") as outfile:
            json.dump(d, outfile)

        if show_prints:
            print('Correctly computed country_stat.json')
        return True

    except Exception as e:
        print('Error when computing coutnry_stats.json')
        print(e)
        return False


if __name__ == '__main__':
    compute_country_stats()
