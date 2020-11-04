#Frederick Herzog
# Python Word Count
# 11/3/2020

from re import sub
from collections import Counter
from pydoop import hdfs

def txt_WordsToList(file):
	with open(file, 'r') as f:
		data = f.read().split()
		return data
	
def removePunct(dat):
	cleandat = []
	for word in dat:
		cleaned_word = sub('[^A-Za-z0-9]+', '', word)
		cleandat.append(cleaned_word)
	return cleandat

def makeLowerCase(dat):
	lower_case = [w.lower() for w in dat]
	return lower_case

def countWords(dat):
	count = Counter
	c = count(dat)
	return dict_to_tuples(c)

def dict_to_tuples(dat):
	freq = []
	for k, v in dat.items():
		freq.append((v,k))
	freq.sort(reverse = True)
	return freq

def out_to_txt(dat, file):
	with open(file, 'w') as f:
		for i in dat:
			f.write('    '.join (str(s) for s in i) + '\n')

def out_to_dfs(file, dfs_path):
	print("Writing file to HDFS...")
	hdfs.put(file, dfs_path)

if __name__ == '__main__':
	file_path = "Shakespeare.txt"
	out_path = "count_python.txt"
	dfs_path = "hdfs://localhost:9000/SPtext/"+out_path
	words = txt_WordsToList(file_path)
	words_no_punct = removePunct(words)
	lower_c_words = makeLowerCase(words_no_punct)
	my_count = countWords(lower_c_words)
	print(my_count)
	out_to_txt(my_count, out_path)
	out_to_dfs(out_path, dfs_path)



