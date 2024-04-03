import sys
from pyspark.sql import SparkSession, functions, types, Row
import re
from math import sqrt

spark = SparkSession.builder.appName('correlate logs').getOrCreate()
spark.sparkContext.setLogLevel('WARN')

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
assert spark.version >= '2.3' # make sure we have Spark 2.3+

line_re = re.compile(r"^(\S+) - - \[\S+ [+-]\d+\] \"[A-Z]+ \S+ HTTP/\d\.\d\" \d+ (\d+)$")


def line_to_row(line):
    """
    Take a logfile line and return a Row object with hostname and bytes transferred. Return None if regex doesn't match.
    """
    m = line_re.match(line)
    if m:
        # TODO
        return Row(host_name=m.group(1), bytes_transferred=m.group(2))
    else:
        return None


def not_none(row):
    """
    Is this None? Hint: .filter() with it.
    """
    return row is not None


def create_row_rdd(in_directory):
    log_lines = spark.sparkContext.textFile(in_directory)
    
    # TODO: return an RDD of Row() objects
    log_rows = log_lines.map(line_to_row)
    log_rows = log_rows.filter(not_none)
    return log_rows


def main(in_directory):
    logs = spark.createDataFrame(create_row_rdd(in_directory)).cache()

    # Group by hostname; get the number of requests and sum of bytes transferred, to form a data point
    logs_groupby_host = logs.groupBy('host_name').agg(functions.sum(logs['bytes_transferred']).alias('y'), functions.count(logs['host_name']).alias('x')).cache()

    # To produce “the six sums”, you can call .groupBy() with no arguments to aggregate the entire DataFrame to one row.
    agg_logs = logs_groupby_host.groupBy()

    # Produce six values, add them to get the six sums
    # use first() to get the tuple, then [0] to get the first value
    n = logs_groupby_host.count()
    x_i = agg_logs.agg(functions.sum(logs_groupby_host['x'])).first()[0]
    y_i = agg_logs.agg(functions.sum(logs_groupby_host['y'])).first()[0]
    x_i_sq = agg_logs.agg(functions.sum(logs_groupby_host['x']**2)).first()[0]
    y_i_sq = agg_logs.agg(functions.sum(logs_groupby_host['y']**2)).first()[0]
    x_i_y_i = agg_logs.agg(functions.sum(logs_groupby_host['x'] * logs_groupby_host['y'])).first()[0] 

    # TODO: calculate r.
    r = ((n * x_i_y_i) - (x_i * y_i)) / ((sqrt((n * x_i_sq) - (x_i**2))) * (sqrt((n * y_i_sq) - (y_i**2))))
    print("r = %g\nr^2 = %g" % (r, r**2))


if __name__=='__main__':
    in_directory = sys.argv[1]
    main(in_directory)