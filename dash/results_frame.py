import customtkinter as ctk

from core.database import Database
from core.widgets import BookGrid, SearchBar

class ResultsFrame(ctk.CTkFrame):
    def __init__(self, parent, on_back, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_back = on_back

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.top_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.top_bar.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.top_bar.grid_columnconfigure(0, weight=1)
        self.top_bar.grid_columnconfigure(1, weight=1)

        self.back_btn = ctk.CTkButton(self.top_bar, text="← Back", command=self.on_back, width=80)
        self.back_btn.grid(row=0, column=1, sticky="e", padx=(0, 10))

        self.searchbar = SearchBar(self.top_bar, on_search=self.search_books)
        self.searchbar.grid(row=0, column=0, sticky="e")

        self.results_area = ctk.CTkFrame(self, fg_color="transparent")
        self.results_area.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

    def search_books(self, query):
        self.searchbar.search_field.delete(0, ctk.END)
        self.searchbar.search_field.insert(0, query)

        db = Database()
        books = db.fetch_all("SELECT * FROM books WHERE book_title LIKE %s OR book_author LIKE %s",
                             (f"%{query}%", f"%{query}%"))

        # Clear previous results
        for widget in self.results_area.winfo_children():
            widget.destroy()

        if not books:
            self.msg_container = ctk.CTkFrame(self, fg_color="transparent")
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

            book_grid = BookGrid(self.results_area, books=books, on_card_click=self.show_book_details)
            book_grid.pack(fill="both", expand=True)

    def show_book_details(self, book_data):
        # Optional: implement a popup or side panel
        pass