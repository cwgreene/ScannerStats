import sqlite3
import os

import md5

#this should probably be constructed based upon a class
def init_database(conn):
	conn.execute("create table pages "+
			"(md5hash text, address text)")
	conn.execute("create table histograms "+
			"(pagehash text, character text, count int)")


def create_database(filename):
	if os.path.exists(filename):
		raise "File Exists"
	conn = sqlite3.connect(filename)

	init_database(conn)

	return conn

def open_database(filename):
	conn = None
	if os.path.exists(filename):
		conn = sqlite3.connect(filename)
	else:
		conn = create_database(filename)
	return conn

def page_exists(conn,page):
	cur = conn.cursor()
	result = cur.execute("select md5hash from pages where md5hash=?",
			(page.hash,))
	row = result.fetchone()
	if row == None:
		return False
	return True

def inter_histogram(conn,page,histogram):
	if not page_exists(conn,page):
		cur = conn.cursor()
		cur.execute("insert into pages values (?,?)",
				(page.hash,page.filename))
	else:
		print "Already interred"
		return
	for key in histogram:
		cur = conn.cursor()
		cur.execute("insert into histograms "+
			    "values (?,?,?)",
			    (page.hash,key,histogram[key]))
	conn.commit() #consistent

