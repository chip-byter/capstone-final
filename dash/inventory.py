import customtkinter as ctk
from dash.book_details import BookDetailsWindow
from dash.newbookform import BookForm
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

        
        self.add_btn = ctk.CTkButton(self.transactions, text="Add", width=80, command=self.open_book_form)
        self.add_btn.grid(row=0, column=1)

        self.results_area = ctk.CTkFrame(self, fg_color="transparent")
        self.results_area.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        self.load_and_display_books()

    def open_book_form(self):
        BookForm(self, on_update=self.refresh_books)

    def load_and_display_books(self, query=None):
        db = Database()
        # all_books = fetch_all_books()
        all_books = db.fetch_all("SELECT * FROM books")

        if query:
            all_books = db.fetch_all("SELECT * FROM books WHERE book_title LIKE %s OR book_author LIKE %s", (f"%{query}%", f"%{query}%"))
        
        for widget in self.results_area.winfo_children():
            widget.destroy()

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
                self.no_result_label.destroy()
                self.no_result_sublabel.destroy()

            if hasattr(self, "book_grid"):
                self.book_grid.destroy()

            self.book_grid = BookGrid(self.results_area, books=all_books, on_card_click=self.on_book_click)
            self.book_grid.pack(fill="both", expand=True)

    def search_books(self, query):
        self.load_and_display_books(query)

    def get_books(self):
        db = Database()
        return db.fetch_all("SELECT * FROM books")

    def on_book_click(self, book_data):
        BookDetailsWindow(self, book_data, on_update=self.refresh_books)

    def refresh_books(self):
        for widget in self.book_grid.winfo_children():
            widget.destroy()
        self.book_grid.destroy()

        self.book_grid = BookGrid(self, books=self.get_books(), on_card_click=self.on_book_click)
        self.book_grid.grid(row=1, column=0, pady=10, sticky="nsew")