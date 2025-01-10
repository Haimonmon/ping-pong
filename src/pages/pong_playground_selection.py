import retro as ret
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

        self.__game_engine: ret = ret.PongManager()

        self.__list_maps = self.__game_engine.get_map_details()

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

        self.generate_buttons(canvas = inner_canvas)

        self.handle_inputs(inner_canvas)

        print('Selected Game Mode: ', self.game_mode_text_images[gamemode])


    def handle_inputs(self, canvas) -> None:
        self.app_widget.create_canvas_keybind_sign(master_canvas=canvas, key_bind='B', x_coordinate=883, y_coordinate=519,image_path=r'assets\keyboard_bindings.png', img_width=22, img_height=22, text='Back', gap=40, font=("SF Pixelate", 10), command = self.previous_page.render)
    

    def generate_buttons(self, canvas: tk.Canvas) -> None:
        self.selected_button = None
        self.selected_button_txt = None

        self.hovering = False

        gap = 50
        start_y = 90
        for i in range(1, len(self.__list_maps) + 1):
            playground_btn = canvas.create_rectangle(76, start_y, 103, start_y + 27, outline='#FADAC1', fill = '#1D313C',width=1)
            playground_btn_txt = canvas.create_text(89.5, start_y + (27 // 2), fill='white', text=i, font = ('Pixel Emulator', 9))

            hitbox = canvas.create_rectangle(76, start_y, 103, start_y + 27, outline='', fill='')

            canvas.tag_bind(hitbox, "<Enter>", lambda event, button=playground_btn, text_btn=playground_btn_txt: hover_btn(event, button, canvas, text_btn))
            canvas.tag_bind(hitbox, "<Leave>", lambda event, button=playground_btn, text_btn=playground_btn_txt: unhover_btn(event, button, canvas, text_btn))

            canvas.tag_bind(hitbox, "<Button-1>", lambda event, index = i - 1, button = playground_btn, text_btn = playground_btn_txt: select_button(event, button, canvas, text_btn, index))
            
            start_y += gap

        def hover_btn(event, button = None, canvas = None, text = None) -> None:
            self.hovering = True

            if self.selected_button != button:
                event.widget["cursor"] = "@assets/Link.cur"
                if button:
                    canvas.itemconfig(button, fill = '#F7723A')
                    canvas.after(15,lambda: canvas.move(button, -9, 0))
                    canvas.after(15,lambda: canvas.move(text, -9, 0)) 


        def unhover_btn(event, button = None, canvas = None, text = None) -> None:
            self.hovering = False

            if self.selected_button != button:
                event.widget["cursor"] = "@assets/Alternate.cur"
                if button:
                    canvas.itemconfig(button, fill='#1D313C')
                    canvas.after(15,lambda: canvas.move(button, 9, 0))
                    canvas.after(15, lambda: canvas.move(text, 9, 0))


        def select_button(event, button=None, canvas=None, text=None, index=None) -> None:           
            if self.selected_button == button:
                return 
            
            if self.selected_button and self.selected_button != button:
                canvas.itemconfig(self.selected_button, fill='#1D313C')
                canvas.move(self.selected_button, 9, 0)
                canvas.move(self.selected_button_txt, 9, 0)

                
            self.selected_button = button
            self.selected_button_txt = text
            canvas.itemconfig(button, fill='#F7723A')
            
            if not self.hovering:
                canvas.move(button, -9, 0)
                canvas.move(text, -9, 0)
            else:
                canvas.move(button, 0, 0)
                canvas.move(text, 0, 0)
                
            self.change_current_index(index)


    def change_current_index(self , index) -> None:
        self.current_playground_index = index

        selected_map = self.__list_maps[self.current_playground_index]

        print('Selected: ', selected_map['name'])

        


