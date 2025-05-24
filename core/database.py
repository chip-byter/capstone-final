from datetime import datetime, timedelta
import mysql.connector 
from mysql.connector import Error

class Database:
    def __init__(self):
       self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin123",
            database="capstone"
        )
       self.cursor = self.connection.cursor(dictionary=True)

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            print("Successful Query!")
            return self.cursor.lastrowid
        except Error as e:
            print(f"[QUERY ERROR] : {e}")
        # finally:
        #     if self is not None and self.con.is_connected():
        #         self.cursor.close()
        #         self.con.close()
        #         print("Database is closed!")

    def fetch_one(self, query:str, params=None):
        """ RETURNS ONE RESULT FROM THE QUERY

            ---
            - query: `SELECT * FROM table WHERE column = %s`
            - params: `(value, )`
        """
        try:
            self.cursor.execute(query, params)
            print("Successful Query!")
            return self.cursor.fetchone()
        except Error as e:
            print(f"[FETCH ONE ERROR] : {e}")
        
    def fetch_all(self, query:str, params=None):
        try: 
            self.cursor.execute(query, params)
            print("Successful Query!")
            return self.cursor.fetchall()
        except Error as e:
            print(f"[FETCH ALL ERROR] : {e}")
        # finally:
        #     if self is not None and self.con.is_connected():
        #         self.cursor.close()
        #         self.con.close()
        #         print("Database is closed!")
    
    def log_activity(self, action, book_id, book_title, user_id=None, user_name=None):
        try:
            self.execute_query("""
                INSERT INTO activity_log (action, book_id, book_title,  user_id, user_name))
                VALUES (%s, %s, %s, %s, %s)
            """, (action, book_id, book_title,  user_id, user_name))
            self.connection.commit()
            print(f"[LOGGED]: {action} - {book_id} - {book_title} - User: {user_name or 'System'}")
        except Exception as e:
            print(f"[LOG ERROR]: {e}")

    def get_book_by_rfid(self, rfid):
        rfid = ''.join(rfid.split())
        self.cursor.execute("SELECT book_id, book_title FROM books WHERE rfid = %s", (rfid,))
        return self.cursor.fetchone()

    def get_book_status(self, book_id, user_id):
        self.cursor.execute("""
            SELECT status FROM transactions
            WHERE book_id = %s AND user_id = %s
            ORDER BY timestamp DESC LIMIT 1
        """, (book_id, user_id))
        result = self.cursor.fetchone()
        return result["status"] if result else "Available"
    
    def borrow_book(self, user_id, user_name, user_email, book_id):
        due_date = datetime.now() + timedelta(minutes=1)
        try:
            self.cursor.execute("""
                INSERT INTO transactions (user_id, user_name, user_email, book_id, status, timestamp, due_date)
                VALUES (%s, %s, %s, %s, 'Borrowed', NOW(), %s)
            """, (user_id, user_name, user_email, book_id, due_date))
            self.cursor.execute("UPDATE books SET copy = copy - 1 WHERE book_id = %s", (book_id,))
            self.cursor.execute("UPDATE books SET status = 'Unavailable' WHERE book_id = %s AND copy <= 0", (book_id,))
            self.connection.commit()
        except Error as e:
            self.connect.rollback()  
            print(f"Borrow Book Error: {e}")
        return due_date

    def return_book(self, user_id, book_id):
        try:
            self.cursor.execute("""
                UPDATE transactions 
                SET status = 'Returned', return_date = NOW()
                WHERE user_id = %s AND book_id = %s 
                AND status IN ('Borrowed', 'Overdue');
            """, (user_id, book_id))

            self.cursor.execute("UPDATE books SET copy = copy + 1 WHERE book_id = %s", (book_id,))
            self.cursor.execute("UPDATE books SET status = 'Available' WHERE book_id = %s AND copy > 0", (book_id,))
            self.connection.commit()
        except Error as e:
            self.connect.rollback()  
            print(f"Return Book Error: {e}")

    def get_overdue_books(self):
        query = """
            SELECT tr.book_id, b.book_title AS book_title, tr.user_email, tr.user_name, tr.due_date
            FROM transactions tr
            JOIN books b ON tr.book_id = b.book_id
            WHERE tr.status = 'Overdue'
        """
        
        self.cursor.execute(query)
        results = self.cursor.fetchall()

        return results

    def reset_table(self, table_name:str):
        """ DELETE ALL ROWS OF THE TABLE

            ---
            table_name: 
            - `books`
            - `transactions`
            - `accounts`

        """
        try: 
            self.cursor.execute(f"DELETE FROM {table_name}")
            self.con().commit()
        except Error as e:
            print(f"[ERROR] : {e}")
        # finally:
        #     if self is not None and self.con.is_connected():
        #         self.cursor.close()
        #         self.con.close()
        #         print("Database is closed!")

    def generate_path(self, title:str):
        modified_title = title.lower().replace(" ", "-") + ".jpg"
        path = f"images/{modified_title}"
        return path
    
if __name__ == "__main__":
    db = Database()
    
    # results = db.fetch_one("SELECT password_hash FROM users WHERE username = %s", ('staff', ))
    # results = db.execute_query("")
    # print(results[0])
    title = "1984"
    book_id = db.fetch_one("SELECT book_id FROM books WHERE book_title = %s", (title, ))
    print(book_id["book_id"])
    # db.log_activity("Added", book_id, title)
    
    # results = db.fetch_one("SELECT password_hash FROM users WHERE username = %s", ('admin', ))
    # print(results)