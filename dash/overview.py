from datetime import datetime
import customtkinter as ctk
from core.database import Database

class Overview(ctk.CTkFrame):
    def __init__(self, parent, controller, fg_color=None):
        super().__init__(parent, fg_color="transparent")
        self.navigation = controller
        self.db = Database()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.body_container = ctk.CTkFrame(self, fg_color="transparent")
        self.body_container.grid(row=1, column=0, sticky="nsew")
        self.body_container.grid_columnconfigure(0, weight=1)
        self.body_container.grid_rowconfigure(0, weight=1)
        self.body_container.grid_rowconfigure(1, weight=1)
        
        self.summary_frame = ctk.CTkFrame(self.body_container, fg_color="transparent")
        self.summary_frame.grid(row=0, column=0, sticky="nsew", pady=5)
        self.summary_frame.grid_rowconfigure(0, weight=1)
        self.summary_frame.grid_columnconfigure(0, weight=1)
        self.summary_frame.grid_columnconfigure(1, weight=1)
        self.summary_frame.grid_columnconfigure(2, weight=1)
        self.summary_frame.grid_columnconfigure(3, weight=1)
        self.summary_frame.grid_columnconfigure(4, weight=1)

        self.create_summary_container("Total Books", 0, self.total_bks())
        self.create_summary_container("Available Books", 1, self.total_available())
        self.create_summary_container("Borrowed Books", 2, self.total_borrowed())
        self.create_summary_container("Overdue Books", 3, self.total_due())
        self.create_summary_container("Lost & Damaged Books", 4, self.total_lost_damaged())

        self.notif_frame = ctk.CTkFrame(self.body_container, fg_color="transparent")
        self.notif_frame.grid(row=1, column=0, pady=(5,10), padx=10, sticky="nsew")

        self.notif_frame.grid_columnconfigure(0, weight=1)
        self.notif_frame.grid_columnconfigure(1, weight=1)
        self.notif_frame.grid_rowconfigure(0, weight=1)

        self.returns = ctk.CTkFrame(self.notif_frame, fg_color="transparent", border_width=1)
        self.returns.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        self.returns.grid_columnconfigure(0, weight=1)
        self.returns.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(self.returns, text="UPCOMING RETURN DUES", font=("Helvetica", 15, 'bold')).grid(row=0, column=0, pady=10)
        self.returns_list = ctk.CTkScrollableFrame(self.returns, fg_color="transparent")
        self.returns_list.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)

        self.activities = ctk.CTkFrame(self.notif_frame, fg_color="transparent", border_width=1)
        self.activities.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        self.activities.grid_columnconfigure(0, weight=1)
        self.activities.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(self.activities, text="RECENT ACTIVITIES", font=("Helvetica", 15, 'bold')).grid(row=0, column=0, pady=10)
        self.acts_list = ctk.CTkScrollableFrame(self.activities, fg_color="transparent")
        self.acts_list.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
        
        self.show_logs()
        self.show_borrowed()

    def create_summary_container(self, title, column, total_number):
        total_number = total_number if total_number else 0
        self.frame = ctk.CTkFrame(self.summary_frame, border_width=1)
        self.frame.grid(row=0, column=column, padx=10, sticky="nsew")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame_books = ctk.CTkLabel(self.frame, text=total_number, font=("Helvetica", 30, 'bold'))
        self.frame_books.grid(row=0, column=0, pady=(5, 0), sticky='s')
        ctk.CTkLabel(self.frame, text=title, font=("Helvetica", 13, 'bold')).grid(row=1, column=0, pady=(0, 5), sticky='n')   

    def total_bks(self):    
        self.db.execute_query("SELECT COUNT(*) FROM book_items")
        results = self.db.cursor.fetchone()
        return results['COUNT(*)']
    
    def total_available(self):
        self.db.execute_query("SELECT COUNT(*) FROM book_items WHERE status = 'Available'")
        results = self.db.cursor.fetchone()
        return results['COUNT(*)']
    
    def total_borrowed(self):
        self.db.execute_query("SELECT COUNT(*) FROM transactions WHERE status = 'Borrowed'")
        results = self.db.cursor.fetchone()
        return results['COUNT(*)']

    def total_due(self):
        self.db.execute_query("SELECT COUNT(*) FROM transactions WHERE status = 'Overdue'")
        results = self.db.cursor.fetchone()
        return results['COUNT(*)']
    
    def total_lost_damaged(self):
        self.db.execute_query("SELECT COUNT(*) FROM book_items WHERE status = 'Lost' OR status = 'Damaged'")
        results = self.db.cursor.fetchone()
        return results['COUNT(*)']

    def fetch_logs(self, limit=20):
        db = Database()
        query = "SELECT * FROM activity_log ORDER BY timestamp DESC LIMIT %s"
        return db.fetch_all(query, (limit, ))
        
    def get_book_details(self, log):
        results = []
        book_id_row = self.db.fetch_one("SELECT book_id FROM book_items WHERE rfid = %s", (log['rfid'],))
        if book_id_row:
            book_id = book_id_row['book_id']
            book_row = self.db.fetch_one("SELECT book_title FROM books WHERE book_id = %s", (book_id,))
            if book_row:
                book_title = book_row['book_title']
                results.append({
                    "book_id": book_id,
                    "book_title": book_title
                })
        return results
        

    def show_logs(self):
        logs = self.fetch_logs()
        for log in logs:
            color = {
                "Added": "#28AA00",
                "Updated": "#1877C5",
                "Deleted": "#BB0F0F",
                "Borrowed": "#BE4A14",  
                "Returned": "#076837",  
                "Overdue": "#5A076B"   
            }.get(log["action"], "#607D8B")
            
            card = ctk.CTkFrame(self.acts_list, corner_radius=10, border_width=1, border_color=color)
            card.pack(fill="x", padx=10, pady=5)

            action_label = ctk.CTkLabel(card, text=log["action"], text_color=color, font=("Arial", 15, "bold"))
            action_label.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")
            
            book_info = ""

            for key in self.get_book_details(log):
                book_info = f"{key['book_title']} (ID: {key['book_id']})"
            
            ctk.CTkLabel(card, text=book_info, font=("Arial", 13, "italic"), wraplength=280).grid(row=1, column=0, padx=10, sticky="w")

            performer = "System"
            timestamp = datetime.strptime(str(log["timestamp"]), "%Y-%m-%d %H:%M:%S")
            time_str = timestamp.strftime("%b %d, %Y - %I:%M %p")

            footer = f"By: {performer}  •  {time_str}"
            ctk.CTkLabel(card, text=footer, font=("Arial", 11, "italic")).grid(row=2, column=0, padx=10, pady=(0, 5), sticky="w")

    def fetch_borrowed(self, limit=20):
        db = Database()
        query = """
        SELECT 
            t.rfid,
            t.user_id,
            t.user_name,
            t.user_email,
            t.borrowed_date,
            t.due_date,
            t.return_date,
            t.status,
            t.overdue_notified,
            b.book_title,
            bi.rfid
        FROM transactions t
        JOIN book_items bi ON bi.rfid = t.rfid
        JOIN books b ON b.book_id = bi.book_id
        WHERE t.status = 'Borrowed' OR t.status = 'Overdue' ORDER BY borrowed_date DESC LIMIT %s
        """
        
        return db.fetch_all(query, (limit, ))
        

    def show_borrowed(self):
        db = Database()
        books = self.fetch_borrowed()
        if books:
            for entry in books:

                due_date = entry["due_date"]  
                now = datetime.now()

                delta = due_date - now  
                total_hours = delta.total_seconds() / 60  
                hours = int(total_hours)

                overdue_txt = 'Overdue' if due_date <= now else f"Due in {hours} minutes"
                

                color = "#800707" if hours <= 2 else "#470881" if hours <= 5 else "#09428B"
                
                card = ctk.CTkFrame(self.returns_list, corner_radius=10, border_width=1, border_color=color)
                card.pack(fill="x", padx=10, pady=5)
                
                action_label = ctk.CTkLabel(card, text=overdue_txt, text_color=color, font=("Arial", 15, "bold"))
                action_label.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")

                book_info = f"{entry['book_title']} (ID: {entry['rfid']})"
                ctk.CTkLabel(card, text=book_info, font=("Arial", 13, "italic")).grid(row=1, column=0, padx=10, sticky="w")

                borrower = entry["user_name"]
                user_id = entry['user_id']
                footer = f"By: {borrower} [ {user_id} ]"
                ctk.CTkLabel(card, text=footer, font=("Arial", 11, "italic")).grid(row=2, column=0, padx=10, pady=(0, 5), sticky="w")

