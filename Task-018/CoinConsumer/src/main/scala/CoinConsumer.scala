import org.apache.spark.sql._
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.types._
import org.apache.spark.sql.functions._

object CoinConsumer
{

    def main(args: Array[String])
    {

      val schema =
   		StructType(List(
     	StructField("status", StringType, true),
     	StructField("data", StringType, true) ) )

   	  val schema2 =
   		StructType(List(
     	StructField("base", StringType, true),
     	StructField("coin", StringType, true) ) )

   	  val schema3 =
   		StructType(List(
     	StructField("id", StringType, true),
     	StructField("symbol", StringType, true),
     	StructField("price", StringType, true) ) )

      val ss = SparkSession
      	.builder
      	.appName("CoinConsumer")
      	.master("local[*]")
      	.getOrCreate()

      import ss.implicits._

      val inputDf = ss
      	.readStream
      	.format("kafka")
      	.option("kafka.bootstrap.servers", "localhost:9099")
      	.option("subscribe", "coin")
      	.load()

	  val rawDataframe = inputDf.select($"value" cast "string" as "json")
	  	.select(from_json($"json", schema) as "stuff")
	  	.select("stuff.*")
	  	.drop("status")  

	  val coin = rawDataframe.select(from_json($"data", schema2) as "stuff")
	  	.select("stuff.*")
	  	.drop("base")
	  	.select(from_json($"coin", schema3) as "coin")
	  	.select("coin.*")

      val query = coin
      	.writeStream
      	.outputMode("Append")
      	.format("console")
      	.start()
      
      query.awaitTermination()

    }
}


//spark-submit --class CoinConsumer --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.1 target/scala-2.11/coinconsumer_2.11-1.0.jar