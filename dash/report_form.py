import customtkinter as ctk
from core.widgets import center_window, MessageBox
# from core.widgets import center_window


class ReportForm(ctk.CTkToplevel):
    def __init__(self, parent, on_submit=None,):
        super().__init__(parent)
        self.title("User Details")
        center_window(self, 350, 150)
        # self.grab_set()
        self.on_submit = on_submit

        self.grid_columnconfigure(0, weight=1)
        # self.grid_rowconfigure(0, weight=1)

        self.frame = ctk.CTkFrame(self)
        self.frame.grid(row=0, column=0, sticky="nsew")
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

        ctk.CTkLabel(self.frame, text="Report Form", font=("Helvetica", 20, "bold")).grid(row=0, column=0, columnspan=2)

        ctk.CTkLabel(self.frame, text="Email Recepient").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.recipient_email = ctk.CTkEntry(self.frame, placeholder_text="user.name@gmail.com")
        self.recipient_email.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkLabel(self.frame, text="File Name:").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.filename = ctk.CTkEntry(self.frame, placeholder_text="report_yyyy-mm-dd.xlsx")
        self.filename.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.buttons = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons.grid(row=1, column=0, padx=10, pady=10, sticky="ne")

        self.submit_btn = ctk.CTkButton(self.buttons, text="Send", width=80, command=self.send)
        self.submit_btn.grid(row=0, column=0)

        self.after(100, self.set_grab)

    def set_grab(self):
        self.grab_set()
        
    

    def send(self):
        recipient = self.recipient_email.get().strip()
        filename = self.filename.get().strip() or None

        if self.on_submit:
            self.on_submit(recipient, filename) 
        self.destroy()


    # def submit(self):
    #     if self.on_submit:
    #         self.on_submit(self.get_form_entries()) 
    #     self.destroy()

if __name__ == "__main__":
    root = ctk.CTk()
    

    root.mainloop()
    