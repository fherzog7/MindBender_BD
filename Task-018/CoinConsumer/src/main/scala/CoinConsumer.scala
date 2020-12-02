import org.apache.spark.sql._
import org.apache.spark.sql.SparkSession
//import org.apache.spark.sql.functions._


object CoinConsumer
{
    def main(args: Array[String])
    {
      val ss = SparkSession
      	.builder
      	.appName("CoinConsumer")
      	.master("local[*]")
      	.getOrCreate()

      import ss.implicits._

      val inputDF = ss
      	.readStream
      	.format("kafka")
      	.option("kafka.bootstrap.servers", "localhost:9099")
      	.option("subscribe", "coin")
      	.load()

      val rawDF = inputDF.selectExpr("CAST(value AS STRING)").as[String]

      val query = rawDF
      	.writeStream
      	.outputMode("update")
      	.format("console")
      	.start()
      
      query.awaitTermination()

    }
}