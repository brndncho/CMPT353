import pandas as pd 
#from scipy import stats

data = pd.read_csv('data-6.csv')
#print(data)

# mean
x_mean = data['x'].mean()
y_mean = data['y'].mean()
print('mean = ', x_mean, y_mean)

# standard deviation
x_std = data['x'].std()
y_std = data['y'].std()
print('standard deviation = ', x_std, y_std)

# min value
x_min = data['x'].min()
y_min = data['y'].min()
print('min values = ', x_min, y_min)

# max value
x_max = data['x'].max()
y_max = data['y'].max()
print('max values = ', x_max, y_max)

# correlation (r) value
x_y_corr = data['x'].corr(data['y'])
#x_y_corr_2 = stats.linregress(data['x'], data['y']).rvalue
print('correlation = ', x_y_corr)
#print('correlation2: =', x_y_corr_2)