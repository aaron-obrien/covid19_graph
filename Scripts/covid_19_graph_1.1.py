#!python3
import requests
import csv
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import time
from datetime import datetime

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

#1.1 updates: Graph shows



def date_changer(date_list):
    '''
    Prepares dates by converting the format to Months, for better x axes labels.
    #TODO: Make this work
    '''

    for date in date_list:
        date_string = "2012-12-12 10:10:10"
        print (datetime.fromisoformat(date_string))

    return date_list


def get_covid_api_data(country):
    '''
    Retrieves the COVID 19 API data from an inputted country
    '''

    #Concatenate website for API request
    api_website_input = ('https://api.covid19api.com/dayone/country/' + country + '/status/confirmed')

    #API request
    covid_api_data = requests.get(api_website_input)
    print(covid_api_data)

    return covid_api_data

def make_csv(apidata,country_name):
    #Assign raw data from json format
    raw_covid_data = apidata.json()

    #Set up csv file + writer
    csv_namer = ('covid_data_' + country_name + '.csv')
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
    return csv_namer    

def plot_csv(csv_name):
    '''
    Reads a CSV into a pandas DataFrame, and plots the data using matplotlib
    '''
    #Read csv into pandas dataframe + populate dataframe
    dataset = pd.read_csv(csv_name)
    df = pd.DataFrame(dataset)

    #date_changer(df['Date'])

    plot_title = ('Covid-19 cases in ' + str(input_country.capitalize()) + ' since first case.')

    ## Plotting code
    #Plot graph
    df.plot(kind='line', x='Date', y='Cases', color='blue')
    plt.title(plot_title)
    plt.xticks(rotation=270)
    plt.ylabel('Number of cases (log10 scale)')
    plt.yscale('log')
    plt.show()
    return df

#User inputs country
input_country = raw_input('Please input a country for covid_19 analysis: ')
api_data = get_covid_api_data(input_country)
csv_name = make_csv(api_data, input_country)
plot_csv(csv_name)



