import customtkinter as ctk
from core.dashboard import Dashboard
from core.encryption import verify_user


class Login(ctk.CTkFrame):
    def __init__(self, parent, controller, fg_color=None):
        super().__init__(parent, fg_color="transparent")
        self.navigation = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.regular_font = ctk.CTkFont("Helvetica", 15, "normal")

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=0, sticky="nsew")

        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)
        self.container.grid_rowconfigure(0, weight=1)

        self.title_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.title_frame.grid(row=0, column=0, padx=(0,5), sticky="nsew")
        self.title_frame.grid_columnconfigure(0, weight=1)
        self.title_frame.grid_rowconfigure(0, weight=1)
        self.title_frame.grid_rowconfigure(1, weight=1)
        
        self.font_title = ctk.CTkFont("Courier New", 50, "bold")
        # self.font_subtitle = ctk.CTkFont("Courier New", 30, "italic")

        ctk.CTkLabel(self.title_frame, text="WELCOME TO", font=("Helvetica", 15, "normal")).grid(row=0, column=0, sticky="s")
        ctk.CTkLabel(self.title_frame, text="ORGANICER", font=self.font_title).grid(row=1, column=0, sticky="n")

        self.login_frame = ctk.CTkFrame(self.container)
        self.login_frame.grid(row=0, column=1, padx=(5,0), sticky="nsew")
        self.login_frame.grid_columnconfigure(0, weight=1)
        self.login_frame.grid_rowconfigure(0, weight=1)

        self.padding = ctk.CTkFrame(self.login_frame, fg_color="transparent")
        self.padding.grid(row=0, column=0, pady=10, padx=35, sticky="nsew")
        self.padding.grid_columnconfigure(0, weight=1)
        self.padding.grid_rowconfigure(0, weight=1)
        self.padding.grid_rowconfigure(1, weight=0)
        self.padding.grid_rowconfigure(2, weight=1)

        self.header = ctk.CTkFrame(self.padding, fg_color="transparent")
        self.header.grid(row=0, column=0, sticky="sew")
        ctk.CTkLabel(self.header, text="Sign In", font=("Helvetica", 30, "bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(self.header, text="Please sign in to your account", font=("Helvetica", 15, "italic"), text_color="gray").grid(row=1, column=0)

        self.form = ctk.CTkFrame(self.padding, fg_color="transparent")
        self.form.grid(row=1, column=0, pady=(20,5), sticky="ew")
        self.form.grid_columnconfigure(0, weight=1)

        self.username = ctk.CTkEntry(self.form, placeholder_text="Username", corner_radius=0, border_width=0, font=self.regular_font)
        self.username.grid(row=0, column=0, pady=(0,10), sticky="ew")
        self.username.bind("<Map>", self.search_field_focus)

        self.password = ctk.CTkEntry(self.form, placeholder_text="Password", corner_radius=0, border_width=0, show="*", font=self.regular_font) 
        self.password.grid(row=1, column=0, sticky="ew")


        self.footer = ctk.CTkFrame(self.padding, fg_color="transparent")
        self.footer.grid(row=2, column=0, pady=(20, 0), sticky="new")
        self.footer.grid_columnconfigure(0, weight=1)


        self.signin_btn = ctk.CTkButton(self.footer, text="Sign In", height=30, command=self.authentication)
        self.signin_btn.grid(row=0, column=0, sticky="ew")
        self.password.bind("<Return>", lambda e:self.authentication())

    def search_field_focus(self, event):
        self.username.focus_set()


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