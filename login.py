import customtkinter as ctk
from dashboard import Dashboard
from encryption import verify_user


class Login(ctk.CTkFrame):
    def __init__(self, parent, controller, fg_color=None):
        super().__init__(parent, fg_color="transparent")
        self.navigation = controller
        
        self.regular_font = ctk.CTkFont("Helvetica", 15, "normal")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=0)

        self.container.grid_columnconfigure(0, weight=1)
        

        self.header = ctk.CTkFrame(self.container, fg_color="transparent")
        self.header.grid(row=0, column=0, pady=(0, 20), sticky="ew")
        ctk.CTkLabel(self.header, text="Sign In", font=("Helvetica", 40, "bold")).grid(row=0, column=0)
        ctk.CTkLabel(self.header, text="Please sign in to your account", font=("Helvetica", 25, "italic"), text_color="gray").grid(row=1, column=0)

        self.form = ctk.CTkFrame(self.container, fg_color="transparent")
        self.form.grid(row=1, column=0, pady=(0, 20), sticky="ew")
        self.form.grid_columnconfigure(0, weight=1)

        self.username = ctk.CTkEntry(self.form, placeholder_text="Username", corner_radius=0, height=30, border_width=0, font=self.regular_font)
        self.username.grid(row=0, column=0, pady=(0,10), sticky="ew")

        self.password = ctk.CTkEntry(self.form, placeholder_text="Password", corner_radius=0, height=30, border_width=0, show="*", font=self.regular_font) 
        self.password.grid(row=1, column=0, sticky="ew")

        self.footer = ctk.CTkFrame(self.container, fg_color="transparent")
        self.footer.grid(row=2, column=0, sticky="ew")
        self.footer.grid_columnconfigure(0, weight=1)

        self.signin_btn = ctk.CTkButton(self.footer, text="Sign In", height=30, font=self.regular_font, command=self.authentication)
        self.signin_btn.grid(row=0, column=0, sticky="ew")
        self.password.bind("<Return>", lambda e:self.authentication())
    
    def authentication(self):
        username = self.username.get()
        password = self.password.get()

        if verify_user(username, password):
            # self.navigation.navigate_to("dashboard_page")
            self.container.grid_forget()
            self.dashboard_page = Dashboard(self)
            self.dashboard_page.grid(row=0, column=0, sticky="nsew")

            print("Access Granted")
        else:
            print("Access Denied")