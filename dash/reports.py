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

        self.filter_frame = ctk.CTkFrame(self)
        self.filter_frame.pack(pady=10, padx=20, fill="x")

        self.report_type_option = ctk.CTkOptionMenu(
            self.filter_frame,
            values=["Borrowed Books", "Overdue Books", "Returned Books", "Inventory Summary"],
            command=self.generate_report
        )
        self.report_type_option.set("Borrowed Books")
        self.report_type_option.grid(row=0, column=0, padx=10)

        self.start_date = ctk.CTkEntry(self.filter_frame, placeholder_text="Start Date (YYYY-MM-DD)")
        self.start_date.grid(row=0, column=1, padx=10)

        self.end_date = ctk.CTkEntry(self.filter_frame, placeholder_text="End Date (YYYY-MM-DD)")
        self.end_date.grid(row=0, column=2, padx=10)

        self.search_button = ctk.CTkButton(self.filter_frame, text="Generate Report", command=self.generate_report)
        self.search_button.grid(row=0, column=3, padx=10)

        # Report Table
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.pack(padx=20, pady=10, fill="both", expand=True)

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
            self.tree.column(col, anchor="center")

        self.tree.pack(fill="both", expand=True)

        # Export Buttons
        self.export_frame = ctk.CTkFrame(self)
        self.export_frame.pack(pady=10)

        self.export_pdf = ctk.CTkButton(self.export_frame, text="Export PDF", command=self.export_as_pdf)
        self.export_pdf.grid(row=0, column=0, padx=10)

        self.export_csv = ctk.CTkButton(self.export_frame, text="Export CSV", command=self.export_as_csv)
        self.export_csv.grid(row=0, column=1, padx=10)

        self.export_excel = ctk.CTkButton(self.export_frame, text="Export Excel", command=self.export_as_excel)
        self.export_excel.grid(row=0, column=2, padx=10)

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

    def export_as_csv(self):
        # df = pd.DataFrame(self.report_data, columns=self.columns)
        # df.to_csv("report.csv", index=False)
        pass

    def export_as_excel(self):
        df = pd.DataFrame(self.report_data, columns=self.columns)
        df.to_excel("report.xlsx", index=False)

    def export_as_pdf(self):
        # df = pd.DataFrame(self.report_data, columns=self.columns)
        # pdf = FPDF()
        # pdf.add_page()
        # pdf.set_font("Arial", size=10)
        # pdf.cell(200, 10, txt="Library Report", ln=True, align='C')

        # for i, row in df.iterrows():
        #     line = " | ".join(str(value) for value in row)
        #     pdf.cell(200, 10, txt=line, ln=True)

        # pdf.output("report.pdf")
        pass