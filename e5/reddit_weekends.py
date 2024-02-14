import sys
import pandas as pd
pd.options.mode.chained_assignment = None
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np


OUTPUT_TEMPLATE = (
    "Initial T-test p-value: {initial_ttest_p:.3g}\n"
    "Original data normality p-values: {initial_weekday_normality_p:.3g} {initial_weekend_normality_p:.3g}\n"
    "Original data equal-variance p-value: {initial_levene_p:.3g}\n"
    "Transformed data normality p-values: {transformed_weekday_normality_p:.3g} {transformed_weekend_normality_p:.3g}\n"
    "Transformed data equal-variance p-value: {transformed_levene_p:.3g}\n"
    "Weekly data normality p-values: {weekly_weekday_normality_p:.3g} {weekly_weekend_normality_p:.3g}\n"
    "Weekly data equal-variance p-value: {weekly_levene_p:.3g}\n"
    "Weekly T-test p-value: {weekly_ttest_p:.3g}\n"
    "Mann-Whitney U-test p-value: {utest_p:.3g}"
)

# to get the year from datetime type
def to_year(dt):
    return dt.year

# get weekday number
def to_weekday(dt):
    return dt.weekday()

# get year and week
def to_isocalendar(dt):
    return dt.isocalendar()[:2]

def main():

    counts = pd.read_json(sys.argv[1], lines=True)
    # start 15470 rows

    counts['year'] = counts['date'].apply(to_year) # add year column
    counts = counts.drop(counts[(counts['year'] != 2012) & (counts['year'] != 2013)].index) # drop rows that are not 2012 or 2013
    counts = counts.drop(counts[counts['subreddit'] != 'canada'].index) # drop rows that are not in canada subreddit
    # filtered to 731 rows

    counts['weekday'] = counts['date'].apply(to_weekday) # add weekday column

    # seperate weekdays and weekends
    counts_weekdays = counts[(counts['weekday'] != 5) & (counts['weekday'] != 6)]
    counts_weekends = counts[(counts['weekday'] == 5) | (counts['weekday'] == 6)]
    #print(counts_weekdays)
    #print(counts_weekends)

    ttest = stats.ttest_ind(counts_weekdays['comment_count'], counts_weekends['comment_count'])
    #print(ttest.pvalue) result is 1.3005502847207912e-58

    normaltest_weekdays = stats.normaltest(counts_weekdays['comment_count'])
    normaltest_weekends = stats.normaltest(counts_weekends['comment_count'])
    #print(normaltest_weekdays.pvalue) result is 1.0091137251707994e-07
    #print(normaltest_weekends.pvalue) result is 0.0015209196859635404
    # p is < 0.05, so we cannot assume the distribution is normal

    levenetest = stats.levene(counts_weekdays['comment_count'], counts_weekends['comment_count'])
    #print(levenetest.pvalue) result is 0.04378740989202803
    # p is < 0.05, so we cannot assume the two data sets have equal variances

    #plt.hist(counts_weekdays['comment_count'])
    #plt.show() weekdays looks more normal
    #plt.hist(counts_weekends['comment_count'])
    #plt.show() weekends looks more skewed 

    # log gave better results for weekends, sqrt gave better results for weekdays, sticking with log
    counts_weekdays_log = np.log(counts_weekdays['comment_count'])
    counts_weekends_log = np.log(counts_weekends['comment_count'])
    normaltest_weekdays_log = stats.normaltest(counts_weekdays_log)
    normaltest_weekends_log = stats.normaltest(counts_weekends_log)
    #print(normaltest_weekdays_log.pvalue) result is 0.00040159142006827235
    #print(normaltest_weekends_log.pvalue) result is 0.31493886820667
    levenetest_log = stats.levene(counts_weekdays_log, counts_weekends_log)
    #print(levenetest_log.pvalue) result is 0.0004190759393372205

    counts_weekdays['year_week'] = counts_weekdays['date'].apply(to_isocalendar)
    counts_weekends['year_week'] = counts_weekends['date'].apply(to_isocalendar)
    # combine the comment counts if they have the same year and week and get the average
    counts_weekdays_average = counts_weekdays.groupby(['year_week'], dropna=True)['comment_count'].mean()
    counts_weekends_average = counts_weekends.groupby(['year_week'], dropna=True)['comment_count'].mean()
    ttest_fix2 = stats.ttest_ind(counts_weekdays_average, counts_weekends_average)
    #print(ttest_fix2.pvalue) result is 1.3353656052303144e-34
    normaltest_weekdays_fix2 = stats.normaltest(counts_weekdays_average)
    #print(normaltest_weekdays_fix2.pvalue) result is 0.3082637390825463
    normaltest_weekends_fix2 = stats.normaltest(counts_weekends_average)
    #print(normaltest_weekends_fix2.pvalue) result is 0.15294924717078442
    # p is > 0.05, so we can assume the distribution is normal
    levenetest_fix2 = stats.levene(counts_weekdays_average, counts_weekends_average)
    #print(levenetest_fix2.pvalue) result is 0.20383788083573426
    # p is > 0.05, so we can assume the two data sets have equal variances

    MWU_test = stats.mannwhitneyu(counts_weekdays['comment_count'], counts_weekends['comment_count'])
    #print(MWU_test.pvalue) result is 8.6244532347343e-53
    # p < 0.05, its not equally-likely that the large number of comments occur on weekends vs weekdays

    print(OUTPUT_TEMPLATE.format(
        initial_ttest_p= ttest.pvalue,
        initial_weekday_normality_p= normaltest_weekdays.pvalue,
        initial_weekend_normality_p= normaltest_weekends.pvalue,
        initial_levene_p= levenetest.pvalue,
        transformed_weekday_normality_p= normaltest_weekdays_log.pvalue,
        transformed_weekend_normality_p= normaltest_weekends_log.pvalue,
        transformed_levene_p= levenetest_log.pvalue,
        weekly_weekday_normality_p= normaltest_weekdays_fix2.pvalue,
        weekly_weekend_normality_p= normaltest_weekends_fix2.pvalue,
        weekly_levene_p= levenetest_fix2.pvalue,
        weekly_ttest_p= ttest_fix2.pvalue,
        utest_p= MWU_test.pvalue,
    ))


if __name__ == '__main__':
    main()
