from datetime import datetime
import re
import customtkinter as ctk
from tkinter import ttk
import pandas as pd 
from core.database import Database
import openpyxl

class Reports(ctk.CTkFrame):
    def __init__(self, parent, controller, fg_color=None):
        super().__init__(parent, fg_color="transparent")
        self.navigation = controller
        self.db = Database()
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.filter_frame = ctk.CTkFrame(self)
        self.filter_frame.grid(row=0, column=0)

        self.report_type_option = ctk.CTkOptionMenu(
            self.filter_frame,
            values=["Borrowed Books", "Overdue Books", "Returned Books"],
            command=self.generate_report
        )

        self.report_type_option.set("Borrowed Books")
        self.report_type_option.grid(row=0, column=0, padx=10)

        self.start_date = ctk.CTkEntry(self.filter_frame, placeholder_text="Start Date (YYYY-MM-DD)")
        self.start_date.grid(row=0, column=1, padx=10)

        self.end_date = ctk.CTkEntry(self.filter_frame, placeholder_text="End Date (YYYY-MM-DD)")
        self.end_date.grid(row=0, column=2, padx=10)

        self.search_button = ctk.CTkButton(self.filter_frame, text="Generate Report", width=80, command=self.generate_report)
        self.search_button.grid(row=0, column=3, padx=10)

        self.export_excel = ctk.CTkButton(self.filter_frame, text="Export Excel", width=80, command=self.export_as_excel)
        self.export_excel.grid(row=0, column=4, padx=10)

        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.grid(row=1, column=0, pady=10, padx=5, sticky="nsew")
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)

        self.columns = ("book_id", "user_name", "timestamp", "due_date", "status")
        self.tree = ttk.Treeview(self.tree_frame, columns=self.columns, show='headings')

        column_titles = {
            "book_id": "Book ID",
            "user_name": "Borrower",
            "timestamp": "Borrow Date",
            "due_date": "Due Date",
            "status": "Status"
        }

        for col in self.columns:
            self.tree.heading(col, text=column_titles[col])
            self.tree.column(col, anchor="center", stretch=True, width=100)

        self.tree.pack(fill="both", expand=True)

        self.report_data = []

    def generate_report(self, *args):
        report_type = self.report_type_option.get()
        start = self.start_date.get()
        end = self.end_date.get()

        query = ""
        params = []

        if report_type == "Borrowed Books":
            query = "SELECT book_id, user_name, timestamp, due_date, status FROM transactions WHERE status = 'Borrowed'"
        elif report_type == "Overdue Books":
            query = "SELECT book_id, user_name, timestamp, due_date, status FROM transactions WHERE status = 'Overdue'"
        elif report_type == "Returned Books":
            query = "SELECT book_id, user_name, timestamp, due_date, status FROM transactions WHERE status = 'Returned'"

        if start and end:
            query += " AND timestamp BETWEEN %s AND %s"
            params.extend([start, end])

        if query:
            self.report_data = self.db.fetch_all(query, tuple(params))
        else:
            self.report_data = []

        self.populate_treeview()


    def populate_treeview(self):
        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert new rows from dict records
        for record in self.report_data:
            row_values = [
                record.get("book_id", ""),
                record.get("user_name", ""),
                record.get("timestamp", ""),
                record.get("due_date", ""),
                record.get("status", "")
            ]
            self.tree.insert('', 'end', values=row_values)

    def export_as_excel(self):
        report_type = self.report_type_option.get()
        current_date = datetime.now().strftime("%Y-%m-%d")
        formatted_type = re.sub(r'\s+', '_', report_type.strip().lower())

        # Add date to filename
        filename = f"report_{formatted_type}_{current_date}.xlsx"
        df = pd.DataFrame(self.report_data, columns=self.columns)

        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Write the main data starting from row 2 (row index 1)
            df.to_excel(writer, index=False, startrow=1, sheet_name='Report')

            # Access the workbook and sheet to add a date in A1
            workbook = writer.book
            worksheet = writer.sheets['Report']
            for col in ['A', 'B', 'C', 'D', 'E']:
                worksheet.column_dimensions[col].width = 20
                
            worksheet['A1'] = f"{report_type}"
            worksheet['B1'] = f"Report generated on: {current_date}"

        print(f"Exported to [ {filename} ]")
        

  