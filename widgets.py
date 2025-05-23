import customtkinter as ctk
from PIL import Image, ImageTk

# ---------------------------------- SEARCH BAR COMPONENT ----------------------------------------------
class SearchBar(ctk.CTkFrame):
    def __init__(self, parent, on_search=None):
        super().__init__(parent)

        self.search_field = ctk.CTkEntry(self, width=300)
        self.search_field.grid(row=0, column=0, padx=5, pady=5, sticky="new")
        self.search_field.bind("<Map>", self.search_field_focus)
        # self.search_field.bind("<Return>", lambda event: controller.show_frame("Books Page"))

        self.search_btn = ctk.CTkButton(self, text="Search")
        self.search_btn.grid(row=0, column=1, padx=5, pady=5, sticky="nw")

        self.on_search = on_search
        self.search_field.bind("<Return>", lambda e: self._search())

    def _search(self):
        query = self.search_field.get().strip()
        if self.on_search:
            self.on_search(query)

    def search_field_focus(self, event):
        self.search_field.focus_set()


# ---------------------------------- BOOK CARD COMPONENT ----------------------------------------------
class BookCard(ctk.CTkFrame):
    def __init__(self, parent, book_data, on_click=None):
        super().__init__(parent, corner_radius=10, border_width=1)
        self.book_data = book_data
        self.on_click = on_click

        # Load book cover image
        img = Image.open(book_data["cover_path"]).resize((60, 80))
        self.cover_img = ImageTk.PhotoImage(img)
        self.cover_label = ctk.CTkLabel(self, image=self.cover_img, text="")
        self.cover_label.grid(row=0, column=0, rowspan=3, padx=10, pady=10)

        # Book info
        self.title_label = ctk.CTkLabel(self, text=book_data["title"], font=("Arial", 14, "bold"))
        self.title_label.grid(row=0, column=1, sticky="w")

        self.author_label = ctk.CTkLabel(self, text=f"by {book_data['author']}", font=("Arial", 12))
        self.author_label.grid(row=1, column=1, sticky="w")

        self.avail_label = ctk.CTkLabel(self, text=f"Available: {book_data['available']}/{book_data['copies']}")
        self.avail_label.grid(row=2, column=1, sticky="w")

        self.bind_all_widgets("<Button-1>", lambda e: on_click(book_data) if on_click else None)

    def bind_all_widgets(self, event, callback):
        self.bind(event, callback)
        for widget in self.winfo_children():
            widget.bind(event, callback)
