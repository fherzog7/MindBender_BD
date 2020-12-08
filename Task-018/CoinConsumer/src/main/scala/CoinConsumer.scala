import org.apache.spark.sql._
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.types._
import org.apache.spark.sql.functions._
import org.apache.spark.sql.streaming.Trigger  

import org.apache.spark.sql.datasources.hbase.HBaseTableCatalog

object CoinConsumer
{

    def main(args: Array[String])
    {

      val rawSchema =
   		StructType(List(
     	StructField("status", StringType, true),
     	StructField("data", StringType, true) ) )

   	  val dataSchema =
   		StructType(List(
     	StructField("base", StringType, true),
     	StructField("coin", StringType, true) ) )

   	  val coinSchema =
   		StructType(List(
     	StructField("id", StringType, true),
     	StructField("symbol", StringType, true),
      StructField("name", StringType, true),
     	StructField("price", IntegerType, true),
      StructField("volume", IntegerType, true),
      StructField("totalSupply", StringType, true),
      StructField("rank", StringType, true)) )

      def catalog =
        s"""{
           |"table":{"namespace":"default", "name":"coins"},
           |"rowkey":"id",
           |"columns":{
           |"id":{"cf":"rowkey", "col":"id", "type":"string"},
           |"symbol":{"cf":"general", "col":"symbol", "type":"string"},
           |"name":{"cf":"general", "col":"name", "type":"string"},
           |"price":{"cf":"tech", "col":"middleName", "type":"double"},
           |"volume":{"cf":"tech", "col":"addressLine", "type":"integer"},
           |"totalSupply":{"cf":"tech", "col":"totalSupply", "type":"integer"},
           |"rank":{"cf":"general", "col":"rank", "type":"string"},
           |"timestamp":{"cf":"general", "col":"timestamp", "type":"string"}
           |}
           |}""".stripMargin

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
	  	.select(from_json($"json", rawSchema) as "stuff")
	  	.select("stuff.*")
	  	.drop("status")  

	  val coin = rawDataframe.select(from_json($"data", dataSchema) as "stuff")
	  	.select("stuff.*")
	  	.drop("base")
	  	.select(from_json($"coin", coinSchema) as "coin")
	  	.select("coin.*")
      .withColumn("timestamp", lit(System.currentTimeMillis))

      coin.printSchema()

      //coin.write
      //  .options(Map(HBaseTableCatalog.tableCatalog -> catalog, 
      //      HBaseTableCatalog.newTable -> 4))
      //  .format("org.apache.spark.sql.execution.datasources.hbase")
      //  .save()

      val query = coin
      	.writeStream
      	.outputMode("Append")
      	.format("console")
        .trigger(Trigger.ProcessingTime("35 seconds"))
      	.start()
    
      query.awaitTermination()

    }
}


//spark-submit --class CoinConsumer --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.1 target/scala-2.11/coinconsumer_2.11-1.0.jar