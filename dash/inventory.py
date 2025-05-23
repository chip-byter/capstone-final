import customtkinter as ctk

from encryption import verify_user


class Inventory(ctk.CTkFrame):
    def __init__(self, parent, controller, fg_color=None):
        super().__init__(parent, fg_color="transparent")
        self.navigation = controller
        
        ctk.CTkLabel(self, text="Hello, INVENTORY!").pack()