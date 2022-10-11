#!/usr/bin/env python
"""Extract events from kafka and write them to hdfs
"""
import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, from_json
from pyspark.sql.types import StructType, StructField, StringType


def event_schema():
    """
    root
    |-- Accept: string (nullable = true)
    |-- Host: string (nullable = true)
    |-- User-Agent: string (nullable = true)
    |-- event_type: string (nullable = true)
    |-- timestamp: string (nullable = true)
    """
    return StructType([
        StructField("Accept", StringType(), True),
        StructField("Host", StringType(), True),
        StructField("User-Agent", StringType(), True),
        StructField("event_type", StringType(), True),
    ])


@udf('boolean')
def is_purchase(event_as_json):
    event = json.loads(event_as_json)
    if event['event_type'] == 'purchase_sword':
        return True
    elif event['event_type'] == 'purchase_armor':
        return True
    elif event['event_type'] == 'purchase_shield':
        return True
    return False


@udf('boolean')
def is_guild_join(event_as_json):
    event = json.loads(event_as_json)
    if event['event_type'] == 'join_guild':
        return True
    return False


def main():
    """main
    """
    spark = SparkSession \
        .builder \
        .appName("ExtractEventsJob") \
        .enableHiveSupport()\
        .getOrCreate()

    raw_events = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("subscribe", "events") \
        .load()

    all_purchases = raw_events \
        .filter(is_purchase(raw_events.value.cast('string'))) \
        .select(raw_events.value.cast('string').alias('raw_event'),
                raw_events.timestamp.cast('string'),
                from_json(raw_events.value.cast('string'),
                          event_schema()).alias('json')) \
        .select('raw_event', 'timestamp', 'json.*')

    guilds_join = raw_events \
        .filter(is_guild_join(raw_events.value.cast('string'))) \
        .select(raw_events.value.cast('string').alias('raw_event'),
                raw_events.timestamp.cast('string'),
                from_json(raw_events.value.cast('string'),
                          event_schema()).alias('json')) \
        .select('raw_event', 'timestamp', 'json.*')
    
    spark.sql("drop table if exists all_purchases")
    purchase_sql_string = """
        create external table if not exists all_purchases (
            raw_event string,
            timestamp string,
            Accept string,
            Host string,
            `User-Agent` string,
            event_type string
            )
            stored as parquet
            location '/tmp/all_purchases'
            tblproperties ("parquet.compress"="SNAPPY")
            """
    spark.sql(purchase_sql_string)
    
    spark.sql("drop table if exists guilds_join")
    guild_sql_string = """
        create external table if not exists guilds_join (
            raw_event string,
            timestamp string,
            Accept string,
            Host string,
            `User-Agent` string,
            event_type string
            )
            stored as parquet
            location '/tmp/guilds_join'
            tblproperties ("parquet.compress"="SNAPPY")
            """
    spark.sql(guild_sql_string)
    
    purchase_sink = all_purchases \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_purchases") \
        .option("path", "/tmp/all_purchases") \
        .trigger(processingTime="10 seconds") \
        .start()

    guild_sink = guilds_join \
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_guilds") \
        .option("path", "/tmp/guilds_join") \
        .trigger(processingTime="10 seconds") \
        .start()
        
    purchase_sink.awaitTermination()
    guild_sink.awaitTermination()


if __name__ == "__main__":
    main()