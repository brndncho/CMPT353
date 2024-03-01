import pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

data = pd.read_csv('data.csv')

# You will need a statistical test that can be used to determine if the means of multiple samples are different
# Use ANOVA for 2+ groups

anova = stats.f_oneway(data['qs1'], data['qs2'], data['qs3'], data['qs4'], data['qs5'], data['merge1'], data['partition_sort'])
print(anova.pvalue)

# significance from ANOVA, can do post hoc analysis
x_data = pd.DataFrame({'qs1':data['qs1'],
                        'qs2':data['qs2'],
                        'qs3':data['qs3'],
                        'qs4':data['qs4'],
                        'qs5':data['qs5'],
                        'merge1':data['merge1'],
                        'partition_sort':data['partition_sort']})
x_melt = pd.melt(x_data)
posthoc = pairwise_tukeyhsd(
    x_melt['value'], x_melt['variable'],
    alpha = 0.05)
print(posthoc)

fig = posthoc.plot_simultaneous()
fig.savefig('tukey_hsd.png')