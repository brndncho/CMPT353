import time
from implementations import all_implementations
import pandas as pd
import numpy as np

random_array = np.random.randint(7000, size=7000)

data = pd.DataFrame(columns = ['qs1', 'qs2', 'qs3', 'qs4', 'qs5', 'merge1', 'partition_sort'])

for i in range(41):

    running_times = []

    for sort in all_implementations:
        st = time.time()
        res = sort(random_array)
        en = time.time()
        running_times.append(en - st) # subtract before from after to get time
    
    data.loc[i] = running_times

data.to_csv('data.csv', index = False)
