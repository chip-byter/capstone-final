# components/book_grid.py
import customtkinter as ctk
from widgets import BookCard

class BookGrid(ctk.CTkScrollableFrame):
    def __init__(self, parent, books, on_card_click):
        super().__init__(parent)
        self.display_books(books, on_card_click)

    def display_books(self, books, on_card_click):
        for idx, book in enumerate(books):
            card = BookCard(self, book, on_click=on_card_click)
            card.grid(row=idx // 3, column=idx % 3, padx=10, pady=10, sticky="nsew")
