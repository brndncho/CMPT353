import numpy as np

data = np.load('monthdata.npz')
totals = data['totals']
counts = data['counts']

# Lowest precipitation over the year
sum_totals = np.sum(totals, axis=1)
lowTotalPrecipitation = np.argmin(sum_totals)
print("Row with lowest total precipitation: ")
print(lowTotalPrecipitation)

# Average precipitation over each month
sumPrecipitationMonthly = np.sum(totals, axis=0) # by columns
sumObservationsMonthly = np.sum(counts, axis=0)
avgMonthlyPrecipitation = np.divide(sumPrecipitationMonthly, sumObservationsMonthly)
print("Average precipitation in each month: ")
print(avgMonthlyPrecipitation)

# Average precipitation over each city
sumCityCount = np.sum(counts, axis=1) # by rows
avgCityPrecipitation = np.divide(sum_totals, sumCityCount)
print("Average precipitation in each city: ")
print(avgCityPrecipitation)

# Total precipitation for ea ch quarter in each city
nRows = len(totals)
initReshape = np.reshape(totals, (4*nRows,3))
sumByCityQuarters = np.sum(initReshape, axis=1)
sumByCityQuarters = np.reshape(sumByCityQuarters, (nRows, 4))
print("Quarterly precipitation totals: ")
print(sumByCityQuarters)