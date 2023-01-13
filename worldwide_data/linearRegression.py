from sklearn.linear_model import LinearRegression
import csv
import numpy as np
from datetime import datetime
def getCountryData():
    """Function to retrieve the actual country energy consumption data by performing a linear regression on historical data

    Returns:
        countries dictionary: a dictionary with the lowercase string of the country as the key and the actual energy consumption as the value
    """    
    rows = []
    # Retrieve historical data from csv, in the future to change with dataset on the internet or database source
    html = open('energy_data.csv', "r")
    # populate the rows list with per country data
    with html as csvfile:
        scanner = csv.reader(csvfile)
        scanner.__next__()
        for country in scanner:
            rows.append(country)

    dataOfCountries = {}
    # Group data per country
    for row in rows:
        if dataOfCountries.__contains__(row[0]):
            dataOfCountries.get(row[0]).get('years').append(int(row[2]))
            dataOfCountries.get(row[0]).get('consumption').append(float(row[3]))
        else:
            dataOfCountries[row[0]] = {}
            dataOfCountries.get(row[0])['years'] = []
            dataOfCountries.get(row[0])['years'].append(int(row[2]))
            dataOfCountries.get(row[0])['consumption'] = []
            dataOfCountries.get(row[0])['consumption'].append(float(row[3]))
    # create numpy array of x y values per year and consumption per country
    for country in dataOfCountries.keys():
        x = np.array(dataOfCountries.get(country).get('years')).reshape((-1, 1))
        y = np.array(dataOfCountries.get(country).get('consumption'))
        #create a linear regression model
        model = LinearRegression().fit(x, y)
        #get the last year data from country
        latestYear = dataOfCountries.get(country).get('years')[-1]
        # add the data missing from the last year up to now
        actualYear = datetime.now().year
        for curYear in range(latestYear + 1, actualYear):
            dataOfCountries.get(country).get('years').append(curYear)
            dataOfCountries.get(country).get('consumption').append(model.predict([[curYear]]).tolist()[0])

    countries = {}
    # Get the latest consumption data in a dictionary of keys as the country and values as the consumption of actual year
    for key in dataOfCountries.keys():
        countries[key.lower()] = round(float(dataOfCountries.get(key).get('consumption')[-1]),2)
    return countries