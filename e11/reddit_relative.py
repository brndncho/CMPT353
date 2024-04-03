import sys
from pyspark.sql import SparkSession, functions, types

spark = SparkSession.builder.appName('reddit relative scores').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

comments_schema = types.StructType([
    types.StructField('archived', types.BooleanType()),
    types.StructField('author', types.StringType()),
    types.StructField('author_flair_css_class', types.StringType()),
    types.StructField('author_flair_text', types.StringType()),
    types.StructField('body', types.StringType()),
    types.StructField('controversiality', types.LongType()),
    types.StructField('created_utc', types.StringType()),
    types.StructField('distinguished', types.StringType()),
    types.StructField('downs', types.LongType()),
    types.StructField('edited', types.StringType()),
    types.StructField('gilded', types.LongType()),
    types.StructField('id', types.StringType()),
    types.StructField('link_id', types.StringType()),
    types.StructField('name', types.StringType()),
    types.StructField('parent_id', types.StringType()),
    types.StructField('retrieved_on', types.LongType()),
    types.StructField('score', types.LongType()),
    types.StructField('score_hidden', types.BooleanType()),
    types.StructField('subreddit', types.StringType()),
    types.StructField('subreddit_id', types.StringType()),
    types.StructField('ups', types.LongType()),
    #types.StructField('year', types.IntegerType()),
    #types.StructField('month', types.IntegerType()),
])


def main(in_directory, out_directory):
    comments = spark.read.json(in_directory, schema=comments_schema).cache()
    
    # Calculate the average score for each subreddit, as before.
    groups = comments.groupBy('subreddit') # group by subreddit
    result = groups.agg(functions.avg(comments['score'])).cache() # average scores by subreddit

    # Exclude any subreddits with average score ≤0.
    result = result.filter(result['avg(score)'] > 0)

    # Join the average score to the collection of all comments. Divide to get the relative score.
    comments = comments.join(result, ['subreddit'])
    comments = comments.withColumn('rel_score', (comments['score'] / comments['avg(score)'])).cache()

    # Determine the max relative score for each subreddit.
    comments_grouped_subreddit = comments.groupby('subreddit').agg(functions.max(comments['rel_score']).alias('rel_score')).cache()

    # Join again to get the best comment on each subreddit: we need this step to get the author.
    best_author = comments.join(comments_grouped_subreddit, ['subreddit', 'rel_score']).cache()
    best_author = best_author.select('subreddit', 'author', 'rel_score')

    # Output should be uncompressed JSON (as in the hint) with the fields subreddit, author, (from the original data) and rel_score (calculated as above).
    best_author.write.json(out_directory, mode='overwrite')
    # use command (cat output/part-* | less) to see output 

if __name__=='__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)
