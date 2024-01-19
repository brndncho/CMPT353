import pandas as pd

totals = pd.read_csv('totals.csv').set_index(keys=['name'])
counts = pd.read_csv('counts.csv').set_index(keys=['name'])

# Lowest precipitation over the year
sumTotals = totals.sum(axis=1)
lowTotalPrecipitation = sumTotals.idxmin()
print("City with lowest total precipitation: ")
print(lowTotalPrecipitation)

# Average precipitation over each month
sumPrecipitationMonthly = totals.sum(axis=0)
sumObservationsMonthly = counts.sum(axis=0)
avgMonthlyPrecipitation = sumPrecipitationMonthly.divide(sumObservationsMonthly)
print("Average precipitation in each month: ")
print(avgMonthlyPrecipitation)

# Average precipitation over each city
sumCityCount = counts.sum(axis=1)
avgCityPrecipitation= sumTotals.divide(sumCityCount)
print("Average precipitation in each city: ")
print(avgCityPrecipitation)