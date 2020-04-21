#!python3
def gather_countries():
    '''
    Function to take multiple inputs from the user and append them to a list, which is returned.
    '''

    ###Developer notes: Tested and works.
    
    country_list = []
    cur_country = ''
    while cur_country != ('n'):
        cur_country = input('input countries. If no more countries, please click n then enter.')
        if cur_country == 'n':
            break
        country_list.append(cur_country)
    return country_list

def error_check_countries(countries):
    '''
    Checks the countries inputted from gather_countries() exists in the list of countries on the API data.
    '''

    ###############################TODO: Make this work#################################################

    import requests
    import pandas as pd

    #Retrieve countries from API, loads data to json.
    listed_countries = requests.get('https://api.covid19api.com/countries')
    country_data = listed_countries.json()

    #Loop over all inputted countries
    for input_country in countries:
        print(input_country)

        #Compares each inputted country against list retrieved from API.
        if input_country not in country_data:
            print('Country ', input_country, 'was not found. This will not be displayed on the graph.')
            countries.remove(input_country)
    print(countries)
    
    return countries

def get_covid_api_data(country):
    '''
    Retrieves the COVID 19 API data from an inputted country
    '''
    import requests

    #Concatenate website for API request
    api_website_input = ('https://api.covid19api.com/dayone/country/' + country + '/status/confirmed')

    #API request
    covid_api_data = requests.get(api_website_input)
    print(covid_api_data)
    return covid_api_data

def plot_csv(csv_name):
    '''
    Reads a CSV into a pandas DataFrame, and plots the data using matplotlib
    '''
    #Read csv into pandas dataframe + populate dataframe
    dataset = pd.read_csv(csv_name)
    df = pd.DataFrame(dataset)
    df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)

    plot_title = ('Covid-19 cases in ' + str(input_country.capitalize()) + ' since first case.')

    ## Plotting code
    #Plot graph
    df.plot(kind='line', x='Date', y='Cases', color='blue')
    plt.title(plot_title)
    plt.ylabel('Number of cases (log10 scale)')
    plt.xlabel('Time')
    plt.yscale('log')
    plt.show()
    return df


raw_input_countries = gather_countries()
#cleaned_countries = error_check_countries(raw_input_countries)

api_country_list = []
for country in raw_input_countries:
    var_name = str(country) + '_api_data'
    cur_country_api_data = get_covid_api_data(country)
    api_country_list.append(cur_country_api_data)
print(api_country_list)
