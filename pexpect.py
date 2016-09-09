#!/usr/bin/python

import re
import pexpect
import getpass

try:
	password = getpass.getpass('password: ')
	child = pexpect.spawn("ssh youit@189.42.52.67 -p 7222 get system status")
	child.expect(".*assword:")
	child.sendline(password)
	child.expect(pexpect.EOF)
	systemOutput = child.before
	FGTSerial = ""
	FGTHostname = ""

	regexHostname = r"(Hostname:)\ (\w+)"
	if re.search(regexHostname, systemOutput):
		strFind = re.search(regexHostname, systemOutput)
		FGTHostname = strFind.group(2)

	regexSerial = r"(Serial\-Number:)\ (\w+)"
	if re.search(regexSerial, systemOutput):
		strFind = re.search(regexSerial, systemOutput)
		FGTSerial = strFind.group(2)

	print FGTSerial

except pexpect.ExceptionPexpect, e:
	print "error: %s" % (e)
