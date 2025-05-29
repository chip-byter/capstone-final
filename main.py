import time
import threading
import customtkinter as ctk
from core.widgets import center_window
from core.dashboard import Dashboard
from core.login import Login
from dash.transactions import Transactions

class Organicer(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Organicer")
        self.geometry("800x400")
        center_window(self, 800, 400)
        # self.attributes('-fullscreen', True)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.loginPage = Login(self, self)
        self.loginPage.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.overdue_checker()
        self.dashboardPage = None  

    def show_login(self):
        if self.dashboardPage:
            self.dashboardPage.destroy()
            self.dashboardPage = None
        self.loginPage = Login(self, self)
        self.loginPage.grid(row=0, column=0, sticky="nsew")

    def show_dashboard(self):
        self.loginPage.destroy()
        self.dashboardPage = Dashboard(self, self)
        self.dashboardPage.grid(row=0, column=0, sticky="nsew")

    def overdue_checker(self, interval_seconds=3600):  # 86400 = 24 hours
        def loop():
            while True:
                Transactions.handle_overdue_books()
                time.sleep(interval_seconds)
        
        threading.Thread(target=loop, daemon=True).start()

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    app = Organicer()
    app.mainloop()