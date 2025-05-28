import customtkinter as ctk
from core.database import Database
from core.widgets import ConfirmationDialog, center_window

class BookForm(ctk.CTkToplevel):
    def __init__(self, parent, book_data=None, on_update=None):
        super().__init__(parent)
        self.parent = parent
        self.title("Update Book Details")
        center_window(self, 450, 400)
        # self.resizable(False, False)
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
        self.cover_entry = self.create_labeled_entry("Book Cover Path: ", 9, "assets/book_covers/title-of-the-book.jpeg")
        
        self.buttons = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons.grid(row=8, column=0, sticky="ne")

        self.button_name = ""
        if self.book_data:
            self.button_name = "Update"
        else:
            self.button_name = "Add"

        self.action_btn = ctk.CTkButton(self.buttons, text=self.button_name, width=100, command=self.confirm_send)
        self.action_btn.grid(row=0, column=1, padx=5, pady=10)
        
        self.cancel_btn = ctk.CTkButton(self.buttons, text="Cancel", width=100, command=self.destroy)
        self.cancel_btn.grid(row=0, column=0, padx=5, pady=10)

        if self.book_data:
            self.book_id_entry.insert(0, self.book_data.get("book_id", ""))
            self.rfid_entry.insert(0, self.book_data.get("rfid", ""))
            self.book_title_entry.insert(0, self.book_data.get("book_title", ""))
            self.author_entry.insert(0, self.book_data.get("book_author", ""))
            self.status_entry.insert(0, self.book_data.get("status", ""))
            self.cover_entry.insert(0, self.book_data.get("cover", ""))

        self.after(100, self.set_grab)

    def set_grab(self):
        self.grab_set()

    def confirm_send(self):
        ConfirmationDialog(self, f"Are you sure you want to add '{self.title_entry.get().strip()}'?", self.send)

    def send(self):
        db = Database()
        
        book_data = {
            "id": self.id_entry.get().strip(),
            "title": self.title_entry.get().strip(),
            "author": self.author_entry.get().strip(),
            "copy": int(self.copy_entry.get().strip()),
            "rfid": self.rfid_entry.get().strip(),
            "cover": db.generate_path(self.title_entry.get().strip()),
            "status": self.status_entry.get().strip(),
        }

        if self.book_data:  # means you're updating
            try:
                db.execute_query("""
                    UPDATE books 
                    SET book_title=%s, book_author=%s, copy=%s, rfid=%s, cover=%s, status=%s
                    WHERE book_id=%s
                """, (
                    book_data["title"], 
                    book_data["author"],
                    book_data["copy"],
                    book_data["rfid"],
                    book_data["cover"],
                    book_data["status"],
                    book_data["id"]
                ))
                db.connection.commit()
                db.log_activity("Updated", book_data['id'], book_data['title'])
                print(f"Book {book_data['title']} updated successfully.")
            except Exception as e:
                print("Update failed:", e)

        else:  # INSERT new book
            try:
                db.execute_query("""
                    INSERT INTO books (book_title, book_author, copy, rfid, cover, status)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    book_data["title"],
                    book_data["author"],
                    book_data["copy"],
                    book_data["rfid"],
                    book_data["cover"],
                    book_data["status"]
                ))
                db.connection.commit()
                book = db.fetch_one("SELECT book_id FROM books WHERE book_title = %s", (book_data["title"], ))
                db.log_activity("Added", book['book_id'], book_data["title"])
                print(f"Book {book_data['title']} added successfully.")
            except Exception as e:
                print("Insert failed:", e)

        if self.on_update:
            self.on_update()  
        else:
            print("Book data:", book_data)

        
        self.destroy()
