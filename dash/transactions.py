import customtkinter as ctk
from dash.results_frame import ResultsFrame
from core.database import Database
from core.widgets import BookGrid, SearchBar



class Transactions(ctk.CTkFrame):
    def __init__(self, parent, controller, fg_color=None):
        super().__init__(parent, fg_color="transparent")
        self.navigation = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_view = ctk.CTkFrame(self, fg_color="transparent")
        self.main_view.grid(row=0, column=0, sticky="nsew")
        
        self.main_view.grid_columnconfigure(0, weight=1)
        self.main_view.grid_rowconfigure(0, weight=1)
        self.main_view.grid_rowconfigure(1, weight=0)
        self.main_view.grid_rowconfigure(2, weight=1)

        self.app_name = ctk.CTkLabel(self.main_view, text="ORGANICER", font=("Courier New", 80, "bold"))
        self.app_name.grid(row=0, column=0, sticky="s")

        self.search = SearchBar(self.main_view, on_search=self.show_results_frame)
        self.search.grid(row=1, column=0, pady=(5, 0))

        self.buttons = ctk.CTkFrame(self.main_view, fg_color="transparent")
        self.buttons.grid(row=2, column=0, pady=10, sticky="n")
        self.lend_btn = ctk.CTkButton(self.buttons, text="Lend a Book")
        self.return_btn = ctk.CTkButton(self.buttons, text="Return a Book")
        self.lend_btn.grid(row=0, column=0, padx=5)
        self.return_btn.grid(row=0, column=1, padx=5)

        self.results_frame = ResultsFrame(self, on_back=self.show_main_view)
        self.results_frame.grid(row=0, column=0, sticky="nsew")
        self.results_frame.lower()
        
    def show_results_frame(self, query):
        self.main_view.lower()
        self.results_frame.search_books(query)
        self.results_frame.lift()

    def show_main_view(self):
        self.search.search_field.delete(0, ctk.END)
        self.results_frame.lower()
        self.main_view.lift()
    
         
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("800x400")
    loginPage = Transactions(root, root)
    loginPage.pack(expand=True, fill="both")
    root.mainloop()