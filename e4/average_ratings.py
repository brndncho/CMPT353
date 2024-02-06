import sys
import pandas as pd
import difflib as dl
#python3 average_ratings.py movie_list.txt movie_ratings.csv output.csv

filename1 = sys.argv[1]
filename2 = sys.argv[2]
filename3 = sys.argv[3]

movie_list = open(filename1).read().splitlines()
movie_title_df = pd.DataFrame(data=movie_list, columns=['title'])
movie_title_rating_df = pd.read_csv(filename2)

# source: https://stackoverflow.com/questions/72610732/convert-multiple-python-lines-to-a-concurrent-dataframe-and-merge-with-source-da
def find_close_matches(word):
    match = dl.get_close_matches(word, movie_title_df['title'])
    return match[0] if match else pd.NaT

movie_title_rating_df['title'] = movie_title_rating_df['title'].apply(find_close_matches)
a = movie_title_rating_df.groupby(['title'], dropna=True).mean()

print(a)
print(movie_title_rating_df.dtypes)