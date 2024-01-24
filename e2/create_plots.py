# import statements
# To make it run on my pc w/ anaconda navigator:
# C:/Users/brand/anaconda3/python.exe create_plots.py pagecounts-20190509-120000.txt pagecounts-20190509-130000.txt
import sys
import pandas as pd
import matplotlib.pyplot as plt

# setup file arguments
filename1 = sys.argv[1]
filename2 = sys.argv[2]

# file order: language, page name, number of views, bytes transferred

# plot 1
data_filename1 = pd.read_csv(filename1, sep=' ', header=None, index_col=1, names=['lang', 'page', 'views', 'bytes'])
data_filename1_sorted = data_filename1.sort_values(by=['views'], ascending=False)
plt.figure(figsize=(10, 5)) # change the size to something sensible
plt.subplot(1, 2, 1) # subplots in 1 row, 2 columns, select the first
plt.plot(data_filename1_sorted['views'].values, 'b-') # build plot 1
plt.title('Popularity Distribution')
plt.xlabel('Rank')
plt.ylabel('Views')

# plot 2
data_filename2 = pd.read_csv(filename2, sep=' ', header=None, index_col=1, names=['lang', 'page', 'views', 'bytes'])
data_filename2_sorted = data_filename2.sort_values(by=['views'], ascending=False)
data_filename1_sorted['viewsPlot2'] = data_filename2_sorted['views'] # x and y must be the same size, cannot be other way around
plt.subplot(1, 2, 2) # ... and then select the second
plt.scatter(data_filename1_sorted['viewsPlot2'].values, data_filename1_sorted['views'].values, s=10, c='b') # build plot 2
plt.xscale('log') # logarithmic scales
plt.yscale('log')
plt.title('Hourly Correlation')
plt.xlabel('Hour 1 views')
plt.ylabel('Hour 2 views')

# resulting image
#plt.show()
plt.savefig('wikipedia.png')
