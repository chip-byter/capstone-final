import customtkinter as ctk
from core.database import Database
from dash.newbookform import BookForm
from core.widgets import ConfirmationDialog, center_window


class BookDetailsWindow(ctk.CTkToplevel):
    def __init__(self, parent, book_data, on_update=None):
        super().__init__(parent)
        
        self.title("Book Details")
        center_window(self, 450, 350)
        self.resizable(False, False)
        self.focus_force()   
        # self.grab_set()
        self.on_update = on_update

        self.book = book_data or {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_columnconfigure(1, weight=1)
    
        ctk.CTkLabel(self.frame, text="Book Details", font=("Helvetica", 20, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
  
        # BOOK DETAILS
        self.book_id_entry = self.create_labeled_entry("Book ID: ", 1, "Book ID")
        self.rfid_entry = self.create_labeled_entry("RFID: ", 2, "NFC")
        self.book_title_entry = self.create_labeled_entry("Title: ", 3, "Book Title")
        self.author_entry = self.create_labeled_entry("Author: ", 4, "Book Author")
        self.status_entry = self.create_labeled_entry("Status: ", 5, "'Available', 'Lost', 'Damaged', 'Borrowed'")
        
        self.buttons = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons.grid(row=1, column=0, sticky="ne")

        self.update_btn = ctk.CTkButton(self.buttons, text="Update", width=100, fg_color="green", command=self.open_update_form)
        self.update_btn.grid(row=0, column=0, padx=5, pady=10)
        
        self.delete_btn = ctk.CTkButton(self.buttons, text="Delete", width=100, fg_color="brown", command=self.delete_book)
        self.delete_btn.grid(row=0, column=1, padx=5, pady=10)

        self.cancel_btn = ctk.CTkButton(self.buttons, text="Cancel", width=100, command=self.cancel)
        self.cancel_btn.grid(row=0, column=2, padx=5, pady=10)

        if self.on_update:
            self.on_update()

        if self.book:
            self.populate_entries()

        self.after(100, self.set_grab)

    def set_grab(self):
        self.grab_set()

    def create_labeled_entry(self, label, row, placeholder):
        ctk.CTkLabel(self.frame, text=label).grid(row=row, column=0, sticky="e", padx=10, pady=5)
        entry = ctk.CTkLabel(self.frame, text="", width=300, wraplength=300)
        entry.grid(row=row, column=1, sticky="w", padx=10, pady=5)
        return entry

    def open_update_form(self):
        def after_update():
            if self.on_update:
                self.on_update()
            self.destroy()

        # BookForm(self, self.book_data, on_update=after_update)
        BookForm(self, self.book, on_update=after_update)

    def get_book_data(self):
        book = {
            "id": self.book['book_id'],
            "rfid": self.book['rfid'],
            "title": self.book['book_title'],
            "author": self.book['book_author'],
            "status": self.book['status'],
        }
        return book

    def populate_entries(self):
        book = self.get_book_data()
        self.book_id_entry.configure(text=book['id'])
        self.rfid_entry.configure(text=book['rfid'])
        self.book_title_entry.configure(text=book['title'])
        self.author_entry.configure(text=book['author'])
        self.status_entry.configure(text=book['status'])

    def delete_book(self):
        db = Database()
        confirm = ctk.CTkInputDialog(text=f"Type DELETE to confirm deletion of the book\n{self.book['book_title']}.", title="Confirm Book Deletion")
        if confirm.get_input().strip().upper() == "DELETE":
            db.execute_query("DELETE FROM books WHERE book_id = %s", (self.book['book_id'],))
            db.log_activity("Deleted", self.book['book_id'], self.book['book_title'])
            db.connection.commit()
            if self.on_update:
                self.on_update()
            self.destroy()
    
    def cancel(self):
        ConfirmationDialog(self, "Do you want to close this form?", self.destroy)