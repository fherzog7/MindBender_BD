from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql import SparkSession
from re import sub



sc = SparkContext("local[*]", "Shakespeare")
ssc = StreamingContext(sc, 3)

ss = SparkSession.builder \
	.enableHiveSupport() \
	.getOrCreate()


words = sc.textFile("/home/eit/Shakespeare.txt").flatMap(lambda line: line.split(" "))
	
	
wordCounts = words.map(lambda word: word.lower()) \
	.map(lambda word: sub('[^A-Za-z0-9]+', '', word)) \
	.map(lambda word: (word, 1)) \
	.reduceByKey(lambda a,b:a +b)
	


wordCounts.saveAsTextFile("/home/eit/sparkout")











ssc.start()

ssc.awaitTermination()
