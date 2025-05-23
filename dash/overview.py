import customtkinter as ctk



class Overview(ctk.CTkFrame):
    def __init__(self, parent, controller, fg_color=None):
        super().__init__(parent, fg_color="transparent")
        self.navigation = controller
        
        ctk.CTkLabel(self, text="Hello, OVERVIEW").pack()