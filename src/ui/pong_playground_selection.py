class PlayGroundSelection:
    def __init__(self, app, previous_page):
        self.app = app
        self.previous_page = previous_page
        self.app_window = self.app.window
        self.app_widget = self.app.widget
        self.app_widget_list = self.app.widget_list


    def render(self, gamemode: str) -> None:
        pass


    def input_handlers(self) -> None:
        pass