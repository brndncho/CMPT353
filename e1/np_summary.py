import numpy as np

data = np.load('e1/monthdata.npz')
totals = data['totals']
counts = data['counts']

# Lowest precipitation over the year
sum_totals = np.sum(totals, axis=1)
lowTotalPrecipitation = np.argmin(sum_totals)
print("Row with lowest total precipitation: ")
print(lowTotalPrecipitation)

# Average precipitation over each month
sumPrecipitationMonthly = np.sum(totals, axis=0)
sumObservationsMonthly = np.sum(counts, axis=0)
avgMonthlyPrecipitation = np.divide(sumPrecipitationMonthly, sumObservationsMonthly)
print("Average precipitation in each month: ")
print(avgMonthlyPrecipitation)