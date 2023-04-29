-- MySQL dump 10.17  Distrib 10.3.25-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: uas_projects
-- ------------------------------------------------------
-- Server version	10.3.25-MariaDB-0ubuntu0.20.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `visualization_project`
--

DROP TABLE IF EXISTS `visualization_project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `visualization_project` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(200) NOT NULL,
  `Project` int(11) NOT NULL,
  `Path` varchar(2000) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=390 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `project`
--

DROP TABLE IF EXISTS `project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `project` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(1000) CHARACTER SET utf8 NOT NULL,
  `Crop` int(11) NOT NULL,
  `PlantingDate` varchar(20) CHARACTER SET utf8 NOT NULL,
  `HarvestDate` varchar(20) CHARACTER SET utf8 DEFAULT NULL,
  `Description` varchar(3000) CHARACTER SET utf8 DEFAULT NULL,
  `CenterLat` float NOT NULL,
  `CenterLng` float NOT NULL,
  `MinZoom` int(11) NOT NULL,
  `MaxZoom` int(11) NOT NULL,
  `DefaultZoom` int(11) NOT NULL,
  `VisualizationPage` varchar(1000) CHARACTER SET utf8 NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `visualization_group`
--

DROP TABLE IF EXISTS `visualization_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `visualization_group` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(200) NOT NULL,
  `Type` varchar(3) NOT NULL,
  `Project` int(11) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `Project` (`Project`),
  CONSTRAINT `group_project_relation` FOREIGN KEY (`Project`) REFERENCES `visualization_project` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=624 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `product_type`
--

DROP TABLE IF EXISTS `product_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product_type` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(500) CHARACTER SET utf8 NOT NULL,
  `Type` varchar(2) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `imagery_product`
--

DROP TABLE IF EXISTS `imagery_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `imagery_product` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Flight` int(11) DEFAULT NULL,
  `Type` int(11) DEFAULT NULL,
  `Bands` varchar(10) DEFAULT NULL,
  `MinZoom` int(11) NOT NULL DEFAULT 17,
  `MaxZoom` int(11) NOT NULL DEFAULT 25,
  `Zoom` int(11) NOT NULL DEFAULT 19,
  `EPSG` int(11) NOT NULL DEFAULT 32614,
  `FileName` varchar(200) NOT NULL,
  `Size` float NOT NULL,
  `ChunkCount` int(11) NOT NULL,
  `Status` varchar(10) NOT NULL,
  `TempFolder` varchar(1000) NOT NULL DEFAULT '',
  `UploadFolder` varchar(1000) NOT NULL DEFAULT '',
  `DownloadPath` varchar(2000) NOT NULL DEFAULT '',
  `DisplayPath` varchar(2000) NOT NULL DEFAULT '',
  `ThumbPath` varchar(2000) NOT NULL DEFAULT '',
  `TMSPath` varchar(2000) NOT NULL DEFAULT '',
  `Boundary` varchar(200) NOT NULL DEFAULT '',
  `Identifier` varchar(300) NOT NULL,
  `Progress` int(11) DEFAULT NULL,
  `LastUpdate` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `Uploader` varchar(50) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Identifier` (`Identifier`),
  KEY `Flight` (`Flight`),
  KEY `Type` (`Type`),
  CONSTRAINT `product_flight_relation` FOREIGN KEY (`Flight`) REFERENCES `flight` (`ID`),
  CONSTRAINT `product_type_relation` FOREIGN KEY (`Type`) REFERENCES `product_type` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `flight`
--

DROP TABLE IF EXISTS `flight`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `flight` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(1000) CHARACTER SET utf8 NOT NULL,
  `Date` varchar(20) CHARACTER SET utf8 NOT NULL,
  `Project` int(11) NOT NULL,
  `Platform` int(11) NOT NULL,
  `Sensor` int(11) NOT NULL,
  `Altitude` float NOT NULL,
  `Forward` float NOT NULL,
  `Side` float NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `Project` (`Project`),
  KEY `Platform` (`Platform`),
  KEY `Sensor` (`Sensor`),
  CONSTRAINT `flight_platform_relation` FOREIGN KEY (`Platform`) REFERENCES `platform` (`ID`),
  CONSTRAINT `flight_project_relation` FOREIGN KEY (`Project`) REFERENCES `project` (`ID`),
  CONSTRAINT `flight_sensor_relation` FOREIGN KEY (`Sensor`) REFERENCES `sensor` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=1337 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `visualization_layer`
--

DROP TABLE IF EXISTS `visualization_layer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `visualization_layer` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Layer` int(11) NOT NULL,
  `GroupID` int(11) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `GroupID` (`GroupID`),
  CONSTRAINT `layer_group_relation` FOREIGN KEY (`GroupID`) REFERENCES `visualization_group` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3831 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping events for database 'uas_projects'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-01-25 23:00:22
