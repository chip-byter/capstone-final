CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id VARCHAR(20) NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    user_name VARCHAR(255),
    borrow_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    due_date DATETIME,
    return_date DATETIME,
    status ENUM('Borrowed', 'Returned', 'Overdue') DEFAULT 'borrowed',
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE
);

CREATE TABLE book_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id VARCHAR(20),
    rfid VARCHAR(20) UNIQUE,
    status ENUM('Available', 'Borrowed', 'Lost', 'Damaged') DEFAULT 'available',
    date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE activity_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    rfid VARCHAR(20),
    action VARCHAR(100), 
    user_id VARCHAR(50),
    user_name VARCHAR(255),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rfid) REFERENCES book_items(rfid) ON DELETE SET NULL
);