-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: j4d101.p.ssafy.io    Database: jjal
-- ------------------------------------------------------
-- Server version	8.0.23

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `board`
--

DROP TABLE IF EXISTS `board`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `board` (
  `board_no` int NOT NULL AUTO_INCREMENT COMMENT 'board_no',
  `title` varchar(200) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `content` longtext CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT 'content',
  `content_type` varchar(200) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT 'content_type',
  `nickname` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT 'nickname',
  `password` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT 'password',
  `ip` varchar(16) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT 'ip',
  `good` int NOT NULL DEFAULT '0' COMMENT 'good',
  `regdate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `view_cnt` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`board_no`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='board';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `board`
--

LOCK TABLES `board` WRITE;
/*!40000 ALTER TABLE `board` DISABLE KEYS */;
INSERT INTO `board` VALUES (1,'test','{\"url\":\"/api/v1/content/video/68d8f46b09ef4f8ea58914bab89868cd.mp4\", \"content\":\"test\"}','video','test','test','13.124.194.207',0,'2021-04-01 05:13:49',1);
/*!40000 ALTER TABLE `board` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment` (
  `comment_no` int NOT NULL AUTO_INCREMENT COMMENT 'comment_no',
  `board_no` int NOT NULL COMMENT 'board_no',
  `content` longtext NOT NULL COMMENT 'comment',
  `nickname` varchar(45) NOT NULL COMMENT 'nickname',
  `password` varchar(100) NOT NULL COMMENT 'password',
  `ip` varchar(16) NOT NULL COMMENT 'ip',
  `regdate` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`comment_no`),
  KEY `FK_comment_board_no_board_board_no` (`board_no`),
  CONSTRAINT `FK_comment_board_no_board_board_no` FOREIGN KEY (`board_no`) REFERENCES `board` (`board_no`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='comment';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `goodlist`
--

DROP TABLE IF EXISTS `goodlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `goodlist` (
  `good_no` int NOT NULL AUTO_INCREMENT COMMENT 'good_no',
  `board_no` int NOT NULL COMMENT 'board_no',
  `ip` varchar(16) NOT NULL COMMENT 'ip',
  PRIMARY KEY (`good_no`),
  KEY `FK_goodlist_board_no_board_board_no` (`board_no`),
  CONSTRAINT `FK_goodlist_board_no_board_board_no` FOREIGN KEY (`board_no`) REFERENCES `board` (`board_no`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='goodlist';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `goodlist`
--

LOCK TABLES `goodlist` WRITE;
/*!40000 ALTER TABLE `goodlist` DISABLE KEYS */;
/*!40000 ALTER TABLE `goodlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `most`
--

DROP TABLE IF EXISTS `most`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `most` (
  `most_no` int NOT NULL AUTO_INCREMENT COMMENT 'most_no',
  `most_count` int NOT NULL DEFAULT '0' COMMENT 'count',
  `most_name` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT 'name',
  `most_type` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT 'type',
  PRIMARY KEY (`most_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='most';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `most`
--

LOCK TABLES `most` WRITE;
/*!40000 ALTER TABLE `most` DISABLE KEYS */;
/*!40000 ALTER TABLE `most` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shareboard`
--

DROP TABLE IF EXISTS `shareboard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shareboard` (
  `s_board_no` int NOT NULL AUTO_INCREMENT COMMENT 's_board_no',
  `content` varchar(200) NOT NULL COMMENT 'content',
  `content_type` varchar(100) NOT NULL COMMENT 'content_type',
  `nickname` varchar(100) NOT NULL COMMENT 'nickname',
  `ip` varchar(16) NOT NULL COMMENT 'ip',
  `regdate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`s_board_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='shareboard';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shareboard`
--

LOCK TABLES `shareboard` WRITE;
/*!40000 ALTER TABLE `shareboard` DISABLE KEYS */;
/*!40000 ALTER TABLE `shareboard` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-04-01 14:14:24
