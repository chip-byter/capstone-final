import hashlib
import logging
from core.database import Database

# Setup logging to file
logging.basicConfig(
    filename='user_actions.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def hash_string(input_string):
    return hashlib.sha256(input_string.encode()).hexdigest()

def create_user(username, password):
    password_hash = hash_string(password)
    try:
        con = Database()
        con.execute_query("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
        con.connection.commit()
        logging.info(f"User '{username}' added to database.")
        print("User successfully added!")
    except Exception as e:
        logging.error(f"Error inserting user '{username}': {e}")
        print(f"[ERROR] : {e}")
    finally:
        if con is not None and con.connection.is_connected():
            con.cursor.close()
            con.con.close()
            print("Database is closed!")


def verify_user(username, password):
    con = Database()
    hashpass = hash_string(password)
    stored_hash = con.fetch_one("SELECT password_hash FROM users WHERE username = %s", (username, )) 
    return stored_hash['password_hash'] == hashpass
    

if __name__ == "__main__":
    username = input("Enter username: ")
    password = input("Enter password: ")
    # create_user(username, password)

    if verify_user(username, password):
        print("Access Granted")
    else:
        print("Access Denied")