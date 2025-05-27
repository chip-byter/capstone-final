import customtkinter as ctk
from PIL import Image, ImageTk

# ---------------------------------- CENTER WINDOW FUNCTION ----------------------------------------------
def center_window(frame, width:int, height:int):

        screen_width = frame.winfo_screenwidth()
        screen_height = frame.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        return frame.geometry(f"{width}x{height}+{x}+{y}")


# ---------------------------------- SEARCH BAR COMPONENT ----------------------------------------------
class SearchBar(ctk.CTkFrame):
    def __init__(self, parent, on_search=None, **kwargs):
        super().__init__(parent)
        self.on_search = on_search

        self.search_field = ctk.CTkEntry(self, width=300)
        self.search_field.grid(row=0, column=0, padx=5, pady=5, sticky="new")
        self.search_field.bind("<Map>", self.search_field_focus)
        # self.search_field.bind("<Return>", lambda event: controller.show_frame("Books Page"))

        self.search_btn = ctk.CTkButton(self, text="Search", command=self._search, width=80)
        self.search_btn.grid(row=0, column=1, padx=5, pady=5, sticky="nw")

        self.search_field.bind("<Return>", lambda e: self._search())

    def _search(self):
        query = self.search_field.get().strip()
        if query:
            self.on_search(query)

    def search_field_focus(self, event):
        self.search_field.focus_set()


# ---------------------------------- BOOK CARD COMPONENT ----------------------------------------------
class BookCard(ctk.CTkFrame):
    def __init__(self, parent, book_data, on_click=None):
        super().__init__(parent, corner_radius=10, border_width=1)
        self.book_data = book_data
        self.on_click = on_click
        self.default_image_path = "assets/book_covers/default_cover.png"
        
        book_title = book_data['book_title']
        book_author = book_data['book_author']
        book_cover = book_data['cover']
        book_copies = book_data['copy']

        # Load book cover image
        try:
            # img = Image.open(book_data[4]).resize((60, 80))
            img = ctk.CTkImage(dark_image=Image.open(book_cover), size=(125,177))
        except FileNotFoundError:
            img = ctk.CTkImage(dark_image=Image.open(self.default_image_path), size=(125,177))
            

        self.cover_label = ctk.CTkLabel(self, image=img, text="")
        self.cover_label.grid(row=1, column=0, padx=10, pady=(0, 10))

        # Book info
        self.book_metadata = ctk.CTkFrame(self, fg_color="transparent")
        self.book_metadata.grid(row=2, column=0, pady=(0,10), padx=10, sticky="new")
        self.book_metadata.grid_rowconfigure(0, weight=1)
        self.book_metadata.grid_columnconfigure(0, weight=1)


        self.text_title = self.truncate_text(book_title, 20)
        self.book_title = ctk.CTkLabel(self.book_metadata, text=self.text_title, font=("Helvetica", 14, "bold"), wraplength=130)
        self.book_title.grid(row=0, column=0)

        self.text_author = self.truncate_text(book_author, 20)
        self.book_author = ctk.CTkLabel(self.book_metadata, text=self.text_author, font=("Helvetica", 12, 'italic'), wraplength=120)
        self.book_author.grid(row=1, column=0)

        self.copy_num = ctk.CTkLabel(self, text=f"Copies: {book_copies}", bg_color="transparent", font=("helvetica", 12, "bold"), corner_radius=10)
        self.copy_num.grid(row=0, column=0, padx=5, pady=(5,0), sticky="ew")

        self.bind_all_widgets("<Button-1>", lambda e: on_click(book_data) if on_click else None)

    def bind_all_widgets(self, event, callback):
        self.bind(event, callback)
        for widget in self.winfo_children():
            widget.bind(event, callback)

    def truncate_text(self, text, max_chars):
        return text if len(text) <= max_chars else text[:max_chars - 3] + "..."


# ---------------------------------- BOOK GRID COMPONENT ----------------------------------------------
class BookGrid(ctk.CTkScrollableFrame):
    def __init__(self, parent, books, on_card_click):
        super().__init__(parent)
        self.display_books(books, on_card_click)

    def display_books(self, books, on_card_click):
        try:
            for i, book in enumerate(books):
                card = BookCard(self, book, on_click=on_card_click)
                card.grid(row=i // 4, column=i % 4, padx=10, pady=10)
        except TypeError as e:
            print(e)
            return
# ---------------------------------- MESSAGEBOX COMPONENT ----------------------------------------------
class MessageBox(ctk.CTkToplevel):
    def __init__(self, parent, title="Info", message="", on_close=None):
        super().__init__(parent)
        self.title(title)
        # self.geometry("300x150")
        center_window(self, 300, 150)
        self.resizable(False, False)
        # self.grab_set()

        self.label = ctk.CTkLabel(self, text=message, wraplength=280)
        self.label.pack(pady=20, padx=20)

        self.ok_btn = ctk.CTkButton(self, text="OK", command=self.close)
        self.ok_btn.pack(pady=(0, 10))

        self.on_close = on_close
        self.after(100, self.set_grab)

    def set_grab(self):
        self.grab_set()

    def close(self):
        if self.on_close:
            self.on_close()
        self.destroy()

# ---------------------------------- CONFIRMDIALOG COMPONENT ----------------------------------------------
class ConfirmationDialog(ctk.CTkToplevel):
    def __init__(self, parent, message, on_confirm, on_cancel=None):
        super().__init__(parent)
        self.title("Confirmation")
        center_window(self, 300, 150)
        # self.grab_set()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.label = ctk.CTkLabel(self, text=message, wraplength=250)
        self.label.grid(row=0, column=0, pady=20)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=1, column=0, pady=10)

        self.confirm_btn = ctk.CTkButton(btn_frame, text="Yes", width=100, command=lambda: self._confirm(on_confirm))
        self.confirm_btn.grid(row=0, column=1, padx=10)

        self.cancel_btn = ctk.CTkButton(btn_frame, text="No", width=100, command=lambda: self._cancel(on_cancel))
        self.cancel_btn.grid(row=0, column=0)

        self.after(100, self.set_grab)

    def set_grab(self):
        self.grab_set()

    def _confirm(self, callback):
        if callback:
            callback()
        self.destroy()

    def _cancel(self, callback):
        if callback:
            callback()
        self.destroy()