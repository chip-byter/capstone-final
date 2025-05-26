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

        self.total = ctk.CTkFrame(self.summary_frame, border_width=1)
        self.total.grid(row=0, column=0, padx=10, sticky="nsew")
        self.total.grid_columnconfigure(0, weight=1)
        self.total.grid_rowconfigure(0, weight=1)
        self.total.grid_rowconfigure(1, weight=1)
        self.total_books = ctk.CTkLabel(self.total, text=self.total_bks(), font=("Helvetica", 30, 'bold'))
        self.total_books.grid(row=0, column=0, pady=(5, 0), sticky="s")
        ctk.CTkLabel(self.total, text="Total Books", font=("Helvetica", 13, 'bold')).grid(row=1, column=0, pady=(0, 5), sticky="n")

        self.borrowed = ctk.CTkFrame(self.summary_frame, border_width=1)
        self.borrowed.grid(row=0, column=1, padx=10, sticky="nsew")
        self.borrowed.grid_columnconfigure(0, weight=1)
        self.borrowed.grid_rowconfigure(0, weight=1)
        self.borrowed.grid_rowconfigure(1, weight=1)
        self.borrowed_books = ctk.CTkLabel(self.borrowed, text=self.total_borrowed(), font=("Helvetica", 30, 'bold'))
        self.borrowed_books.grid(row=0, column=0, pady=(5, 0), sticky="s")
        ctk.CTkLabel(self.borrowed, text="Borrowed Books", font=("Helvetica", 13, 'bold')).grid(row=1, column=0, pady=(0, 5), sticky='n')

        self.overdue = ctk.CTkFrame(self.summary_frame, border_width=1)
        self.overdue.grid(row=0, column=2, padx=10, sticky="nsew")
        self.overdue.grid_columnconfigure(0, weight=1)
        self.overdue.grid_rowconfigure(0, weight=1)
        self.overdue.grid_rowconfigure(1, weight=1)
        self.overdue_books = ctk.CTkLabel(self.overdue, text=self.total_due(), font=("Helvetica", 30, 'bold'))
        self.overdue_books.grid(row=0, column=0, pady=(5, 0), sticky='s')
        ctk.CTkLabel(self.overdue, text="Overdue Books", font=("Helvetica", 13, 'bold')).grid(row=1, column=0, pady=(0, 5), sticky='n')

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
        self.list = ctk.CTkScrollableFrame(self.returns, fg_color="transparent")
        self.list.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)

        self.activities = ctk.CTkFrame(self.notif_frame, fg_color="transparent", border_width=1)
        self.activities.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        self.activities.grid_columnconfigure(0, weight=1)
        self.activities.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(self.activities, text="RECENT ACTIVITIES", font=("Helvetica", 15, 'bold')).grid(row=0, column=0, pady=10)
        self.list = ctk.CTkScrollableFrame(self.activities, fg_color="transparent")
        self.list.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
        
        
    def total_bks(self):    
        self.db.execute_query("SELECT COUNT(*) FROM books")
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