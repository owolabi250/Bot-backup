 -- delete database if exixt

DROP DATABASE IF EXISTS BotSchedule;

 -- Creates database if not exist

CREATE DATABASE IF NOT EXISTS BotSchedule;

 -- Switch database to new database

USE BotSchedule;

-- create user if not exists and set password, privileges

CREATE USER IF NOT EXISTS 'BotSchedule'@'localhost';
SET PASSWORD FOR 'BotSchedule'@'localhost' = 'BotSchedule';
GRANT ALL PRIVILEGES ON BotSchedule.* TO 'BotSchedule'@'localhost';
GRANT SELECT ON performance_schema.* TO 'BotSchedule'@'localhost';

  -- Table structure for table `cities`

  -- delete table if exist

DROP TABLE IF EXISTS `January`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
  /*!40101 SET character_set_client = utf8 */;

  --create table
CREATE TABLE `January` (
    `ID` int NOT NULL AUTO_INCREMENT,
    `Days` VARCHAR(50),
    `Course` VARCHAR(50),
    `Topic` VARCHAR(50),
    `Reminder` VARCHAR(50),
    `Target` INT,
    `Average` INT,
    `created_at` VARCHAR(50),
    `updated_at` VARCHAR(50),
    PRIMARY KEY(`ID`)
  );
