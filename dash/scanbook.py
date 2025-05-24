import customtkinter as ctk
import core.emailsys
from core.widgets import MessageBox

class ScanBookFrame(ctk.CTkFrame):
    def __init__(self, parent, controller=None, db=None):
        super().__init__(parent)
        self.controller = controller
        self.db = db
        self.user = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.label_heading = ctk.CTkLabel(self, text=" ", font=("Helvetica", 20, "bold"))
        self.label_heading.grid(row=0, column=0, columnspan=2, sticky="s")
        self.label_subheading = ctk.CTkLabel(self, text=" ", font=("Helvetica", 13, "italic"))
        self.label_subheading.grid(row=1, column=0, sticky="n")

        self.rfid_buffer = ""
        self.reading_rfid = False

    def set_user(self, user_data):
        self.user = user_data
        self.label_subheading.configure(text=f"User: {self.user['name']} \n (ID: {self.user['id']})")
        self.label_heading.configure(text="Please scan the book RFID...")
        self.start_rfid_listener()

    def start_rfid_listener(self):
        self.label_heading.configure(text="Scanning...")
        self.rfid_buffer = ""
        self.reading_rfid = True
        self.focus_set()
        self.winfo_toplevel().focus_force()
        self.winfo_toplevel().bind_all("<Key>", self.capture_rfid)

    def capture_rfid(self, event):
        if isinstance(event.widget, ctk.CTkEntry):
            return
        if not self.reading_rfid:
            return

        if event.keysym in ("Return", "Tab"):
            self.reading_rfid = False
            rfid_tag = self.rfid_buffer.strip()
            self.rfid_buffer = ""
            self.process_rfid(rfid_tag)
            return "break"
        else:
            self.rfid_buffer += event.char

    def submit_book(self):
        book_id = self.book_entry.get()
        if book_id:
            self.process_rfid(book_id)

    def cancel(self):
        self.winfo_toplevel().unbind_all("<Key>")
        self.controller.show_main_view()

    def process_rfid(self, rfid_tag):
        try:
            book = self.db.get_book_by_rfid(rfid_tag)

            if not book:
                self.display_error(f"No book found for RFID: {rfid_tag}")
                self.start_rfid_listener()
                return

            book_id = book["book_id"]
            book_title = book["book_title"] 
            self.label_heading.configure(text="Successful!")
            self.label_subheading.configure(text=f"Scanned RFID: {rfid_tag}\nBook Title: {book_title}")

            self.process_transaction(book_id, book_title)
            self.winfo_toplevel().unbind_all("<Key>")

        except Exception as e:
            self.display_error(str(e))
            self.start_rfid_listener()

    def process_transaction(self, book_id, book_title):
        if not self.user:
            self.display_error("User not set.")
            return

        user_id = self.user['id']
        user_name = self.user['name']
        user_email = self.user['email']

        status = self.db.get_book_status(book_id, user_id)
        if status is None:
            self.display_error("Failed to retrieve book status.")
            self.start_rfid_listener()
            return

        if status in ["Borrowed", "Overdue"]:
            self.return_book_flow(user_id, book_id, book_title, user_name, user_email)
        else:
            self.borrow_book_flow(user_id, book_id, book_title, user_name, user_email)

    def return_book_flow(self, user_id, book_id, book_title, user_name, user_email):
        self.db.return_book(user_id, book_id)

        self.db.log_activity("Returned", book_id, book_title, user_id, user_name)
        title="Returning"
        message = f"{user_name} returned book {book_title}"

        subject = f"You returned: {book_title}"
        body_text = f"Hello {user_name},\n\nYou've returned '{book_title}'."
        body_html = core.emailsys.generate_email_template(user_name, book_title, "You've successfully returned this book. <strong>Thank You!</strong>.")
        self.send_email(user_email, subject, body_text, body_html)
        
        self.show_confirmation(title, message)

    def borrow_book_flow(self, user_id, book_id, book_title, user_name, user_email):
        due_date = self.db.borrow_book(user_id, user_name, user_email, book_id)
        if not due_date:
            self.display_error("Failed to borrow the book.")
            self.start_rfid_listener()
            return
        
        self.db.log_activity("Borrowed", book_id, book_title, user_id, user_name)
        
        formatted_due = due_date.strftime("%B %d, %Y")
        title = "Lending"
        message = f"{user_name} borrowed the book \n{book_title}"

        subject = f"You borrowed: {book_title}"
        body_text = f"Hello {user_name},\n\nYou've borrowed '{book_title}'. Return it by {formatted_due}."
        body_html = core.emailsys.generate_email_template(user_name, book_title, f"You've borrowed this book. Return it by <em><strong>{formatted_due}</strong></em>.")
        self.send_email(user_email, subject, body_text, body_html)

        self.show_confirmation(title, message)

    def display_error(self, message):
        self.reading_rfid = False
        MessageBox(self, "Error", message, on_close=self.start_rfid_listener)

        
    def send_email(self, to, subject, text, html):
        try:
            core.emailsys.send_notification_email(to, subject, text, html)
        except Exception as e:
            print("Failed to send email:", e)

    def show_confirmation(self, title, message):
        MessageBox(self, title, message, on_close=lambda: self.controller.show_main_view())
        
