#!/usr/bin/python

import MySQLdb

class DB(object):
	db     = ""
	cursor = ""

	def setup(self, Config):
		DBHost = Config["DBHost"]
		DBUser = Config["DBUser"]
		DBPass = Config["DBPass"]
		DBName = Config["DBBase"]

		try:
			self.db = MySQLdb.connect(DBHost,DBUser,DBPass,DBName )
			self.cursor = self.db.cursor()

		except MySQLdb.Error as e:
			if e[0] == 2002:
				print "** Error on connecting to Mysql \n** Is MysqlServer running on target host?"
			else:
				print "** Error: unable to connect to db \n\t {dberror}".format(dberror=e)
			exit()

	def getAll(self):
		sql = "SELECT * FROM fgt_devices WHERE STATUS = 0"

		try:
			self.cursor.execute(sql)
			results = self.cursor.fetchall()
			return results
		except MySQLdb.Error as e:
			print "Error: unable to fecth data: %s" % (e)
			self.db.close()
