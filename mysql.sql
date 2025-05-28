SET Global event_scheduler = ON

-- SET SQL_SAFE_UPDATES = 0;
 
-- CREATE EVENT IF NOT EXISTS overdue_books
-- ON SCHEDULE EVERY 1 MINUTE 
-- DO UPDATE transactions
-- SET status = 'Overdue'
-- WHERE return_date IS NULL
 
CREATE EVENT IF NOT EXISTS overdue_books 
ON SCHEDULE EVERY 1 MINUTE  
DO   UPDATE transactions   
SET status = 'Overdue', overdue_notified = 1
WHERE due_date < CURRENT_TIMESTAMP()
AND status = 'Borrowed'
p

CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    book_title VARCHAR(255) NOT NULL,
    book_author VARCHAR(255),
    copy INT DEFAULT 1,
    cover VARCHAR(255),
    rfid VARCHAR(100) UNIQUE,
    status ENUM('Available', 'Unavailable') DEFAULT 'Available'
);


CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash CHAR(64) NOT NULL
);


CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    user_id VARCHAR(50) NOT NULL,
    user_name VARCHAR(100),
    user_email VARCHAR(100),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    due_date DATETIME,
    return_date DATETIME,
    status ENUM('Borrowed', 'Returned', 'Overdue') DEFAULT 'Borrowed',
    overdue_notified TINYINT(1) DEFAULT 0,
    
    FOREIGN KEY (book_id) REFERENCES books(book_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE activity_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    action VARCHAR(50) NOT NULL,
    book_id VARCHAR(50),
    book_title VARCHAR(255),
    user_id VARCHAR(100),
    user_name VARCHAR(255),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

