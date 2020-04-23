#!python3
# Tool to display a countries covid19 cases since day one.

import requests
import csv
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

def countrychecker(input_val):
    '''
    Checks if the inputted country matches data in the API, returning a bool,.
    '''
    import pandas as pd
    import requests

    #Read listed countries into dataframe from API.
    country_api_path = ('https://api.covid19api.com/countries')
    df = pd.read_json(country_api_path)

    ISO2_list, countries_list = [], []    #Initialise lists
    ISO2_list, countries_list = df['ISO2'].values.tolist(), df['Country'].values.tolist()    #Assign ISO2 and country lists with values from dataframe
    
    if input_val.capitalize() in countries_list:  #Check ISO2 in list
        return_ISO2 = df.loc[df.Country == input_val.upper(), 'ISO2']    #Retrieve ISO from ISO list///
        listtype = 'Country'
        output_list = [True, return_ISO2, listtype]
        return output_list

    elif input_val.upper() in ISO2_list:  #Check country in API retrieved list.
        return_country = df.loc[df.ISO2 == input_val.upper(), 'Country']    #Retrieve country name from list, where an ISO2 code is inputted (for graphing purposes).
        listtype = 'ISO'
        output_list = [True, return_country, listtype]
        return output_list
        
    else:
        return False


    #is_iso_there = df['ISO2'].str.contains(input_val.upper(), regex = 'False').any()    #Check ISO against list
    #is_country_there = df['Country'].str.contains(input_val.capitalize(), regex = 'False').any()    #Check country against list

def get_covid_api_data(country_or_iso):
    '''
    Retrieves the COVID 19 API data from an inputted country
    '''
    import requests

    api_website_input = ('https://api.covid19api.com/dayone/country/' + country_or_iso + '/status/confirmed')   #Concatenate website for API request
    covid_api_data = requests.get(api_website_input)    #API request

    if covid_api_data.status_code == 200:   #API error handling
        return covid_api_data
    else:
        print ('API data not retrieved. Please input a country or ISO2 code listed under https://api.covid19api.com/countries')
        raise SystemExit()

def make_csv(apidata,country_name):
    '''
    Writes retrieved COVID19 API data to a CSV file, named "covid_data_[countryname].csv"
    '''
    import datetime
    import os.path
    import json
    
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

    #Loop over each row, + write to csv
    for header in raw_covid_data:
        if count == 0:
            cur_header = header.keys()
            csv_writer.writerow(cur_header)
            count+=1

        csv_writer.writerow(header.values())
    
    
    covid_data.close()  #Close file
    return filepath     #Return CSV path

def plot_csv(csv_location):
    '''
    Reads a CSV into a pandas DataFrame, and plots the data using matplotlib
    '''
    import datetime
    import os
    import matplotlib.pyplot as plt
    import pandas

    if os.stat(csv_location).st_size < 10:
        print('Insufficient data is held for this Country/Region. Please rerun the script with a country or ISO2 code listed under https://api.covid19api.com/countries')
        raise SystemExit()

    #Read csv into pandas dataframe + populate dataframe
    dataset = pd.read_csv(csv_location)    #Read CSV
    df = pd.DataFrame(dataset)  #Read in DF 
    df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)    #Date formatting for plot

    plot_title = ('Covid-19 cases in ' + (Determined_country.capitalize()) + ' since first case.')  #Plot tile

    #Plot graph
    df.plot(kind='line', x='Date', y='Cases', color='blue')
    plt.title(plot_title)
    plt.ylabel('Number of cases (log10 scale)')
    plt.xlabel('Time')
    plt.yscale('log')
    plt.show()

    response = input('Would you like to save the graph? Type Y for yes or anything else for No. [Enter]    ')   #User choice for saving figure
    if response.lower() == 'y' or 'yes':
        Current_Date_Formatted = datetime.datetime.today().strftime ('%d%m%Y')  #Format date for saving figure
        figurefilepath = os.path.join(os.path.dirname(csv_location), Determined_country)    #Define path to save figure
        plt.savefig((figurefilepath + '_' + Current_Date_Formatted), format = 'pdf')    #Save figure
    return df


user_input = str(input('Please input a country or ISO2 code for covid_19 analysis: '))   #User inputs country
listed_outputs = countrychecker(user_input) #Outputs listed for error checking
try:
    if listed_outputs[2] == 'ISO':  #ISO input
        Determined_country = listed_outputs[1].tolist()[0]
        print(Determined_country)
        if listed_outputs[0] == True:
            print('Corresponding country to ISO2 code: ', Determined_country)
            api_data = get_covid_api_data(user_input)
            csv_name = make_csv(api_data, Determined_country)
            plot_csv(csv_name)
        else:
            print('Country not recognised. Please input a country or ISO2 code listed under https://api.covid19api.com/countries')

    elif listed_outputs[2] == 'Country':    #Country input
        if listed_outputs[0] == True:
            #Assigns the user inputted country to CSV + Plot making functions.
            Determined_country = user_input
            print('Country found.')

            api_data = get_covid_api_data(Determined_country)
            csv_name = make_csv(api_data,user_input)
            plot_csv(csv_name)
        else:
            print('Country not recognised. Please input a country or ISO2 code listed under https://api.covid19api.com/countries')

except(TypeError):
    print('Country not found. Please input a country or ISO2 code listed under https://api.covid19api.com/countries')
    raise SystemExit()


### Excess code:
'''
            ISO_match = difflib.get_close_matches(input_val, ISO2_list, n=1, cutoff=0.6)
            if ISO_match == []:
                ISO_match = '[\'N/A\']'
            country_match = difflib.get_close_matches(input_val, countries_list, n=1, cutoff=0)
            if country_match == []:
                country_match = '[\'N/A\']'
            second_resp = print('Country/ISO2 code not found against list. Closest ISO2 match:', ISO_match, '. Closest country match:', country_match, '. Type 1 to proceed with the ISO match or 2 to proceed with the country match.')
            
            if second_resp == 1:
                input_val = ISO_match
            elif second_resp == 2:
                input_val = country_match


            count +=1
            #return False
'''