from dash.inventory import Inventory
from dash.overview import Overview
from dash.transactions import Transactions
from dash.reports import Reports


def register_routes(navigator):

    navigator.register_page("inventory_page", Inventory)
    navigator.register_page("overview_page", Overview)
    navigator.register_page("transactions_page", Transactions)
    navigator.register_page("reports_page", Reports)

    