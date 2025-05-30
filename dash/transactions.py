import customtkinter as ctk
from dash.results_frame import ResultsFrame
from core.database import Database
import core.emailsys
from core.widgets import BookGrid, SearchBar
from dash.scanbook import ScanBookFrame
from dash.userform import UserDetails



class Transactions(ctk.CTkFrame):
    def __init__(self, parent, controller, fg_color=None):
        super().__init__(parent, fg_color="transparent")
        
        self.navigation = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.db = Database()
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

        self.lend_btn = ctk.CTkButton(self.buttons, text="Lend a Book", command=self.show_userform)
        self.return_btn = ctk.CTkButton(self.buttons, text="Return a Book", command=self.show_userform)
        self.lend_btn.grid(row=0, column=0, padx=5)
        self.return_btn.grid(row=0, column=1, padx=5)

        self.results_frame = ResultsFrame(self, on_back=self.show_main_view)
        self.results_frame.grid(row=0, column=0, sticky="nsew")
        self.results_frame.lower()

        self.scan_frame = ScanBookFrame(self, controller=self, db=self.db)
        self.scan_frame.grid(row=0, column=0, sticky="nsew")
        self.scan_frame.lower()
    
    def show_results_frame(self, query):
        self.main_view.lower()
        self.results_frame.search_books(query)
        self.results_frame.lift()

    def show_main_view(self):
        self.search.search_field.delete(0, ctk.END)
        self.results_frame.lower()
        self.main_view.lift()

    def show_userform(self):
        UserDetails(self, on_submit=self.send_user_info)

    def send_user_info(self, user):
        self.user_info = user
        self.scan_frame.set_user(user)
        self.show_scan_frame()
    
    def show_scan_frame(self):
        self.main_view.lower()
        self.results_frame.lower()
        self.scan_frame.lift()
    
    def handle_overdue_books():
        db = Database()

        overdues = db.get_overdue_books()

        for book in overdues:
            
            rfid = book["rfid"]
            book_title = book["book_title"]
            user_name = book["user_name"]
            user_email = book["user_email"]
            formatted_due = book["due_date"].strftime("%B %d, %Y")

            db.log_activity("Overdue", rfid, book_title)

            subject = f"Overdue Book: {book_title}"
            body_text = f"Hello {user_name}, \n This is a reminder that the following book you've borrowed <b>'{book_title}'</b> on <b>{formatted_due}<b> is overdue. \n\n Please return it as soon as possible to avoid penalties."

            body_html = core.emailsys.generate_email_template(user_name, book_title, body_text)
            core.emailsys.send_notification_email(user_email, subject, body_text, body_html)
            
        
        print(f"Checked and sent emails for {len(overdues)} overdue book(s).")
            
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("800x400")
    loginPage = Transactions(root, root)
    loginPage.pack(expand=True, fill="both")
    root.mainloop()