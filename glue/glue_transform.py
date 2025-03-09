import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()


def main():
    ## @params: [JOB_NAME]
    args = getResolvedOptions(sys.argv, ["VAL1"])
    file_names=args['VAL1'].split(',')
    df = spark.read.csv(file_names, header = True)
    df.repartition(1).write.mode('append').parquet("s3a://endor-data-uploads/publish/")

main()
