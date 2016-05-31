#!/usr/bin/python


import os
import re
import git
import yaml
import socket
import pexpect
from db import DB
from fgt import FGT
from log import LOG	

global cfg 
with open("config.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

defaultRepo = cfg['repofolder'] 

FTPUser = cfg['ftp']['FTPUser']
FTPPass = cfg['ftp']['FTPPass']
FTPHost = cfg['ftp']['FTPHost']

DBUser = cfg['database']['DBUser']
DBPass = cfg['database']['DBPass']
DBHost = cfg['database']['DBHost']
DBBase = cfg['database']['DBBase']

def main():	
	fgt = FGT()
	db = DB()
	os.chdir(defaultRepo)
	repo = git.Repo( defaultRepo )
	for FGTDevice in db.getAll():
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
	
		IPAddr = fgt.connFGT(IP, IP2, PORT)
		print IPAddr
		if IPAddr:
			outFGTInfo = fgt.runFGTCommand(USER, PASSWORD, IPAddr, PORT, "get system status")
			if "FortiOS" in outFGTInfo:
				FGTInfo = fgt.getFGTInfo(outFGTInfo)
				FGTName   = FGTInfo[0]
				FGTSerial = FGTInfo[1]

				if FGTInfo[0] != NAME:
						print "UPDATE NAME"
				if FGTInfo[1] != SERIAL:
						print "UPDATE SERIAL"

				clientRepo = "%s/%s" % (defaultRepo, CLIENT)
				if not os.path.exists(clientRepo):
					os.makedirs(clientRepo)
					uid = pwd.getpwnam(FTPUser).pw_uid
					gid = grp.getgrnam(FTPUser).gr_gid
					os.chown(clientRepo, uid, gid)

				bkpFile = "%s/bkp_fgtconfig_%s.conf" % (CLIENT, FGTSerial)

				strBkpCMD = 'exec backup full-config ftp %s %s %s %s' % (bkpFile, FTPHost, FTPUser, FTPPass)
				print strBkpCMD
				outFGTBkpInfo = fgt.runFGTCommand(USER, PASSWORD, IPAddr, PORT, strBkpCMD)
				print outFGTBkpInfo
				if "Send config file to ftp server OK" in outFGTBkpInfo:
					print "Backup OK"
					print "Starting to GIT"
					repo.git.add(bkpFile)
					CommitHash = ""
					fcommit = repo.git.commit( m='Initial commit' )
					regexGitHash = r"(.*)\ (\w+)\]\ (.*)"
					if re.search(regexGitHash, fcommit):
						strFind = re.search(regexGitHash, fcommit)
						CommitHash = strFind.group(2)
					print "Hash: %s" % (CommitHash)
				elif "Return code 10" in outFGTBkpInfo:
					print "Error: Login Failed"

if __name__ == "__main__":
	main()

