import retro as ret
from typing import Callable

class RoundUI:
    def __init__(self, app, previous_page):
        self.app = app
        self.app_window = self.app.window
        self.app_widget = self.app.widget
        self.app_widget_list = self.app.widget_list


        self.__game_engine = ret.PongManager()

        self.previous_page = previous_page

        self.paused = False

      
    def render(self, playground_name: str, gamemode: str, gametype: str) -> None:
        self.app_window.clear_page(self.app_widget_list)

        # * Prepares the rendering of each object before match start
        round = self.__game_engine.setup(
            tkinter_window = self.app_window.root(),
            playground_name = playground_name.lower(),
            gamemode = gamemode.upper(),
            gametype = gametype,
            responsiveness = True,
            automatic_start = False
        )

        prepared_playground: ret.PlayGround = round['playground']
        self.app_widget_list.append(prepared_playground.master)
        self.app_widget_list.append(round['platform_canvas'])

        self.apply_pause(self.app_window.root(), prepared_playground)

        
        # * Starts the game loop or round loop to be called ^-^
        prepared_playground.start_roundloop()


    def apply_pause(self, root, prepared_playground: ret.PlayGround) -> None:
        menu_pause_canvas1 = self.app_widget.create_canvas_popper(prepared_playground.platform, y_coordinate = 0.25,  width=290, height=80, bg="#E86458", highlightthickness=2, highlightbackground="black")

        canvas1 = menu_pause_canvas1.get_canvas()

        canvas1.create_rectangle(0, 75, 300, 90, fill="#823831", outline="")

        canvas1.create_text(300 / 2, 80 / 2,  text="PAUSE", font=("Pixel Emulator", 25), fill="white", anchor="center")

        menu_pause_canvas2 = self.app_widget.create_canvas_popper(prepared_playground.platform, y_coordinate = 0.6,  width=290, height=300, bg="#FFCF6B", highlightthickness=2, highlightbackground="black")

        canvas2 = menu_pause_canvas2.get_canvas()

        canvas2.create_rectangle(0, 293, 300, 310, fill="#786130", outline="")

        self.app_widget.create_canvas_keybind_sign(master_canvas=prepared_playground.master, key_bind='ESC', x_coordinate=1080, y_coordinate=680,image_path=r'assets\keyboard_bindings.png', img_width=40, img_height=24, text='Pause', gap=50, font=("SF Pixelate", 10))

        self.display_options(canvas2, prepared_playground, menu_pause_canvas1, menu_pause_canvas2)

        root.bind("<Escape>", lambda event: self.menu_popper(prepared_playground, menu_pause_canvas1, menu_pause_canvas2))
    

    def display_options(self, canvas, prepared_playground, menu_pause_canvas1, menu_pause_canvas2) -> None:
        """ Main menu options """
        resume_button = self.app_widget.create_canvas_button_text(canvas, 150.5 ,60,orig_text="Resume",sub_text="| Resume |",font=("Pixelify Sans",18), fill='#252321')
        settings_button = self.app_widget.create_canvas_button_text(canvas, 150.5 ,133,orig_text="Settings",sub_text="| Settings |",font=("Pixelify Sans",18), fill='#252321')
        surrender_button = self.app_widget.create_canvas_button_text(canvas, 150.5 ,206,orig_text="Surrender",sub_text="| Surrender |",font=("Pixelify Sans",18), fill='#252321')

        self.handle_inputs(canvas, resume_button, settings_button, surrender_button, prepared_playground, menu_pause_canvas1, menu_pause_canvas2)

    def handle_inputs(self, menu_option_canvas: int, resume_btn: int, settings_btn: int, surrender_btn: int, prepared_playground, menu_pause_canvas1, menu_pause_canvas2) -> None:
        """ Handles user inputs """
        menu_option_canvas.tag_bind(resume_btn, "<Button-1>", lambda event: self.menu_popper(prepared_playground, menu_pause_canvas1, menu_pause_canvas2))
        # menu_option_canvas.tag_bind(settings_btn, "<Button-1>", lambda event: self.app.settings.render())
        menu_option_canvas.tag_bind(surrender_btn, "<Button-1>",lambda event: self.surrender())
    

    def surrender(self) -> None:
        self.paused = False
        self.previous_page.render()


    def menu_popper(self, prepared_playground: ret.PlayGround, menu_pause_canvas1, menu_pause_canvas2) -> None:
        menu_pause_canvas1.toggle()
        menu_pause_canvas2.toggle()

        if self.paused:
            # * Pause Feature
            prepared_playground.start_roundloop()
            self.paused = False
        else:
            # * Continue Feature
            prepared_playground.stop_roundloop()
            self.paused = True

