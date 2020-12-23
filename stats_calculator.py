import pandas as pd
import json
import numpy as np
import warnings
np.seterr(divide = 'ignore')
from file_names import *
import sys
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
        caldata["douberate"] = (np.log(2) / np.log((1 + caldata['growthrate']/100))).where((caldata.location.str.contains("Paraguay"))
                                                | (caldata.location.str.contains("Dominican Republic")),
                                                (7*70 / caldata['growthrate']))
        caldata["douberate"] = caldata["douberate"].fillna(0)
        caldata["status_3day"] = caldata["caseavg_3day"].apply(lambda x : 1 if x < 100 else 0)
        caldata["status_dbl"] = caldata["douberate"].apply(lambda x : 1 if (x >= 10 or x <= 0) else 0)
        caldata["status_casepop"] = caldata["cases_per_100000"].apply(lambda x : 1 if x < 50 else 0)
        caldata['statuscode'] = caldata.status_3day.map(str) + caldata.status_dbl.map(str) + caldata.status_casepop.map(str)

        # Third step - dashboard
        caldata["case_doubling_rate"] = caldata["douberate"].apply(lambda x : '>100' if (x <0 or x > 100) else round(x, 1))
        caldata["new_cases_per_day"] = caldata['caseavg_3day'].round(0).astype(int)
        caldata['status'] = caldata["statuscode"].apply(lambda x : "Yellow" if x == "111" else "Red")
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
            print('Correctly computed country_stats.json', file=sys.stdout)
        return True

    except Exception as e:
        print(f'Error when computing country_stats.json: {e}', file=sys.stdout)
        return False


if __name__ == '__main__':
    compute_country_stats(show_prints=True)


#EOF
