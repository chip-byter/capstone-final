from dash.inventory import Inventory
from dash.overview import Overview
from dash.transactions import Transactions
from dash.reports import Reports
from dash.activity import Activity

def register_routes(navigator):

    navigator.register_page("inventory_page", Inventory)
    navigator.register_page("overview_page", Overview)
    navigator.register_page("transactions_page", Transactions)
    navigator.register_page("activity_page", Activity)
    navigator.register_page("reports_page", Reports)

    