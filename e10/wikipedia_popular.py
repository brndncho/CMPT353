# boilerplate
import sys
from pyspark.sql import SparkSession, functions, types
import os

spark = SparkSession.builder.appName('wikipedia popular').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+


# schema
wikipedia_schema = types.StructType([
    types.StructField('language', types.StringType()),
    types.StructField('page', types.StringType()),
    types.StructField('times_requested', types.LongType()),
    types.StructField('bytes', types.StringType()),
])


# get the YYYYMMDD-HH
def parse_filename(path):
    filename = os.path.basename(path)
    filename_parts = filename.split('-')
    return filename_parts[1] + "-" + filename_parts[2][0:2]


def main(in_directory, out_directory):
    data = spark.read.csv(in_directory, schema=wikipedia_schema, sep=" ").withColumn('filename', functions.input_file_name())

    # apply udf
    path_to_hour = functions.udf(parse_filename, returnType=types.StringType())
    data = data.withColumn('hours', path_to_hour(data['filename']))
    data = data.drop(data['filename'])

    # filter to only en
    data = data.where(data['language'] == 'en')

    # filter out Main_Page
    data = data.filter(data['page'] != 'Main_Page')

    # filter out starting with Special:
    data = data.filter(data['page'].startswith('Special:') == False)

    # group by hours
    data_grouped_hours = data.groupby('hours').agg(functions.max(data['times_requested']).alias('times_requested'))
    
    # join tables
    joined_data = data.join(data_grouped_hours, ['times_requested', 'hours']).cache()
    joined_data = joined_data.sort('hours')
    joined_data = joined_data.select('hours', 'page', 'times_requested')
    
    # output to csv
    joined_data.write.csv(out_directory, mode='overwrite')

if __name__ == '__main__':
    in_directory = sys.argv[1]
    out_directory = sys.argv[2]
    main(in_directory, out_directory)