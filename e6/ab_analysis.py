import sys
import pandas as pd
from scipy import stats


OUTPUT_TEMPLATE = (
    '"Did more/less users use the search feature?" p-value:  {more_users_p:.3g}\n'
    '"Did users search more/less?" p-value:  {more_searches_p:.3g} \n'
    '"Did more/less instructors use the search feature?" p-value:  {more_instr_p:.3g}\n'
    '"Did instructors search more/less?" p-value:  {more_instr_searches_p:.3g}'
)


def main():
    # C:/Users/brand/anaconda3/python.exe ab_analysis.py searches.json

    searches = pd.read_json(sys.argv[1], orient='records', lines=True)

    # seperate between old and even with modulo
    old_searches = searches.drop(searches[searches['uid'] %2 == 1].index)
    new_searches = searches.drop(searches[searches['uid'] %2 == 0].index)

    # categories will be even/odd uid (aka control/treatment), and “searched at least once”/“never searched”.
    old_searches_least_once = old_searches['search_count'].drop(old_searches[old_searches['search_count'] == 0].index).count()
    old_searches_never = old_searches['search_count'].drop(old_searches[old_searches['search_count'] > 0].index).count()
    #print(old_searches_least_once)
    #print(old_searches_never)
    new_searches_least_once = new_searches['search_count'].drop(new_searches[new_searches['search_count'] == 0].index).count()
    new_searches_never = new_searches['search_count'].drop(new_searches[new_searches['search_count'] > 0].index).count()
    #print(new_searches_least_once)
    #print(new_searches_never)

    # Did more users use the search feature? (More precisely: did a different fraction of users have search count > 0?)
    contingency_table = [[old_searches_least_once, old_searches_never], 
                        [new_searches_least_once, new_searches_never]] 
    chi2, p, dof, expected = stats.chi2_contingency(contingency_table)

    # Did users search more often? (More precisely: is the number of searches per user different?)
    search_more_often = stats.mannwhitneyu(old_searches['search_count'], new_searches['search_count']).pvalue

    # Repeat the above analysis looking only at instructors.
    old_searches_instructors = old_searches.drop(old_searches[old_searches['is_instructor'] == False].index)
    new_searches_instructors = new_searches.drop(new_searches[new_searches['is_instructor'] == False].index)

    old_searches_least_once_instructors = old_searches_instructors['search_count'].drop(old_searches_instructors[old_searches_instructors['search_count'] == 0].index).count()
    old_searches_never_instructors = old_searches_instructors['search_count'].drop(old_searches_instructors[old_searches_instructors['search_count'] > 0].index).count()
    new_searches_least_once_instructors = new_searches_instructors['search_count'].drop(new_searches_instructors[new_searches_instructors['search_count'] == 0].index).count()
    new_searches_never_instructors = new_searches_instructors['search_count'].drop(new_searches_instructors[new_searches_instructors['search_count'] > 0].index).count()

    contingency_table_instrutors = [[old_searches_least_once_instructors, old_searches_never_instructors], 
                                    [new_searches_least_once_instructors, new_searches_never_instructors]]
    chi2_instructors, p_instructors, dof_instructors, expected_instructors = stats.chi2_contingency(contingency_table_instrutors)

    search_more_often_instructors = stats.mannwhitneyu(old_searches_instructors['search_count'], new_searches_instructors['search_count']).pvalue

    print(OUTPUT_TEMPLATE.format(
        more_users_p= p,
        more_searches_p= search_more_often,
        more_instr_p= p_instructors,
        more_instr_searches_p= search_more_often_instructors,
    ))


if __name__ == '__main__':
    main()
