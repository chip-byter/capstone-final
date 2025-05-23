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
    
    def log_activity(self, action, book_id, book_title):
        try:
            self.execute_query("""
                INSERT INTO activity_log (action, book_id, book_title)
                VALUES (%s, %s, %s)
            """, (action, book_id, book_title))
            self.connection.commit()
            print(f"[LOGGED]: {action} - {book_id} - {book_title} - SYSTEM AUTOMATED")
        except Exception as e:
            print(f"[LOG ERROR]: {e}")

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