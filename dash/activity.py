from datetime import datetime
import customtkinter as ctk
from core.database import Database

class Activity(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.navigation = controller
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # self.refresh = ctk.CTkButton(self, text="Refersh", width=80, command=self.refresh_activities)
        # self.refresh.grid(row=0, column=0, sticky="e")

        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.grid(row=1, column=0, sticky="nsew")

        self.show_logs()

    # def refresh_activities(self):
    #     for widget in self.scroll_frame.winfo_children():
    #         widget.destroy()

    #     # Reload new logs
    #     self.show_logs()

    def fetch_logs(self, limit=20):
        db = Database()
        query = "SELECT * FROM activity_log ORDER BY timestamp DESC LIMIT %s"
        db.cursor.execute(query, (limit,))
        return db.cursor.fetchall()

    def show_logs(self):
        logs = self.fetch_logs()

        for log in logs:
            card = ctk.CTkFrame(self.scroll_frame, corner_radius=10, border_width=1)
            card.pack(fill="x", padx=10, pady=5)

            color = {
                "Added": "#4CAF50",
                "Updated": "#2196F3",
                "Deleted": "#f44336",
                "Borrowed": "#FF9800",  
                "Returned": "#009688",  
                "Overdue": "#607D8B"   
            }.get(log["action"], "#607D8B")

            action_label = ctk.CTkLabel(card, text=log["action"], text_color=color, font=("Arial", 20, "bold"))
            action_label.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")

            book_info = f"{log['book_title']} (ID: {log['book_id']})"
            ctk.CTkLabel(card, text=book_info, font=("Arial", 17, "italic")).grid(row=1, column=0, padx=10, sticky="w")

            performer = "System"
            timestamp = datetime.strptime(str(log["timestamp"]), "%Y-%m-%d %H:%M:%S")
            time_str = timestamp.strftime("%b %d, %Y - %I:%M %p")

            footer = f"By: {performer}  •  {time_str}"
            ctk.CTkLabel(card, text=footer, font=("Arial", 13, "italic")).grid(row=2, column=0, padx=10, pady=(0, 5), sticky="w")