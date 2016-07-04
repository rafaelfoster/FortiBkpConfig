#!/usr/bin/python

import MySQLdb

class DB(object):
	db        = ""
	cursor    = ""
	FGT_Table = "fgt_devices"

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
		sql = "SELECT * FROM {tbName} WHERE STATUS = 0".format(tbName=self.FGT_Table)

		try:
			self.cursor.execute(sql)
			results = self.cursor.fetchall()
			return results
		except MySQLdb.Error as e:
			print "Error: unable to fecth data: %s" % (e)
			self.db.close()

	def updateDB(self, field, value, ID ):
		sql = "UPDATE {tbName} SET {tbField} = {tbValue} WHERE ID = {tbID}".format(
			tbName=self.FGT_Table,
			tbField=field,
			tbValue=value,
			tbID=ID
		)
		try:
			self.cursor.execute(sql)
			results = self.cursor.fetchall()
			return results
		except MySQLdb.Error as e:
			print "Error: Unable to update field: %s" % (e)
			self.db.close
