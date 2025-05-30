import customtkinter as ctk
from core.database import Database
from core.widgets import ConfirmationDialog, center_window

class BookForm(ctk.CTkToplevel):
    def __init__(self, parent, book_data=None, on_update=None):
        super().__init__(parent)
        self.parent = parent
        self.db = Database()
       
        self.book_data = book_data or {}
        self.action = ""
        if self.book_data:
            self.action = "Update Book"
        else:
            self.action = "Add New Book"

        self.title(self.action)

        center_window(self, 450, 350)
        self.resizable(False, False)
        self.focus_force()   
        # self.grab_set()
        self.on_update = on_update


        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_columnconfigure(1, weight=1)
    

        ctk.CTkLabel(self.frame, text=self.action, font=("Helvetica", 20, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

        # BOOK DETAILS
        self.book_id_entry = self.create_labeled_entry("Book ID: ", 1, "Book ID")
        self.rfid_entry = self.create_labeled_entry("RFID: ", 2, "RFID")
        self.book_title_entry = self.create_labeled_entry("Title: ", 3, "Book Title")
        self.author_entry = self.create_labeled_entry("Author: ", 4, "Book Author")
        self.status_entry = self.create_labeled_entry("Status: ", 5, "'Available', 'Lost', 'Damaged', 'Borrowed'")
       
        # CHECKS EXISTING BOOKS
        self.book_id_entry.bind("<FocusOut>", self.check_existing_book)
        # ENABLE FIELDS 
        self.book_id_entry.bind("<KeyRelease>", self.on_book_id_change)

        self.buttons = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons.grid(row=1, column=0, sticky="ne")

        button_name = "Update" if self.book_data else "Add"

        self.action_btn = ctk.CTkButton(self.buttons, text=button_name, width=100, command=lambda: self.confirm_send(button_name))
        self.action_btn.grid(row=0, column=1, padx=5, pady=10)
        
        self.cancel_btn = ctk.CTkButton(self.buttons, text="Cancel", width=100, command=self.cancel)
        self.cancel_btn.grid(row=0, column=0, padx=5, pady=10)

        if self.book_data:
            self.set_book_data()

        self.after(100, self.set_grab)

    def create_labeled_entry(self, label, row, placeholder):
        ctk.CTkLabel(self.frame, text=label).grid(row=row, column=0, sticky="e", padx=(15,5), pady=5)
        entry = ctk.CTkEntry(self.frame, placeholder_text=placeholder, width=300)
        entry.grid(row=row, column=1, sticky="ew", padx=(5, 15), pady=5)
        return entry

    def set_grab(self):
        self.grab_set()

    def confirm_send(self, action):
        book_title = self.book_title_entry.get().strip()
        ConfirmationDialog(self, f"Are you sure you want to {action} '{book_title}'?", self.send_data)

    def get_book_data(self):
        return {
            "id": self.book_id_entry.get().strip(),
            "rfid": self.rfid_entry.get().strip(),
            "title": self.book_title_entry.get().strip(),
            "author": self.author_entry.get().strip(),
            "status": self.status_entry.get().strip(),
        }

    def check_existing_book(self, event=None):
        book_id = self.book_id_entry.get().strip()
        if not book_id:
            return

        query = "SELECT book_title, book_author FROM books WHERE book_id = %s"
        result = self.db.fetch_one(query, (book_id,))
        
        if result:
            self.book_title_entry.delete(0, 'end')
            self.book_title_entry.insert(0, result['book_title'])
            self.author_entry.delete(0, 'end')
            self.author_entry.insert(0, result['book_author'] or "")
            
            self.book_title_entry.configure(state="disabled")
            self.author_entry.configure(state="disabled")

    def on_book_id_change(self, event=None):
        self.book_title_entry.configure(state="normal")
        self.author_entry.configure(state="normal")
        self.book_title_entry.delete(0, 'end')
        self.author_entry.delete(0, 'end')

    def send_data(self):
        book = self.get_book_data()
        book_id = book["id"]
        book_rfid = book["rfid"]
        book_title = book["title"]
        book_author = book["author"]
        book_status = book["status"]
        book_cover = self.db.generate_path(book_title)

        try:
            # Check if book exists
            book_exists = self.db.fetch_one("SELECT 1 FROM books WHERE book_id = %s", (book_id,))
            
            # Check if this specific book item exists
            item_exists = self.db.fetch_one("SELECT 1 FROM book_items WHERE rfid = %s", (book_rfid,))
            
            if book_exists:
                # Update the book metadata
                query_book = """
                    UPDATE books 
                    SET book_title = %s, book_author = %s
                    WHERE book_id = %s
                """
                self.db.execute_query(query_book, (book_title, book_author, book_id))
            else:
                # Insert new book
                query_book = """
                    INSERT INTO books (book_id, book_title, book_author, cover)
                    VALUES (%s, %s, %s, %s)
                """
                self.db.execute_query(query_book, (book_id, book_title, book_author, book_cover))
            
            if item_exists:
                # Update existing book item (copy)
                query_item = """
                    UPDATE book_items 
                    SET status = %s 
                    WHERE rfid = %s
                """
                self.db.execute_query(query_item, (book_status, book_rfid))
                self.db.log_activity("Updated Copy", book_rfid, user_name="Admin")
            else:
                # Add new book item (copy)
                query_item = """
                    INSERT INTO book_items (book_id, rfid, status)
                    VALUES (%s, %s, %s)
                """
                self.db.execute_query(query_item, (book_id, book_rfid, book_status))
                self.db.log_activity("New Copy Added", book_rfid, user_name="Admin")

            self.db.connection.commit()
            print(f"Book '{book_title}' processed successfully.")

        except Exception as e:
            print("Database operation failed:", e)

        if self.on_update:
            self.on_update()
        self.destroy()

    def set_book_data(self):
        self.book_id_entry.insert(0, self.book_data.get("book_id", ""))
        self.rfid_entry.insert(0, self.book_data.get("rfid", ""))
        self.book_title_entry.insert(0, self.book_data.get("book_title", ""))
        self.author_entry.insert(0, self.book_data.get("book_author", ""))
        self.status_entry.insert(0, self.book_data.get("status", ""))

        
    def cancel(self):
        ConfirmationDialog(self, "Do you want to close this form?", self.destroy)

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
