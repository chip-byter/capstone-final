import customtkinter as ctk
from dash.book_details import BookDetailsWindow
from dash.bookform import BookForm
from core.database import Database
from core.widgets import SearchBar, BookGrid
from core.encryption import verify_user

class Inventory(ctk.CTkFrame):
    def __init__(self, parent, controller, fg_color=None):
        super().__init__(parent, fg_color="transparent")
        self.navigation = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.transactions = ctk.CTkFrame(self, fg_color="transparent")
        self.transactions.grid(row=0, column=0, sticky="n")
        self.transactions.grid_columnconfigure(0, weight=0)

        self.search = SearchBar(self.transactions, on_search=self.search_books)
        self.search.grid(row=0, column=0)    

        self.load_and_display_books()
        
        self.add_btn = ctk.CTkButton(self.transactions, text="Add", width=80, command=self.open_book_form)
        self.add_btn.grid(row=0, column=1)

    def open_book_form(self):
        BookForm(self, on_update=self.refresh_books)

    def load_and_display_books(self, query=None):
        db = Database()
        # all_books = fetch_all_books()
        all_books = db.fetch_all("SELECT * FROM books")

        if query:
            all_books = db.fetch_all("SELECT * FROM books WHERE book_title LIKE %s OR book_author LIKE %s", (f"%{query}%", f"%{query}%"))
        
        if hasattr(self, 'grid_frame'):
            self.grid_frame.destroy()

        if not all_books:
            self.msg_container = ctk.CTkFrame(self)
            self.msg_container.grid(row=1, column=0, pady=10)
            self.no_result_label = ctk.CTkLabel(
                self.msg_container, 
                text=f"Sorry, there's no result for '{query}'.", 
                font=("Helvetica", 20, "bold"))
            self.no_result_label.grid(row=0, column=0, sticky="sew")
            self.no_result_sublabel = ctk.CTkLabel(
                self.msg_container, 
                text="Please check your spelling or enter a specific book title or author.", 
                font=("Helvetica", 13, "italic"))
            self.no_result_sublabel.grid(row=1, column=0, sticky="new")
            
        else: 
            if hasattr(self, "msg_container"):
                self.msg_container.destroy()

            self.grid_frame = BookGrid(self, books=all_books, on_card_click=self.on_book_click)
            self.grid_frame.grid(row=1, column=0, pady=10, sticky="nsew") 
            self.grid_frame.grid_columnconfigure(0, weight=0)   
            self.grid_frame.grid_columnconfigure(2, weight=0)   
            self.grid_frame.grid_columnconfigure(3, weight=0)   
            self.grid_frame.grid_columnconfigure(4, weight=0)   

    # def show_book_details(self, book_data):
    #     # MAKE THIS TOPLEVEL WINDOW
    #     print(f"Selected Book: {book_data[1]}\nAuthor: {book_data[2]}\nCopies: {book_data[3]}")

    def search_books(self, query):
        self.load_and_display_books(query)

    def get_books(self):
        db = Database()
        return db.fetch_all("SELECT * FROM books")

    def on_book_click(self, book_data):
        # Open the details toplevel window
        BookDetailsWindow(self, book_data, on_update=self.refresh_books)

    def refresh_books(self):
        # Re-fetch and refresh the book grid
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        self.grid_frame.destroy()

        self.grid_frame = BookGrid(self, books=self.get_books(), on_card_click=self.on_book_click)
        self.grid_frame.grid(row=1, column=0, pady=10, sticky="nsew")