from datetime import datetime, timedelta
import mysql.connector 
from mysql.connector import Error
import os
from dotenv import load_dotenv



class Database:
    def __init__(self):
        
        load_dotenv()

        DB_HOST = os.getenv("DB_HOST")
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_NAME = os.getenv("DB_NAME")

        self.connection = mysql.connector.connect(
            # host="localhost",
            # user="root",
            # password="admin123",
            # database="Library"
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def execute_query(self, query, params=None):
        self.cursor.execute(query, params)
        print("Successful Query!")
        return self.cursor.lastrowid

    def fetch_one(self, query:str, params=None):
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
    
    
    def log_activity(self, action, rfid, user_id=None, user_name=None):
        print(f"[LOG DEBUG] action={action}, rfid={rfid}, user_id={user_id}, user_name={user_name}")
        try:
            self.execute_query("INSERT INTO activity_log (action, rfid, user_id, user_name) VALUES (%s, %s, %s, %s)",
                               (action, rfid, user_id, user_name))
            self.connection.commit()
        except Exception as e:
            print(f"[LOG ERROR]: {e}")

    def get_books(self, query=None):
        q = """
            SELECT 
                books.book_id,
                books.book_title,
                books.book_author,
                books.cover,
                book_items.item_id,
                book_items.rfid,
                book_items.status
            FROM books
            INNER JOIN book_items ON books.book_id = book_items.book_id
            """

        if query:
            q += " WHERE books.book_title LIKE %s OR books.book_author LIKE %s or book_items.rfid = %s"
            params = (f"%{query}%", f"%{query}%", query)
            return q, params
        
        return q
    
    def get_book_by_rfid(self, rfid):
        rfid = ''.join(rfid.split())
        query = """
        SELECT
            bi.book_id,
            bi.rfid,
            b.book_title
        FROM book_items bi
        JOIN books b ON b.book_id = bi.book_id
        WHERE bi.rfid = %s 
        """
        self.cursor.execute(query, (rfid,))
        return self.cursor.fetchone()
    
    def get_overdue_books(self):
        query = """
        SELECT 
            t.rfid,
            t.user_name,
            t.user_email,
            t.borrowed_date,
            t.due_date,
            t.return_date,
            t.status,
            t.overdue_notified,
            b.book_title,
            bi.rfid
        FROM transactions t
        JOIN book_items bi ON bi.rfid = t.rfid
        JOIN books b ON b.book_id = bi.book_id
        WHERE t.status = 'Overdue' AND t.overdue_notified = FALSE;
        """

        return self.fetch_all(query)
    
    
    def mark_overdue_notified(self, rfid):
        query = """
            UPDATE transactions
            SET overdue_notified = TRUE
            WHERE rfid = %s
            AND status = 'Overdue'
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (rfid,))
            self.connection.commit()
            cursor.close()
        except Exception as e:
            print(f"Failed to mark overdue notified for RFID {rfid}: {e}")


    def get_book_status(self, rfid, user_id):
        query = """
            SELECT status FROM transactions
            WHERE rfid = %s AND user_id = %s
            ORDER BY borrowed_date DESC LIMIT 1
        """
        values =  (rfid, user_id)

        result = self.fetch_one(query, values)
        return result["status"] if result else "Available"
    
    def borrow_book(self, user_id, user_name, user_email, rfid, due_hours:int=None, due_days:int=None):
        self.cursor.execute("SELECT * FROM book_items WHERE rfid = %s", (rfid,))
        if not self.cursor.fetchone():
            print(f"[ERROR] RFID {rfid} does not exist in book_items.")
            return None
        
        delta = timedelta()
        if due_days:
            delta += timedelta(days=due_days)
        if due_hours:
            delta += timedelta(minutes=due_hours)
        due_date = datetime.now() + delta if delta else None

        try:
            self.cursor.execute("""
                INSERT INTO transactions (user_id, user_name, user_email, rfid, status, borrowed_date, due_date)
                VALUES (%s, %s, %s, %s, 'Borrowed', NOW(), %s)
            """, (user_id, user_name, user_email, rfid, due_date))

            self.cursor.execute("UPDATE book_items SET status = 'Borrowed' WHERE rfid = %s", (rfid,))
            self.connection.commit()
        except Error as e:
            self.connection.rollback()  
            print(f"Borrow Book Error: {e}")
        return due_date

    def return_book(self, user_id, rfid):
        try:
            self.cursor.execute("""
                UPDATE transactions 
                SET status = 'Returned', return_date = NOW()
                WHERE user_id = %s AND rfid = %s 
                AND status IN ('Borrowed', 'Overdue');
            """, (user_id, rfid))

            self.cursor.execute("UPDATE book_items SET status = 'Available' WHERE rfid = %s", (rfid,))
            self.connection.commit()
        except Error as e:
            self.connection.rollback()  
            print(f"Return Book Error: {e}")
   

    def generate_path(self, title:str):
        modified_title = title.lower().replace(" ", "-") + ".jpg"
        path = f"book_covers/{modified_title}"
        return path
    


if __name__ == "__main__":
    db = Database()
    
    # results = db.fetch_one("SELECT password_hash FROM users WHERE username = %s", ('staff', ))
    # results = db.execute_query("")
    # print(results[0])
    # title = "1984"
    # book_id = db.fetch_one("SELECT book_id FROM books WHERE book_title = %s", (title, ))
    # print(book_id["book_id"])
    # db.execute_query("DELETE FROM books WHERE book_id = %s", ('A000', ))
    # db.connection.commit()
    results = db.fetch_all("SELECT COUNT(*) FROM book_items WHERE book_id = %s", ('A111', ))
    print(results)
    