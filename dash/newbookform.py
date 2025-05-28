import customtkinter as ctk
from core.database import Database
from core.widgets import ConfirmationDialog, center_window

class BookForm(ctk.CTkToplevel):
    def __init__(self, parent, book_data=None, on_update=None):
        super().__init__(parent)
        self.parent = parent
        self.db = Database()
       
        self.title("Update Book Details")
        center_window(self, 450, 400)
        self.resizable(False, False)
        self.focus()
        self.grab_set()
        self.on_update = on_update

        self.book_data = book_data or {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_columnconfigure(1, weight=1)
    
        self.action = ""
        if self.book_data:
            self.action = "Update Book"
        else:
            self.action = "Add New Book"

        ctk.CTkLabel(self.frame, text=self.action, font=("Helvetica", 20, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

        # BOOK DETAILS
        self.book_id_entry = self.create_labeled_entry("Book ID: ", 1, "Book ID")
        self.rfid_entry = self.create_labeled_entry("RFID: ", 2, "RFID")
        self.book_title_entry = self.create_labeled_entry("Book Title: ", 3, "Book Title")
        self.author_entry = self.create_labeled_entry("Author: ", 4, "Book Author")
        self.status_entry = self.create_labeled_entry("Status: ", 7, "'Available', 'Lost', 'Damaged', 'Borrowed'")
        self.cover_entry = self.create_labeled_entry("Cover Path: ", 9, "assets/book_covers/title-of-the-book.jpeg")
        
        self.buttons = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons.grid(row=8, column=0, sticky="ne")

        self.button_name = ""
        if self.book_data:
            self.button_name = "Update"
        else:
            self.button_name = "Add"

        self.action_btn = ctk.CTkButton(self.buttons, text=self.button_name, width=100, command=self.confirm_send)
        self.action_btn.grid(row=0, column=1, padx=5, pady=10)
        
        self.cancel_btn = ctk.CTkButton(self.buttons, text="Cancel", width=100)
        self.cancel_btn.grid(row=0, column=0, padx=5, pady=10)

        if self.book_data:
            self.set_book_data()

        # self.after(100, self.set_grab)

    def create_labeled_entry(self, label, row, placeholder):
        ctk.CTkLabel(self.frame, text=label).grid(row=row, column=0, sticky="e", padx=10, pady=5)
        entry = ctk.CTkEntry(self.frame, placeholder_text=placeholder, width=300)
        entry.grid(row=row, column=1, sticky="e", padx=10, pady=5)
        return entry

    # def set_grab(self):
    #     self.grab_set()

    def confirm_send(self):
        ConfirmationDialog(self, 
                           f"Are you sure you want to add '{self.book_title_entry.get().strip()}'?", 
                           self.insert_new_book)

    def get_book_data(self):
        book_data = {
            "id": self.book_id_entry.get().strip(),
            "rfid": self.rfid_entry.get().strip(),
            "title": self.book_title_entry.get().strip(),
            "author": self.author_entry.get().strip(),
            "cover": self.db.generate_path(self.book_title_entry.get().strip()),
            "status": self.status_entry.get().strip(),
        }
        return book_data

    def insert_new_book(self):
        book = self.get_book_data()
        book_id = book["id"]
        book_rfid = book["rfid"]
        book_title = book["title"]
        book_author = book["author"]
        book_cover = book["cover"]
        book_status = book["status"]


        try:
            query_book = """
            INSERT INTO books (book_id, book_title, book_author, cover) 
            VALUES (%s, %s, %s, %s)        
            """
            metadata = (book_id, book_title, book_author, book_cover)
            # Insert book metadata in books table
            self.db.execute_query(query_book, metadata)
            self.db.connection.commit()

            # book = self.db.fetch_one("SELECT book_id FROM books WHERE book_title = %s", (book_data["title"], ))
            print(f"Book {book_title} added successfully.")

        except Exception as e:
            print("Insert in books table failed :", e)

        try:
            query_item = """
            INSERT INTO book_items (book_id, rfid, status)
            VALUES (%s, %s, %s)
            """
            book_item = (book_id, book_rfid, book_status)

            # Insert individual book item in book_items table
            self.db.execute_query(query_item, book_item)
            self.db.connection.commit()
            self.db.log_activity("ADDED", book_rfid, user_name="Admin")
            print(f"Copy of the book '{book_title}' added successfully")
        except Exception as e:
            print("Insert in book_items table failed :", e)
            
    def set_book_data(self):
        self.book_id_entry.insert(0, self.book_data.get("book_id", ""))
        self.rfid_entry.insert(0, self.book_data.get("rfid", ""))
        self.book_title_entry.insert(0, self.book_data.get("book_title", ""))
        self.author_entry.insert(0, self.book_data.get("book_author", ""))
        self.status_entry.insert(0, self.book_data.get("status", ""))
        self.cover_entry.insert(0, self.book_data.get("cover", ""))

    #     if self.on_update:
    #         self.on_update()  
    #     else:
    #         print("Book data:", book_data)

        
    #     self.destroy()


if __name__ == "__main__":
    root = ctk.CTk()
    root.title("testing window")
    root.geometry("450x400")
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    center_window(root, 800, 400)
    newBookForm = BookForm(root)
    newBookForm.grid(row=0, column=0)

    root.mainloop()
