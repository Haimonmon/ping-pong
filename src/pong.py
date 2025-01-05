import ui
import widgets as tkw

class PongClassic:
    def __init__(self):
        self.window = tkw.WindowGenerator()

        self.widget = self.window.widget_generator()

        self.widget_list = [] # * Planning to change this way of single paging soon :)

        self.main_menu = ui.MainMenuUI(self)
        self.settings = ui.SettingsUI(self, previous_page = self.main_menu)
        self.gamemodes = ui.GameModesUI(self, previous_page = self.main_menu)
        self.playground_selection = ui.PlayGroundSelection(self, previous_page = self.gamemodes)
      
        self.window.run(
            func = self.main_menu.render, 
            window_width = 1000, 
            window_height = 580, 
            window_title = "Pong Classic ( Alpha )", 
            resize_status = False, 
            cursor_hidden = False
        )

    def quit(self) -> None:
        self.window.exit(self.widget_list)
        print(' Boinking as always :), Thank you. . . . <3')

if __name__ == "__main__":
    app = PongClassic()

