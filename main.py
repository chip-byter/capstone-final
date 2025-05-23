import customtkinter as ctk
from core.login import Login

class Organicer(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Organicer")
        self.geometry("800x400")
        # self.attributes('-fullscreen', True)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.loginPage = Login(self, self)
        self.loginPage.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

if __name__ == "__main__":
    app = Organicer()
    app.mainloop()