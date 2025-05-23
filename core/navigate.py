class NavigationController:
    def __init__(self, container):
        self.container = container  
        self.pages = {}             
        self.current_page = None   

    def register_page(self, name, page_class):
        self.pages[name] = page_class

    def navigate_to(self, name, **kwargs):
        if name not in self.pages:
            raise ValueError(f"Page '{name}' not found.")

        if self.current_page is not None:
            self.current_page.destroy()

        page_class = self.pages[name]
        self.current_page = page_class(self.container, self, **kwargs)
        self.current_page.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")