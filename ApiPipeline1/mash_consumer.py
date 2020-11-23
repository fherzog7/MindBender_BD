from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql import SparkSession
import json

def Process(rdd):
	if not rdd.isEmpty():
		global ss 
		df = ss.createDataFrame(rdd, schema=["id", "property_type",
			"airbnb_neighborhood", "zip", "night_price", "capacity_of_people", 
			"lat", "lon", "name"])
		df.show()

		df.write.saveAsTable(name="rentals",
			format="hive", mode="append")


sc = SparkContext("local[*]", "RentalData")
ssc = StreamingContext(sc, 7)

ss = SparkSession.builder \
	.appName(sc.appName) \
	.config("spark.sql.warehouse.dir",
		"/user/hive/warehouse") \
	.config("hive.metastore.uris",
		"thrift://localhost:9083") \
	.enableHiveSupport() \
	.getOrCreate()

kafkastream = KafkaUtils.createStream(ssc, "localhost:2181", 
	"rentals", {"rentals": 1})


parsed = kafkastream.map(lambda x: json.loads(x[1]))
content = parsed.map(lambda x: x.get("content"))
properties = content.flatMap(lambda x: x.get("properties"))

filtered = properties.map(lambda x: (x.get("id"), x.get("property_type"), 
	x.get("airbnb_neighborhood"), x.get("zip"), x.get("night_price"), 
	x.get("capacity_of_people"), x.get("lat"), x.get("lon"), x.get("name")))

filtered.foreachRDD(Process)


ssc.start()
ssc.awaitTermination()



### spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.4 mash_consumer.py