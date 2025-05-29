
----------------------------------  CREATE TABLES  ----------------------------------
CREATE TABLE `books` (
  `book_id` VARCHAR(20) NOT NULL,
  `book_title` VARCHAR(255) NOT NULL,
  `book_author` VARCHAR(255) DEFAULT NULL,
  `cover` VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (`book_id`)
) 

CREATE TABLE `book_items` (
  `item_id` INT NOT NULL AUTO_INCREMENT,
  `book_id` VARCHAR(20) DEFAULT NULL,
  `rfid` VARCHAR(20) DEFAULT NULL,
  `status` ENUM('Available','Borrowed','Lost','Damaged') DEFAULT 'Available',
  `date_added` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`item_id`),
  UNIQUE KEY `rfid` (`rfid`),
  KEY `book_id` (`book_id`),
  FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`) ON DELETE CASCADE ON UPDATE CASCADE
) 

CREATE TABLE `activity_log` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `action` VARCHAR(50) DEFAULT NULL,
  `rfid` VARCHAR(50) DEFAULT NULL,
  `user_id` INT DEFAULT NULL,
  `user_name` VARCHAR(100) DEFAULT NULL,
  `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `rfid` (`rfid`),
  FOREIGN KEY (`rfid`) REFERENCES `book_items` (`rfid`)
) 

CREATE TABLE `transactions` (
  `transaction_id` INT NOT NULL AUTO_INCREMENT,
  `book_id` VARCHAR(20) NOT NULL,
  `user_id` VARCHAR(50) NOT NULL,
  `user_name` VARCHAR(100) DEFAULT NULL,
  `user_email` VARCHAR(100) DEFAULT NULL,
  `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `due_date` DATETIME DEFAULT NULL,
  `return_date` DATETIME DEFAULT NULL,
  `status` ENUM('Borrowed','Returned','Overdue') DEFAULT 'Borrowed',
  `overdue_notified` TINYINT(1) DEFAULT '0',
  PRIMARY KEY (`transaction_id`),
  KEY `book_id` (`book_id`),
  FOREIGN KEY (`book_id`) REFERENCES `books` (`book_id`) ON DELETE CASCADE ON UPDATE CASCADE
) 

----------------------------------  EVENTS  ----------------------------------

SET Global event_scheduler = ON

CREATE EVENT IF NOT EXISTS overdue_books 
ON SCHEDULE EVERY 1 MINUTE  
DO UPDATE transactions   
SET status = 'Overdue'
WHERE due_date < CURRENT_TIMESTAMP()
AND status = 'Borrowed'
AND overdue_notified = TRUE


