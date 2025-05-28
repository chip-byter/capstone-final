import customtkinter as ctk
from core.database import Database
from dash.newbookform import BookForm
from core.widgets import center_window


class BookDetailsWindow(ctk.CTkToplevel):
    def __init__(self, parent, book_data, on_update=None):
        super().__init__(parent)
        
        self.resizable(False, False)
        self.title("Book Details")
        center_window(self, 450, 400)

        self.transient(parent) 
        self.focus_force()      

        self.book_data = book_data
        self.on_update = on_update

        self.book_id = book_data['book_id']
        self.book_title = book_data['book_title']
        self.book_author = book_data['book_author']
        self.book_cover = book_data['cover']
        self.book_copies = book_data['copy']
        self.book_rfid = book_data['rfid']
        self.book_status = book_data['status']

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        
        ctk.CTkLabel(self.frame, text="Book Details", font=("Helvetica", 20, "bold")).grid(row=0, column=0, columnspan=2)

        ctk.CTkLabel(self.frame, text="Book ID:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.id_label = ctk.CTkLabel(self.frame, text=self.book_id)
        self.id_label.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(self.frame, text="Title:").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.title_label = ctk.CTkLabel(self.frame, text=self.book_title)
        self.title_label.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(self.frame, text="Author:").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.author_label = ctk.CTkLabel(self.frame, text=self.book_author)
        self.author_label.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(self.frame, text="No. of Copies:").grid(row=4, column=0, sticky="e", padx=10, pady=5)
        self.copy_label = ctk.CTkLabel(self.frame, text=self.book_copies)
        self.copy_label.grid(row=4, column=1, padx=10, pady=5, sticky="w")
       
        ctk.CTkLabel(self.frame, text="RFID:").grid(row=5, column=0, sticky="e", padx=10, pady=5)
        self.rfid_label = ctk.CTkLabel(self.frame, text=self.book_rfid)
        self.rfid_label.grid(row=5, column=1, padx=10, pady=5, sticky="w")
 
        ctk.CTkLabel(self.frame, text="Cover Path:").grid(row=6, column=0, sticky="e", padx=10, pady=5)
        self.cover_label = ctk.CTkLabel(self.frame, text=self.book_cover)
        self.cover_label.grid(row=6, column=1, padx=10, pady=5, sticky="w")
       
        ctk.CTkLabel(self.frame, text="Status:").grid(row=7, column=0, sticky="e", padx=10, pady=(5, 30))
        self.status_label = ctk.CTkLabel(self.frame, text=self.book_status)
        self.status_label.grid(row=7, column=1, padx=10, pady=(5, 30), sticky="w")
        

        # Buttons
        self.buttons = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.buttons.grid(row=8, column=0, sticky="ne", columnspan=2)

        self.update_btn = ctk.CTkButton(self.buttons, text="Update", width=80, command=self.open_update_form)
        self.update_btn.grid(row=0, column=1, padx=10, pady=(5, 30))

        self.delete_btn = ctk.CTkButton(self.buttons, text="Delete", fg_color="brown", width=80, command=self.delete_book)
        self.delete_btn.grid(row=0, column=0, padx=10, pady=(5, 30))

        self.after(100, self.set_grab)

    def set_grab(self):
        self.grab_set()

    def open_update_form(self):
        def after_update():
            if self.on_update:
                self.on_update()
            self.destroy()

        # BookForm(self, self.book_data, on_update=after_update)
        BookForm(self, self.book_data, on_update=after_update)

    def delete_book(self):
        db = Database()
        confirm = ctk.CTkInputDialog(text=f"Type DELETE to confirm deletion of the book\n{self.book_title}.", title="Confirm Book Deletion")
        if confirm.get_input().strip().upper() == "DELETE":
            db.execute_query("DELETE FROM books WHERE book_id = %s", (self.book_id,))
            db.log_activity("Deleted", self.book_id, self.book_title)
            db.connection.commit()
            if self.on_update:
                self.on_update()
            self.destroy()
    
  