import pandas as pd 
import matplotlib.pyplot as plt 
import sys
import numpy as np
from statsmodels.nonparametric.smoothers_lowess import lowess
import pykalman as pk

# File Setup
filename1 = sys.argv[1]
cpu_data = pd.read_csv(filename1, parse_dates=['timestamp'])

# LOESS Smoothing
loess_smoothed = lowess(cpu_data['temperature'], cpu_data['timestamp'], frac=0.05)
plt.figure(figsize=(12, 4))
plt.plot(cpu_data['timestamp'], cpu_data['temperature'], 'b.', alpha=0.5)
plt.plot(cpu_data['timestamp'], loess_smoothed[:, 1], 'r-')
#plt.show()
#plt.savefig('cpu.svg')

# Kalman Smoothing
kalman_data = cpu_data[['temperature', 'cpu_percent', 'sys_load_1', 'fan_rpm']]
kf = pk.KalmanFilter(
    initial_state_mean= kalman_data.iloc[0],
    observation_covariance= np.diag([1.5, 1.5, 2.5, 2.5]) ** 2,
    transition_covariance= np.diag([0.2, 0.2, 0.2, 0.2]) ** 2,
    transition_matrices= [[0.97, 0.5, 0.2, -0.001], [0.1, 0.4, 2.2, 0], [0, 0, 0.95 ,0], [0, 0, 0, 1]]
)
kalman_smoothed, _ = kf.smooth(kalman_data)
plt.plot(cpu_data['timestamp'], kalman_smoothed[:, 0], 'g-')
#plt.show()
plt.savefig('cpu.svg')
