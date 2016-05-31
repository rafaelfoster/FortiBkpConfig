#!/usr/bin/python

import logging

class LOG(object):
	config  = ""
	logfile = ""
	logger  = ""

	def setup(self,cfg):
		self.config = cfg['log']['Destination']
		if "logfile" in self.config:
			self.logfile = cfg['log']['logfile']['logPath']

			self.logger = logging.getLogger(__name__)

			handler = logging.FileHandler('hello.log')
			handler.setLevel(logging.INFO)


	def writeline(self, line):

		if "logfile" in self.config:
			print "LogFile line"

		if "database" in self.config:
			print "DB line"
			
		
