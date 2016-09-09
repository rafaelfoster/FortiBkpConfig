# INSERT INTO fgt_devices (STATUS, NAME, SERIAL, CLIENT, IP, IP2, PORT, USER, PASSWORD, FREQ_CHECK) 
	values(0,"HDAA_FW01","FG100D3G12808753","HDAA","189.42.52.67","127.0.0.1",7222,"youfortibkp","Ukd3UTGAiLxjjXGLAQ0oNHjHKQrB",30);



	def check_conn(IPAddr, Port):
		s = socket.socket()
		try:
			s.connect((IPAddr, Port))
			print "IP: %s  -  [ OK ]" % (IPAddr)
			return True
		except Exception as e: 
			print("something's wrong with %s:%d. Exception is %s" % (IPAddr, Port, e))
		finally:
			s.close()

	def getFGTInfo(FGTSystemstatus):
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

		FGTDeviceInfo = (FGTHostname, FGTSerial)
		return FGTDeviceInfo

	def execFGTBackup(objFGTConn):
		strBackupCMD = 'exec backup full-config ftp "/" admin.youit.com.br fortinet aY19kRsyDcPZsAaw3Y4e91w1QXf6jD3DfEE5twz9Xa6uMHcH'
	#	child.

	def getFGTOutput(FGTDevice,COMMAND):
		ID         = FGTDevice[0]
		STATUS     = FGTDevice[1]
		NAME	   = FGTDevice[2]
		SERIAL     = FGTDevice[3]
		CLIENT     = FGTDevice[4]
		IP         = FGTDevice[5]
		IP2        = FGTDevice[6]
		PORT	   = FGTDevice[7]
		USER       = FGTDevice[8]
		PASSWORD   = FGTDevice[9]
		FREQ_CHECK = FGTDevice[10]

		USER       = "youit"
		PASSWORD   = "10hdaa10" 

		if not check_conn(IP, PORT):
			if not check_conn(IP2, PORT):
				print "There's no connection to Fortigate IP"
				return False
			else:
				IPAddr = IP2
		else:
			IPAddr = IP


		try:
			strFGTConnection = "ssh %s@%s -p %s %s" % (USER, IPAddr, PORT, COMMAND)
			child = pexpect.spawn(strFGTConnection)
			child.expect(".*assword:")
			child.sendline(PASSWORD)
			i = child.expect (['Permission denied', '[#\$] '])
			if i==0:
				print('Permission denied on host. Can\'t login')
				child.kill(1)
				return False
			elif i == 1:
				child.expect(pexpect.EOF)
				FGTOutput = child.before
				return FGTOutput
		except pexpect.ExceptionPexpect, e:
			print "error: %s" % (e)

	def 
			FGTInfo = getFGTInfo(FGTSystemstatus)
				print FGTInfo[0]
				print FGTInfo[1]
				
	def runFGTBackup()
		strExecBackupCMD =  'exec backup full-config ftp "/backup_cfg_%s.cfg" admin.youit.com.br fortinet aY19kRsyDcPZsAaw3Y4e91w1QXf6jD3DfEE5twz9Xa6uMHcH' % (self.FGTSerial)
		child.sendline(strExecBackupCMD)
		print child.before
#			execFGTBackup(child)
		print "\n\n ------------------ \n "