//Frederick Herzog
// Scala Word Count 
// 11/3/2020

import scala.io.Source
import java.io.File
import java.io.PrintWriter
import scala.util.matching.Regex
import scala.collection.immutable.ListMap
import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.{FileSystem, Path}

object wrdcount {
  libraryDependencies ++= Seq(
  "org.apache.hadoop" % "hadoop-client" % "2.7.3"
)
	var file_path = "Shakespeare.txt"
  var out_path = "count_scala.txt"
  var dfs_path = "hdfs://localhost:9000/SPtext/"+out_path

   def main(args: Array[String]) {
       var dat = readData(file_path)
       var my_count = countWords(dat)
       printf("%s", my_count)
       val sorted_map = sort_Map(my_count)
       printMap(sorted_map)
       write_to_File(sorted_map, out_path)
       write_to_dfs(out_path, dfs_path)
   }
	
	def readData(path: String): List[String] = {
		// Using Regex to filter out unwanted characters.
       val words = """([A-Za-z0-9])+""".r
        // Reading each word in the file into a List using flatMap.
       val wordList = io.Source.fromFile(path).getLines.flatMap(words.findAllIn).toList
       val lc_wordList = convert_to_lowerCase(wordList)
       return lc_wordList
        }
    
    def convert_to_lowerCase(dat: List[String]): List[String] = {
    	// Convert each word in List to lowercase.
    	val lowerCase = for (w <- dat) yield w.toLowerCase
    	return lowerCase
    }
    
    def countWords(dat: List[String]): Map[String, Int] = {
    	// Using a map to count the number of occurences for each word.
    	dat.toSet.map((word: String) => (word, dat.count(_ == word))).toMap
    	}

    def sort_Map(dat: Map[String, Int]): Map[String, Int] = {
    	// Sorting the map (descending order) using ListMap.
    	return ListMap(dat.toSeq.sortWith(_._2 < _._2):_*)
    }

    def printMap(dat: Map[String, Int]) = {
    	// Printing out the data from the map.
    	for ((k,v) <- dat) printf("%s : %s\n", k, v)
    }

    def write_to_File(dat: Map[String, Int], path: String) = {
      val writer = new PrintWriter(new File(path))
      dat.foreach {
        case (k, v) => writer.write(k + "  " + v + "\n")

    }
      writer.close()

  }

    def write_to_dfs(path: String, dfs_path: String, dat: Map[String, Int]) = {
      val path = new Path(path)
      val conf = new Configuration
      conf.set("fs.defaultFS", dfs_path)
      val fs = FileSystem.get(conf)
      val out = fs.create(path)
      out.write(dat)
      fs.close()
  }

}
