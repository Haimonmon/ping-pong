import pages
import widgets as tkw

class PongClassic:
    def __init__(self):
        self.window = tkw.WindowGenerator()

        self.widget = self.window.widget_generator()

        self.widget_list = [] # * Planning to change this way of single paging soon :)

        self.main_menu = pages.MainMenuUI(self)
        self.settings = pages.SettingsUI(self, previous_page = self.main_menu)
        self.gamemodes = pages.GameModesUI(self, previous_page = self.main_menu)
        self.playground_selection = pages.PlayGroundSelection(self, previous_page = self.gamemodes)
      
        self.window.run(
            func = self.main_menu.render, 
            window_width = 1000,
            window_height = 580, 
            window_title = "Pong Classic ( Alpha )", 
            resize_status = False, 
        )

    def quit(self) -> None:
        self.window.exit(self.widget_list)
        print(' Boinking as always :), Thank you. . . . <3')

if __name__ == "__main__":
    app = PongClassic()

