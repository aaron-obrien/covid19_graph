#!python3
import requests
import json
import csv
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import time

'''
COVID-19 Graph Plotter by Country

ESSENTIAL
- Software must take user input of a country
- Retrieve the API from the api.covid19api.com
- Convert this data from JSON format to a CSV, saving the file with the name of the country entered
- Produce a plot of log10(cases) over time

DESIRABLE
- Exception handling
    - If user enters incorrect country, direct user to list of countries + allow re-entry without running script.
    - Account for upper and lower cases (may innately do this)
    - Functionalise the code
'''

##  API retrieval + CSV production.

#User inputs country
country = raw_input('Please input a country for covid_19 analysis: ')

#Concatenate website for API request
api_website_input = ('https://api.covid19api.com/dayone/country/' + country + '/status/confirmed')

def date_changer(date_list):
    '''
    Prepares dates by converting the format to Months, for better x axes labels.
    '''
    Dates = date_list
    for date in Dates:
        if date.startswith('2020-02'):
            Dates[date] = 'February'
        elif date.startswith('2020-03'):
            Dates[date] = 'March'
        elif date.startswith('2020-04'):
            Dates[date] = 'April'
        elif date.startswith('2020-05'):
            Dates[date] = 'May'
        elif date.startswith('2020-06'):
            Dates[date] = 'June'
    
    return Dates

#API request
covid_api_data = requests.get(api_website_input)
print(covid_api_data)
#Check input exists
if covid_api_data:
    print ('API found')
    time.sleep(1)
    
    
    #Assign raw data from json format
    raw_covid_data = covid_api_data.json()

    #Set up csv file + writer
    csv_namer = ('covid_data_' + country + '.csv')
    covid_data = open(csv_namer, 'w')
    csv_writer = csv.writer(covid_data)


    #Initalise counter
    count=0

    #Write each row to csv
    for header in raw_covid_data:
        if count == 0:
            cur_header = header.keys()
            csv_writer.writerow(cur_header)
            count+=1

        csv_writer.writerow(header.values())

    covid_data.close()

    ## CSV reading and DataFrame production

    #Read csv into pandas dataframe + populate dataframe
    dataset = pd.read_csv(csv_namer)
    df = pd.DataFrame(dataset)

    #Reduce dataframe to Date and cases
    cols = []
    cols = ['Date', 'Cases']
    my_df = df.loc[:,cols]
    print(my_df)

    #Log the cases values (base 10) + insert to dataframe
    cases_for_log = df.loc[:,'Cases']
    logged_cases = cases_for_log.apply(math.log10)
    my_df['Log_Cases'] = logged_cases
    print(my_df.values)

    #Initialise dates code
    Col_Dates = []
    Col_Dates = my_df['Date']

    ## Plotting code
    #Plot graph
    my_df.plot(kind='line', x='Date', y='Log_Cases', color='blue')
    plt.xticks(rotation=270)
    plt.xlabel(date_changer(Col_Dates))
    plt.ylabel('Number of cases (log10 scale)')
    plt.yscale('log')
    plt.show()

else:
    print('API not found')


