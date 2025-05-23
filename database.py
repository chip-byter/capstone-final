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
       self.cursor = self.connection.cursor()

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


if __name__ == "__main__":
    db = Database()
    
    results = db.fetch_one("SELECT password_hash FROM users WHERE username = %s", ('staff', ))
    # results = db.execute_query("")
    print(results[0])