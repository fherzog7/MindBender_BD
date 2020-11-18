import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf

object SparkWordCount {
  def main(args: Array[String]) {
    // create Spark context with Spark configuration
    val sc = new SparkContext(new SparkConf()
        .setAppName("Spark Count")
        .setMaster("local[*]"))
    
    val data = sc.textFile("/home/eit/Shakespeare.txt")
        .flatMap(line => line.split(" "))
        .map(word => (word, 1))

    val counts = data.reduceByKey(_+_)


    //val splitdata = data.flatMap(line => line.split(" "))
    //val mapdata = splitdata.map(word => (word,1))
    //val reducedata = mapdata.reduceByKey(_+_)

    counts.saveAsTextFile("/home/eit/sparkout")

    sc.stop()


  }
}


//spark-submit \
 //--class "wrdcnt.scala" \
 //   --master local[4] \
 // target/scala-2.10/word-count_2.13-1.0.jar