SET Global event_scheduler = ON
 
CREATE EVENT IF NOT EXISTS overdue_books
ON SCHEDULE EVERY 1 MINUTE 
DO UPDATE transactions
SET status = 'Overdue'
WHERE return_date IS NULL
 
SET SQL_SAFE_UPDATES = 0;

CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    book_title VARCHAR(255) NOT NULL,
    book_author VARCHAR(255),
    copy INT DEFAULT 1,
    cover VARCHAR(255),
    rfid VARCHAR(100) UNIQUE,
    status ENUM('Available', 'Unavailable') DEFAULT 'Available'
);


CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    user_id VARCHAR(50) NOT NULL,
    user_name VARCHAR(100),
    user_email VARCHAR(100),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    due_date DATE,
    status ENUM('Borrowed', 'Returned'),
    
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);


CREATE TABLE activity_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    action VARCHAR(50),
    book_id VARCHAR(50),
    book_title VARCHAR(255),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

