import customtkinter as ctk
from core.widgets import center_window


class UserDetails(ctk.CTkToplevel):
    def __init__(self, parent, on_submit=None,):
        super().__init__(parent)
        self.title("User Details")
        center_window(self, 350, 250)
        # self.grab_set()
        self.on_submit = on_submit

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

        ctk.CTkLabel(self.frame, text="User Form", font=("Helvetica", 20, "bold")).grid(row=0, column=0, columnspan=2)

        ctk.CTkLabel(self.frame, text="User ID:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.user_id = ctk.CTkEntry(self.frame, placeholder_text="User ID")
        self.user_id.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(self.frame, text="User Name:").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.user_name = ctk.CTkEntry(self.frame, placeholder_text="Username")
        self.user_name.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(self.frame, text="User Email:").grid(row=3, column=0, sticky="e", padx=10, pady=(5,30))
        self.user_email = ctk.CTkEntry(self.frame, placeholder_text="username@gmail.com")
        self.user_email.grid(row=3, column=1, padx=10, pady=(5, 30), sticky="ew")

        self.buttons = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons.grid(row=1, column=0, padx=10, pady=10, sticky="ne")

        self.submit_btn = ctk.CTkButton(self.buttons, text="Confirm", width=80, command=self.submit)
        self.submit_btn.grid(row=0, column=0)
        self.after(100, self.set_grab)

    def set_grab(self):
        self.grab_set()
        
    def get_user_details(self):
        return {
        "id": self.user_id.get(),
        "name": self.user_name.get(),
        "email": self.user_email.get()
    }

    def submit(self):
        if self.on_submit:
            self.on_submit(self.get_user_details()) 
        self.destroy()
