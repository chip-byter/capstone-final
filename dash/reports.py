from datetime import datetime
from io import BytesIO
import re
import customtkinter as ctk
from tkinter import ttk
import pandas as pd 
from core.emailsys import send_excel_report
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
        self.filter_frame.grid(row=0, column=0, sticky="ew")

        self.filter_mode = ctk.CTkOptionMenu(self.filter_frame, values=["Transactions", "Books"], command=self.update_filter_options)
        self.filter_mode.set("Transactions")
        self.filter_mode.grid(row=0, column=0, padx=10)

        # RADIO OPTIONS
        self.filter_options = ["Borrowed Books", "Overdue Books", "Returned Books"]

        self.report_option = ctk.CTkOptionMenu(self.filter_frame, values=[], command=self.generate_report)
        self.report_option.set("Borrowed Books")
        self.report_option.grid(row=0, column=1, padx=10)

        self.start_date = ctk.CTkEntry(self.filter_frame, placeholder_text="Start Date (YYYY-MM-DD)")
        self.start_date.grid(row=0, column=2, padx=10)

        self.end_date = ctk.CTkEntry(self.filter_frame, placeholder_text="End Date (YYYY-MM-DD)")
        self.end_date.grid(row=0, column=3, padx=10)

        self.search_button = ctk.CTkButton(self.filter_frame, text="Generate Report", width=80, command=self.generate_report)
        self.search_button.grid(row=0, column=4, padx=10)

        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.grid(row=1, column=0, pady=10, padx=5, sticky="nsew")
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)

        # EXPORT EXCEL BUTTON
        self.export_btns = ctk.CTkFrame(self)
        self.export_btns.grid(row=2, column=0, sticky="ew")
        self.export_btns.grid_columnconfigure(0, weight=1)
        self.export_btns.grid_columnconfigure(1, weight=1)
        self.export_btns.grid_columnconfigure(2, weight=1)

        self.export_excel = ctk.CTkButton(self.export_btns, text="Send Report", width=100, command=self.send_report)
        self.export_excel.grid(row=0, column=2, padx=10, sticky="e")

        self.total_label = ctk.CTkLabel(self.export_btns, text="Total : ", width=150, anchor="w", fg_color="gray")
        self.total_label.grid(row=0, column=0, padx=10, sticky="w")

        self.pagination_frame = ctk.CTkFrame(self.export_btns, fg_color="transparent")
        self.pagination_frame.grid(row=0, column=1)

        self.prev_button = ctk.CTkButton(self.pagination_frame, text=" < Previous ", fg_color="transparent" , width=80, hover=None, text_color="black", command=self.previous_page)
        self.prev_button.grid(row=0, column=0, padx=5)

        self.page_label = ctk.CTkLabel(self.pagination_frame, text="Page 1")
        self.page_label.grid(row=0, column=1, padx=5)

        self.next_button = ctk.CTkButton(self.pagination_frame, text=" Next > ", fg_color="transparent" , width=80, hover=None, text_color="black", command=self.next_page)
        self.next_button.grid(row=0, column=2, padx=5)

        self.columns = ("rfid", "user_id", "borrowed_date", "due_date", "status")
        self.tree = ttk.Treeview(self.tree_frame, columns=self.columns, show='headings')

        column_titles = {
            "rfid": "RFID",
            "user_id": "User ID",
            "borrowed_date": "Borrow Date",
            "due_date": "Due Date",
            "status": "Status"
        }

        for col in self.columns:
            self.tree.heading(col, text=column_titles[col])
            self.tree.column(col, anchor="center", stretch=True, width=100)

        self.tree.pack(fill="both", expand=True)

        self.update_filter_options("Transactions")

        # PAGINATION
        self.rows_per_page = 10
        self.current_page = 1
        self.total_pages = 1

        self.report_data = []

    def update_filter_options(self, selected_mode):
        if selected_mode == "Transactions":
            options = ["Borrowed Books", "Overdue Books", "Returned Books"]
            self.report_option.configure(values=options)
            self.report_option.set("Borrowed Books")  # default
        elif selected_mode == "Books":
            options = ["All Books", "Available", "Borrowed", "Lost", "Damaged"]
            self.report_option.configure(values=options)
            self.report_option.set("All Books")  #

    def generate_report(self, *args):
        mode = self.filter_mode.get()
        selected = self.report_option.get()
        start = self.start_date.get()
        end = self.end_date.get()

        self.report_data = []

        if mode == "Books":
            if selected in ["All Books", "Available", "Borrowed", "Lost", "Damaged"]:
                query = """
                    SELECT 
                        books.book_id,
                        books.book_title,
                        books.book_author,
                        book_items.rfid,
                        book_items.status
                    FROM books
                    INNER JOIN book_items ON books.book_id = book_items.book_id
                """
                params = []
                if selected != "All Books":
                    query += " WHERE book_items.status = %s"
                    params.append(selected)

                self.columns = ("book_id", "book_title", "book_author", "rfid", "status")
                column_titles = {
                    "book_id": "Book ID",
                    "book_title": "Title",
                    "book_author": "Author",
                    "rfid": "RFID",
                    "status": "Status"
                }

        if mode == "Transactions":
            if selected in ["Borrowed Books", "Overdue Books", "Returned Books"]:
                query = "SELECT rfid, user_id, borrowed_date, due_date, status FROM transactions"
                params = []

                if selected == "Borrowed Books":
                    query += " WHERE status = 'Borrowed'"
                elif selected == "Overdue Books":
                    query += " WHERE status = 'Overdue'"
                elif selected == "Returned Books":
                    query += " WHERE status = 'Returned'"

                if start and end:
                    if "WHERE" in query:
                        query += " AND borrowed_date BETWEEN %s AND %s"
                    else:
                        query += " WHERE borrowed_date BETWEEN %s AND %s"
                    params.extend([start, end])

                self.columns = ("rfid", "user_id", "borrowed_date", "due_date", "status")
                column_titles = {
                    "rfid": "RFID",
                    "user_id": "User ID",
                    "borrowed_date": "Borrow Date",
                    "due_date": "Due Date",
                    "status": "Status"
                }

        self.report_data = self.db.fetch_all(query, tuple(params))
        self.total_label.configure(text=f"Total {selected}: {len(self.report_data)}")
        self.update_treeview_headers(column_titles)
        self.current_page = 1
        self.populate_treeview()


    def update_treeview_headers(self, column_titles):
        self.tree.delete(*self.tree.get_children())  
        self.tree["columns"] = self.columns
        for col in self.tree["columns"]:
            self.tree.heading(col, text=column_titles[col])
            self.tree.column(col, anchor="center", width=120)


    def populate_treeview(self):
        self.tree.delete(*self.tree.get_children())

        start_index = (self.current_page - 1) * self.rows_per_page
        end_index = start_index + self.rows_per_page
        paginated_data = self.report_data[start_index:end_index]

        for record in paginated_data:
            values = [record.get(col, "") for col in self.columns]
            self.tree.insert('', 'end', values=values)

        self.total_pages = max(1, (len(self.report_data) + self.rows_per_page - 1) // self.rows_per_page)
        self.page_label.configure(text=f"Page {self.current_page} of {self.total_pages}")

        self.prev_button.configure(state="normal" if self.current_page > 1 else "disabled")
        self.next_button.configure(state="normal" if self.current_page < self.total_pages else "disabled")

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.populate_treeview()

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.populate_treeview()

    def export_as_excel(self):
        mode = self.report_option.get()
        current_date = datetime.now().strftime("%Y-%m-%d")
        formatted_type = re.sub(r'\s+', '_', mode.strip().lower())
        filename = f"report_{formatted_type}_{current_date}.xlsx"

        df = pd.DataFrame(self.report_data, columns=self.columns)
        buffer = BytesIO()

        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, startrow=1, sheet_name='Report')
            # workbook = writer.book
            worksheet = writer.sheets['Report']
            for col in ['A', 'B', 'C', 'D', 'E']:
                worksheet.column_dimensions[col].width = 30
            worksheet['A1'] = f"{mode}"
            worksheet['B1'] = f"Report generated on: {current_date}"

        buffer.seek(0) 
        return buffer, filename
     
    def open_report_form(self):
        self.report_form = ctk.CTkToplevel(self)
        self.report_form.title("Data Report Settings")
        


    def send_report(self):
        buffer, filename = self.export_as_excel()
        send_excel_report(
            recipient='delacruz.ellezir@gmail.com',
            subject='Organicer Report',
            body='Please see the attached file of the automated library report.',
            file_buffer=buffer,
            filename=filename
        )

  