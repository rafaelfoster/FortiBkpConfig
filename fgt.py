#!/usr/bin/python

import re
import pexpect
import socket
from db import DB

class FGT():

	def check_conn(self, IPAddr, Port):
		s = socket.socket()
		try:
			s.connect((IPAddr, Port))
			return True
		except Exception as e:
			return False
		finally:
			s.close()

	def connFGT(self,IP, IP2, PORT):
		if not self.check_conn(IP, PORT):
			if not self.check_conn(IP2, PORT):
				print "There's no connection to Fortigate"
				return False
			else:
				IPAddr = IP2
		else:
			IPAddr = IP

		return IPAddr

	def getFGTInfo(self,FGTSystemstatus):
		regexHostname = r"(Hostname:)\ (\w+)"
		if re.search(regexHostname, FGTSystemstatus):
			strFind = re.search(regexHostname, FGTSystemstatus)
			FGTHostname = strFind.group(2)
		else:
			FGTHostname = None

		regexSerial = r"(Serial\-Number:)\ (\w+)"
		if re.search(regexSerial, FGTSystemstatus):
			strFind = re.search(regexSerial, FGTSystemstatus)
			FGTSerial = strFind.group(2)
		else:
			FGTSerial = None

		FGTInfo = (FGTHostname,FGTSerial)
		return FGTInfo

	def runFGTCommand(self, USER, PASSWORD, IPAddr, PORT, COMMAND):
		try:
			strFGTConnection = "ssh %s@%s -p %s %s" % (USER, IPAddr, PORT, COMMAND)
			child = pexpect.spawn(strFGTConnection, timeout=60)
			child.expect(".*assword:")
			child.sendline(PASSWORD)
			i = child.expect (['Permission denied', '[#\$] '])
			if i == 0:
				child.kill(1)
				return 1
			elif i == 1:
				child.expect(pexpect.EOF)
				FGTOutput = child.before
				return FGTOutput
		except pexpect.ExceptionPexpect, e:
			if "timeout" in e:
				return 2
			else:
				print "error: %s" % (e)
				return 3
