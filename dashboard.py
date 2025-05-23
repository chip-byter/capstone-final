import customtkinter as ctk
from navigate import NavigationController
from urls import register_routes

class Dashboard(ctk.CTkFrame):
    def __init__(self, parent, fg_color=None):
        super().__init__(parent, fg_color="transparent")
        self.regular_font = ctk.CTkFont("Helvetica", 15, "normal")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.body_container = ctk.CTkFrame(self)
        self.body_container.grid(row=1, column=0, pady=10, sticky="nsew")
        
        self.navigator = NavigationController(self.body_container)
        register_routes(self.navigator)

        self.buttons_container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.buttons_container.grid(row=0, column=0, pady=(10, 0), sticky="ew")

        self.buttons_container.grid_columnconfigure(0, weight=1)
        self.buttons_container.grid_columnconfigure(1, weight=1)
        self.buttons_container.grid_columnconfigure(2, weight=1)
        self.buttons_container.grid_columnconfigure(3, weight=1)
        self.buttons_container.grid_columnconfigure(4, weight=1)

        self.overview_btn = ctk.CTkButton(
            self.buttons_container, 
            text="Overview", 
            fg_color="transparent",
            command=lambda: self.switch("overview_page", self.overview_btn))
        self.overview_btn.grid(row=0, column=0, sticky="ew")

        self.books_btn = ctk.CTkButton(
            self.buttons_container, 
            text="Manage Books", 
            fg_color="transparent",
            command=lambda: self.switch("inventory_page", self.books_btn))
        self.books_btn.grid(row=0, column=1, sticky="ew")

        self.transactions_btn = ctk.CTkButton(
            self.buttons_container, 
            text="Transactions", 
            fg_color="transparent",
            command=lambda: self.switch("transactions_page", self.transactions_btn))
        self.transactions_btn.grid(row=0, column=2, sticky="ew")

        self.activity_btn = ctk.CTkButton(
            self.buttons_container, 
            text="Activity Log", 
            fg_color="transparent",
            command=lambda: self.switch("activity_page", self.activity_btn))
        self.activity_btn.grid(row=0, column=3, sticky="ew")

        self.reports_btn = ctk.CTkButton(
            self.buttons_container, 
            text="Reports", 
            fg_color="transparent",
            command=lambda: self.switch("reports_page", self.reports_btn))
        self.reports_btn.grid(row=0, column=4, sticky="ew")

        self.navigator.navigate_to("overview_page")
        self.overview_btn.configure(fg_color="#1F6AA5")

    def switch(self, page_name, actv_btn):
        for each_widget in self.buttons_container.winfo_children():
            if isinstance(each_widget, ctk.CTkButton):
                each_widget.configure(fg_color="transparent")

        actv_btn.configure(fg_color="#1F6AA5")
        self.navigator.navigate_to(page_name)
        

    

if __name__ == "__main__":
    root = ctk.CTk()
    
    root.geometry("800x400")

    loginPage = Dashboard(root)
    loginPage.pack(expand=True, fill="both")
    root.mainloop()


