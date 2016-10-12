-- MySQL dump 10.14  Distrib 5.5.52-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: fortibkpconfig
-- ------------------------------------------------------
-- Server version	5.5.52-MariaDB-1ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `fortibkpconfig`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `fortibkpconfig` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `fortibkpconfig`;

--
-- Table structure for table `fgt_bkp_log`
--

DROP TABLE IF EXISTS `fgt_bkp_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fgt_bkp_log` (
  `ID` int(10) NOT NULL AUTO_INCREMENT,
  `FGTID` int(3) NOT NULL,
  `DATE` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `LAST_STATUS` int(1) NOT NULL,
  `MESSAGE` varchar(100) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `FGTID` (`FGTID`),
  CONSTRAINT `fgt_bkp_log_ibfk_1` FOREIGN KEY (`FGTID`) REFERENCES `fgt_devices` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `fgt_devices`
--

DROP TABLE IF EXISTS `fgt_devices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fgt_devices` (
  `ID` int(3) NOT NULL AUTO_INCREMENT,
  `STATUS` tinyint(1) NOT NULL,
  `NAME` varchar(20) NOT NULL,
  `SERIAL` varchar(20) NOT NULL,
  `LOCAL` varchar(30) NOT NULL,
  `IP` varchar(15) NOT NULL,
  `IP2` varchar(15) DEFAULT NULL,
  `PORT` int(5) NOT NULL,
  `USER` varchar(20) NOT NULL,
  `PASSWORD` varchar(50) NOT NULL,
  `FREQ_CHECK` int(4) NOT NULL DEFAULT '30',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `IP` (`IP`),
  UNIQUE KEY `IP2` (`IP2`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-10-12 11:45:33
