//Frederick Herzog
// Scala Word Count 
// 10/31/2020

import scala.io.Source
import scala.util.matching.Regex
import scala.collection.immutable.ListMap

object wrdcount {
	var file_path = "Shakespeare.txt"

   def main(args: Array[String]) {
       var dat = readData(file_path)
       var my_count = countWords(dat)
       val sorted_map = sort_Map(my_count)
       printMap(sorted_map)

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
}
