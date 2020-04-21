#!python3
# Tool to display a countries covid19 cases since day one.

import requests
import csv
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import math
from datetime import datetime
import os.path

'''
COVID-19 Graph Plotter by Country

ESSENTIAL
- Software must take user input of a country
- Retrieve the API from the api.covid19api.com
- Convert this data from JSON format to a CSV, saving the file with the name of the country entered
- Produce a plot of log10(cases) over time
'''

#1.1 updates: Graph shows
#1.2 updates: X axis presents much better, code is now functionalised
#1.3 TODO: Error handling

def countrychecker(inputted_country):
    '''
    Checks if the inputted country matches data in the API, returning a bool,.
    '''
    import pandas

    #Read permitted countries into dataframe
    country_api_path = ('https://api.covid19api.com/countries')
    df = pd.read_json(country_api_path)

    #Parse list checking if country matches the permtited list.
    is_iso_there = df['ISO2'].str.contains(inputted_country.upper(), regex = 'False').any()
    is_country_there = df['Country'].str.contains(inputted_country.capitalize(), regex = 'False').any()

    if is_iso_there == True:
        globalcountry = df.loc[df.ISO2 == inputted_country.upper(), 'Country']
        listtype = 'ISO'
        output_list = [True, globalcountry, listtype]
        return output_list

    elif is_country_there == True:
        globalcountry = df.loc[df.Country == inputted_country.upper, 'Country']
        globalISO = df.loc[df.ISO2 == inputted_country.upper, 'ISO2']
        listtype = 'Country'
        output_list = [True, globalISO, listtype]
        return output_list

    elif is_country_there == False or is_iso_there == False:
        return False

def get_covid_api_data(country_or_iso):
    '''
    Retrieves the COVID 19 API data from an inputted country
    '''

    #Concatenate website for API request
    api_website_input = ('https://api.covid19api.com/dayone/country/' + country_or_iso + '/status/confirmed')
    print(api_website_input)
    #API request
    try:
        covid_api_data = requests.get(api_website_input)
        if covid_api_data.status_code == 200:
            return covid_api_data
        else:
            print ('API data not retrieved. Please input a country or ISO2 code listed under https://api.covid19api.com/countries')
            raise SystemExit()
    except requests.exceptions.RequestException:
        print('API data was not retrieved. Please input a country or ISO2 code listed under https://api.covid19api.com/countries')
        raise SystemExit()

def make_csv(apidata,country_name):
    '''
    Writes retrieved COVID19 API data to a CSV file, named "covid_data_[countryname].csv"
    '''
    import datetime
    #Assign raw data from json format
    raw_covid_data = apidata.json()

    #Set up csv file + writer
    Current_Date_Formatted = datetime.datetime.today().strftime ('%d%m%Y')
    csv_namer = ('covid_data_' + Determined_country + '_' + str(Current_Date_Formatted) + '.csv')

    filepath = os.path.join(('../Data'),(csv_namer))
    covid_data = open(filepath, 'w')
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
    
    #Close file and return csv_name
    covid_data.close()
    return filepath

def plot_csv(csv_location):
    '''
    Reads a CSV into a pandas DataFrame, and plots the data using matplotlib
    '''
    import datetime
    import os

    if os.stat(csv_location).st_size > 10:
        print('Insufficient data is held for this Country/Region. Please rerun the script with a country or ISO2 code listed under https://api.covid19api.com/countries')

    #Read csv into pandas dataframe + populate dataframe
    dataset = pd.read_csv(csv_location)
    df = pd.DataFrame(dataset)
    df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)

    plot_title = ('Covid-19 cases in ' + (Determined_country.capitalize()) + ' since first case.')

    ## Plotting code
    #Plot graph
    df.plot(kind='line', x='Date', y='Cases', color='blue')
    plt.title(plot_title)
    plt.ylabel('Number of cases (log10 scale)')
    plt.xlabel('Time')
    plt.yscale('log')
    
    response = input('Would you like to save the graph? Type Y for yes or anything else for No. [Enter]     ')
    if response.upper() == 'Y' or 'Yes':
        Current_Date_Formatted = datetime.datetime.today().strftime ('%d%m%Y')
        figurefilepath = os.path.join(os.path.dirname(csv_location), Determined_country) 
        plt.savefig((figurefilepath + '_' + Current_Date_Formatted), format = 'pdf')
    plt.show()
    return df

#User inputs country
user_input = input('Please input a country or ISO2 code for covid_19 analysis: ')

#Checks if error handling output is list (expected outcome).
if type(countrychecker(user_input)) is list:
    listed_outputs = countrychecker(user_input)

    #ISO input
    if listed_outputs[2] == 'ISO':
        Determined_country = pd.Series.to_string(listed_outputs[1])
        if listed_outputs[0] == True:
            print('Corresponding country to ISO2 code: ', Determined_country)
            api_data = get_covid_api_data(user_input)
            csv_name = make_csv(api_data, Determined_country)
            plot_csv(csv_name)
        else:
            print('Country not recognised. Please input a country or ISO2 code listed under https://api.covid19api.com/countries')
    
    #Country input
    elif listed_outputs[2] == 'Country':
        if listed_outputs[0] == True:
            #Assigns the user inputted country to CSV + Plot making functions.
            Determined_country = user_input
            DeterminedISO = pd.Series.to_string(listed_outputs[1])
            print('Country found.')

            api_data = get_covid_api_data(Determined_country)
            csv_name = make_csv(api_data,user_input)
            plot_csv(csv_name)
        else:
            print('Country not recognised. Please input a country or ISO2 code listed under https://api.covid19api.com/countries')

elif type(countrychecker(user_input)) is bool:
    if countrychecker(user_input) == True:
        Determined_country = user_input
        api_data = get_covid_api_data(Determined_country)
        csv_name = make_csv(api_data, Determined_country)
        plot_csv(csv_name)
    if countrychecker(user_input) == False:
        print('Country not recognised. Please input a country or ISO2 code listed under https://api.covid19api.com/countries')

#TODO: pd.series.to_string to get just the country name.
#      Same with the ISO name.
#      Ensure the script takes common names (E.g. England, United Kingdom, United States.)
#      Provide fix to csv filesize error.