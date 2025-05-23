import customtkinter as ctk
from widgets import SearchBar
# from encryption import verify_user


class Transactions(ctk.CTkFrame):
    def __init__(self, parent, controller, fg_color=None):
        super().__init__(parent, fg_color="transparent")
        self.navigation = controller
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)

        self.app_name = ctk.CTkLabel(self, text="ORGANICER", font=("Courier New", 80, "bold"))
        self.app_name.grid(row=1, column=0, columnspan=2, sticky="s")
        
        self.transactions = ctk.CTkFrame(self, fg_color="transparent")
        self.transactions.grid(row=2, column=0, sticky="n")
        self.transactions.grid_columnconfigure(0, weight=0)

        self.search = SearchBar(self.transactions)
        self.search.grid(row=0, column=0)    

        # self.search_field = ctk.CTkEntry(self.transactions, width=300)
        # self.search_field.grid(row=0, column=0, padx=5, pady=5, sticky="new")
        # # self.search_field.bind("<Map>", self.search_field_focus)
        # # self.search_field.bind("<Return>", lambda event: controller.show_frame("Books Page"))

        # self.search_btn = ctk.CTkButton(self.transactions, text="Search")
        # self.search_btn.grid(row=0, column=1, padx=5, pady=5, sticky="nw")

        self.buttons = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons.grid(row=3, column=0, pady=10, sticky="n")
        
        self.lend_btn = ctk.CTkButton(self.buttons, text="Lend a Book")
        self.lend_btn.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.return_btn = ctk.CTkButton(self.buttons, text="Return a Book")
        self.return_btn.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("800x400")
    loginPage = Transactions(root, root)
    loginPage.pack(expand=True, fill="both")
    root.mainloop()