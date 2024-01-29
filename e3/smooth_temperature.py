import pandas as pd 
import matplotlib.pyplot as plt 
import sys
from statsmodels.nonparametric.smoothers_lowess import lowess

filename1 = sys.argv[1]

cpu_data = pd.read_csv(filename1, parse_dates=['timestamp'])

# LOESS Smoothing
loess_smoothed = lowess(cpu_data['temperature'], cpu_data['timestamp'], frac=0.05)
plt.figure(figsize=(12, 4))
plt.plot(cpu_data['timestamp'], cpu_data['temperature'], 'b.', alpha=0.5)
plt.plot(cpu_data['timestamp'], loess_smoothed[:, 1], 'r-')
plt.show()
#plt.savefig('cpu.svg')

# Kalman Smoothing
