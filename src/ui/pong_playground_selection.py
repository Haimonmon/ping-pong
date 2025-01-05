import retro
import tkinter as tk


class PlayGroundSelection:
    def __init__(self, app, previous_page = None):
        self.app = app
        self.previous_page = previous_page
        self.app_window = self.app.window
        self.app_widget = self.app.widget
        self.app_widget_list = self.app.widget_list

        self.game_mode_text_images = {
            'PVA': 'Player Vs Ai Mode ⚡',
            'PVP': 'Player Vs Player Mode 🏓',
            'CM': 'Custom Mode 📦',
            'Developing': 'Testing 🚥'
        }

        self.__game_engine: retro = retro
        self.__playgrounds = self.__game_engine

        self.current_playground_index = 0


    def render(self, gamemode: str) -> None:
        self.app_window.clear_page(self.app_widget_list)

        main_canvas = self.app_widget.create_canvas(width=1000, height=580, background="#1D313C", highlightthickness=0, pack={"fill": 'both', "expand": True})
        self.app_widget_list.append(main_canvas)

        inner_canvas: tk.Canvas = self.app_widget.create_canvas(parent_widget=main_canvas, width=955, height=534, background="#1D313C", highlightthickness=2, bd=0, highlightcolor='#FADAC1', relief='solid', place={"relx": 0.5, "rely": 0.5, "anchor": "center"})
        self.app_widget_list.append(inner_canvas)

        playground_looks_frame = inner_canvas.create_rectangle(124, 92, 830, 441, outline = '#FADAC1', width = 2.5)
        playground_name_frame = inner_canvas.create_rectangle(124, 441, 299, 485, outline = '#FADAC1', width = 2.5)
        playground_gameplay_type_frame = inner_canvas.create_rectangle(397, 441, 830, 485, outline = '#FADAC1', width = 2.5)

        playground_play_button_frame = inner_canvas.create_rectangle(299, 441, 397, 485, outline = '#FADAC1', width = 2.5, fill = '#FF601E')
        playbutton_icon = inner_canvas.create_polygon(342, 462 - 10, 342 + 20, 462, 342, 462 + 10, fill='#FADAC1')

        self.handle_inputs(inner_canvas)

        print('Selected Game Mode: ', self.game_mode_text_images[gamemode])



    def handle_inputs(self, canvas) -> None:
        self.app_widget.create_canvas_keybind_sign(master_canvas=canvas, key_bind='B', x_coordinate=883, y_coordinate=519,image_path=r'assets\keyboard_bindings.png', img_width=22, img_height=22, text='Back', gap=40, font=("SF Pixelate", 10), command = self.previous_page.render)
    

    def generate_buttons(self) -> None:
        pass