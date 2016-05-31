#!/usr/bin/python

import MySQLdb

class DB(object):
	db     = ""
	cursor = ""

	def __init__(self):
		try:
			self.db = MySQLdb.connect(DBHost,DBUser,DBPass,DBName )
			self.cursor = self.db.cursor()

		except MySQLdb.Error as e:
			print "Error: unable to connect to db: %s" % (e)
			self.db.close()

	def getAll(self):
		sql = "SELECT * FROM fgt_devices WHERE STATUS = 0"

		try:
			self.cursor.execute(sql)  
			results = self.cursor.fetchall()
			return results
		except MySQLdb.Error as e:
			print "Error: unable to fecth data: %s" % (e)
			self.db.close()
