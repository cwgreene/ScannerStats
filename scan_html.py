import sys
import os
import re
import locale
import codecs

from collections import defaultdict

import pages
import database

def extract_text(file):
	return file #not yet

def character_count(doclines):
	counts = defaultdict(lambda: 0)
	for line in doclines:
		for char in line:
			if ord(char) > 255:
				counts[char]+=1
	return counts

def print_char_counts(counts):
	#hack:ord
	x = [(k,counts[k]) for k in counts]
	x.sort(key= lambda k : (-k[1],k[0]))
	for key in x:
		print key[0],key[1]

def find_charset(filename):
	file = open(filename)
	charset = None
	line=" "
	while not charset and line:
		line = file.readline()
		if line.find("charset") >= 0:
			#hack
			charset = re.findall("charset=([^ \"]*)[\" ]",line)[0]
	if charset:
		return charset
	file.close()
	return "utf-8"

def process_file(filename):
	charset = find_charset(filename)
	lines = ""
	file = open(filename)
	for line in file:
		lines += unicode(line,charset)
	file.close()
	return lines

def main(args):
	conn = database.open_database("db/test.lite")
	for filename in args[1:]:
		filelines = process_file(filename)
		counts=character_count(filelines)
		print_char_counts(counts)
	
		page = pages.Page(filename)
		database.inter_histogram(conn,page,counts)

if __name__=="__main__":
	sys.stdout=codecs.getwriter("utf-8")(sys.stdout)
	main(sys.argv)
