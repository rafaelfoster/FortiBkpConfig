#!/usr/bin/python

import os
import re
import git
import grp
import pwd
import sys
import yaml
import errno
import socket
import pexpect
import datetime
from db import DB
from fgt import FGT
from log import LOG

Debug = False
def main(configFile):
    today = datetime.date.today()
    commit_format_date = today.strftime('%d-%m-%Y')

    with open(configFile, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    with open("logmessages.yaml", 'r') as logfile:
        LOGM = yaml.load(logfile)

    if len(cfg) == 0:
        print "Could not obtain configs from config file."
        exit()

    defaultRepo = cfg['repofolder']
    FTPUser = cfg['ftp']['FTPUser']
    FTPPass = cfg['ftp']['FTPPass']
    FTPHost = cfg['ftp']['FTPHost']

    DBUser = cfg['database']['DBUser']
    DBPass = cfg['database']['DBPass']
    DBHost = cfg['database']['DBHost']
    DBBase = cfg['database']['DBBase']

    fgt = FGT()
    db = DB()
    db.setup(cfg['database'])
    if not os.path.exists(defaultRepo):
        print "Path does not exist. Creating it...."
        try:
            os.makedirs(defaultRepo)
        except OSError as e:
            print "Error on create repo directory: %s" % (e)
            return 1

        try:
            uid = pwd.getpwnam(cfg["ftp"]["FTPUser"]).pw_uid
            gid = grp.getgrnam(cfg["ftp"]["FTPUser"]).gr_gid
            os.chown(defaultRepo, uid, gid)
        except:
            print "Could not change folder user.\nThe user \'%s\' already exists?" % (cfg["ftp"]["FTPUser"])
            exit()

        git.Repo.init(defaultRepo)
    else:
        os.chdir(defaultRepo)

    gitRepo = "%s/%s" % (defaultRepo, ".git")
    if not os.path.exists(gitRepo):
        git.Repo.init(defaultRepo)

    repo = git.Repo( defaultRepo )

    for FGTDevice in db.getAll():
    	ID         = FGTDevice[0]
    	STATUS     = FGTDevice[1]
    	NAME	   = FGTDevice[2]
    	SERIAL     = FGTDevice[3]
    	LOCAL      = FGTDevice[4]
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
            if type(outFGTInfo) == int:
                logID = "FBC04%d" % (outFGTInfo)
                print LOGM[logID]
                exit()
            elif "FortiOS" in outFGTInfo:
                print "We're in!"
                FGTInfo = fgt.getFGTInfo(outFGTInfo)
                FGTName   = FGTInfo[0]
                FGTSerial = FGTInfo[1]

                print FGTName
                print FGTSerial

                if FGTName != NAME:
                    if db.updateDB("NAME", FGTName, ID) == False:
                        print "Error"
                        exit()

                if FGTSerial != SERIAL:
                    if db.updateDB("SERIAL", FGTSerial, ID) == False:
                        print "Error"
                        exit()

                exit()

                clientRepo = "%s/%s" % (defaultRepo, LOCAL)
                if not os.path.exists(clientRepo):
                    print "Path does not exist. Creating it...."
                    try:
                        os.makedirs(clientRepo)
                        uid = pwd.getpwnam(FTPUser).pw_uid
                        gid = grp.getgrnam(FTPUser).gr_gid
                        os.chown(clientRepo, uid, gid)
                    except OSError as e:
                        print "Error on create repo directory: %s" % (e)
                        return 1

                bkpFile = "%s/bkp_fgtconfig_%s.conf" % (LOCAL, FGTSerial)
                strBkpCMD = 'exec backup full-config ftp %s %s %s %s' % (bkpFile, FTPHost, FTPUser, FTPPass)
                print strBkpCMD
                outFGTBkpInfo = fgt.runFGTCommand(USER, PASSWORD, IPAddr, PORT, strBkpCMD)
                print outFGTBkpInfo
                if type(outFGTInfo) == int:
                    logID = "FBC04%d" % (outFGTInfo)
                    print LOGM[logID]
                    exit()
                elif "ftp server OK" in outFGTBkpInfo:
                    print "Backup OK"
                    print "Starting to GIT"
                    gitAddFile = repo.git.add(bkpFile)
                    CommitHash = ""
                    fcommit = repo.git.commit( m='Fortigate Backup Config on {date}'.format(date=commit_format_date) )
                    regexGitHash = r"(.*)\ (\w+)\]\ (.*)"
                    if re.search(regexGitHash, fcommit):
                        strFind = re.search(regexGitHash, fcommit)
                        CommitHash = strFind.group(2)
                        print "Hash: %s" % (CommitHash)
                    elif "Return code 10" in outFGTBkpInfo:
                        print "Error: Login Failed"

if __name__ == "__main__":
    configfile = "config.yaml"
    if sys.argv:
        for x in range(1,len(sys.argv)):
            if sys.argv[x] == "--configfile" or sys.argv[x] == "-c":
                configfile = sys.argv[x + 1]
                print "Loading file %s" % (configfile)

            if sys.argv[x] == "--debug":
                Debug = True

            if sys.argv[x] == "--help" or sys.argv[x] == "-h":
                print "--configfile or -c    [path/to/config/file]"

    main(configfile)
