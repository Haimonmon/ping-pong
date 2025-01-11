import retro as ret

class RoundUI:
    def __init__(self, app, previous_page):
        self.app = app
        self.app_window = self.app.window
        self.app_widget = self.app.widget
        self.app_widget_list = self.app.widget_list


        self.__game_engine = ret.PongManager()

        self.previous_page = previous_page

        
    def render(self, playground_name: str, gamemode: str, gametype: str) -> None:
        self.app_window.clear_page(self.app_widget_list)

        self.__game_engine.setup(
            tkinter_window = self.app_window.root(),
            playground_name = playground_name.lower(),
            gamemode = gamemode.upper(),
            gametype = gametype
        )

    def handle_inputs(self, canvas) -> None:
        self.app_widget.create_canvas_keybind_sign(master_canvas=canvas, key_bind='B', x_coordinate=883, y_coordinate=519,image_path=r'assets\keyboard_bindings.png', img_width=22, img_height=22, text='Back', gap=40, font=("SF Pixelate", 10), command = self.previous_page.render)
    