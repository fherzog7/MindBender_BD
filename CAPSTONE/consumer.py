from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StringType, IntegerType 
#from pyspark.sql.types import IntegerType
from pyspark.sql.types import FloatType
from pyspark.sql.types import TimestampType
from pyspark.sql.types import StructType
from pyspark.sql.types import StructField
from argparse import ArgumentParser
from geopy.geocoders import Nominatim
from datetime import datetime
from json import loads

brokers = "localhost:9092, localhost:9093, localhost:9094"
single_broker = "localhost:9099"
topic = "capTest"
topic2 = "Aircraft"
Z_K = "localhost:2181"
AppName = "Aircraft"


Schema = StructType([StructField('icao', StringType(), True),
                    StructField('reg', StringType(), True),
                    StructField('alt', StringType(), True),
					StructField('galt', StringType(), True),
                    StructField('spd', StringType(), True),
                    StructField('dst', StringType(), True),
					StructField('lat', StringType(), True),
                    StructField('lon', StringType(), True),
                    StructField('postime', StringType(), True)])

def Process(rdd):
	if not rdd.isEmpty():
		global ss 
		df = ss.createDataFrame(rdd, Schema) \
			.na.drop()   \
			.show()


		#df.write.saveAsTable(name="rentals",
			#format="hive", mode="append")


sc = SparkContext("local[*]", AppName)
ssc = StreamingContext(sc, 7)

ss = SparkSession.builder.appName(sc.appName).getOrCreate()
	#.config("spark.sql.warehouse.dir",
		#"/user/hive/warehouse") \
	#.config("hive.metastore.uris",
		#"thrift://localhost:9083") \
	#.enableHiveSupport() \
	

kafkastream = KafkaUtils.createStream(ssc, Z_K, AppName, {topic: 1})

raw_json = kafkastream.map(lambda x: loads(x[1]))

aircraft = raw_json.flatMap(lambda x: x.get("ac")) \
	.map(lambda x: (x.get("icao"), x.get("reg"), 
			x.get("alt"), x.get("galt"), x.get("spd"), 
			x.get("dst"), x.get("lat"), x.get("lon"), x.get("postime")))

aircraft.foreachRDD(Process)


ssc.start()
ssc.awaitTermination()

### spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.4 consumer.py
