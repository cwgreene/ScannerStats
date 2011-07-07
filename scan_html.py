import sys
import os
import re

from collections import defaultdict

def extract_text(file):
	return file #not yet

def character_count(doclines):
	counts = defaultdict(lambda: 0)
	for line in doclines:
		for char in line:
			counts[char]+=1
	return counts

def print_char_counts(counts):
	x = [(-counts[k],k) for k in counts if ord(k) > 255]
	x.sort()
	for key in x:
		print key[1],-key[0]

def find_charset(filename):
	file = open(filename)
	charset = None
	line=" "
	while not charset and line:
		line = file.readline()
		if line.find("charset") >= 0:
			charset = re.findall("charset=(.*)[\" ]",line)[0]
	if charset:
		return charset
	return "utf-8"

def process_file(filename):
	charset = find_charset(filename)
	lines = ""
	for line in open(filename):
		lines += unicode(line,charset)
	return lines

def main(args):
	for filename in args[1:]:
		filelines = process_file(filename)
		counts=character_count(filelines)
		print_char_counts(counts)

if __name__=="__main__":
	main(sys.argv)
