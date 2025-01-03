import ui
import retro
import widgets as tkw


class PongClassic:
    def __init__(self):
        self.window = tkw.WindowGenerator()

        self.widget = self.window.widget_generator()

        self.widget_list = [] # * Planning to change this way of single paging soon :)

        self.main_menu = ui.MainMenuUI(self)
      
        self.window.run(func=self.main_menu.render(), window_width=1000,window_height=580, window_title="Pong Classic ( Alpha )", resize_status=False)


    def quit(self) -> None:
        print(' Boinking as always :), Thank you. . . . <3')
        self.window.exit(self.widget_list)

if __name__ == "__main__":
    app = PongClassic()

