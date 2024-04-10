import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import split, explode, lower
import string, re

spark = SparkSession.builder.appName('word count').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

# run with spark-submit wordcount.py wordcount-1 output


def main(in_directory, out_directory):
    # read text file lines
    textlines_df = spark.read.text(in_directory)
    
    # split the lines into words
    wordbreak = r'[%s\s]+' % (re.escape(string.punctuation),)  # regex that matches spaces and/or punctuation
    words_df = textlines_df.select(explode(split(textlines_df['value'], wordbreak)).alias('words'))

    # normalize strings to lowercase
    words_df = words_df.withColumn('words', lower(words_df['words']))
    
    # remove empty strings
    words_df = words_df.filter(words_df['words'] != '')
    
    # count number of times each word occurs
    words_count_df = words_df.groupBy('words').count()

    # sort by decreasing count, then alphabetically if tie
    words_count_sorted_df = words_count_df.orderBy(['count', 'words'], ascending=[0, 1])
    
    # save to csv
    words_count_sorted_df.write.csv(out_directory, mode='overwrite')

    return 0


if __name__ == '__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)