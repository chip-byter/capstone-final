import customtkinter as ctk
from widgets import SearchBar
from encryption import verify_user


class Inventory(ctk.CTkFrame):
    def __init__(self, parent, controller, fg_color=None):
        super().__init__(parent, fg_color="transparent")
        self.navigation = controller
        
        self.transactions = ctk.CTkFrame(self, fg_color="transparent")
        self.transactions.grid(row=0, column=0, sticky="n")
        self.transactions.grid_columnconfigure(0, weight=0)

        self.search = SearchBar(self.transactions)
        self.search.grid(row=0, column=0)    