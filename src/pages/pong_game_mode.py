from .pong_playground_selection import PlayGroundSelection

class GameModesUI:
    def __init__(self, app, previous_page):
       self.app = app
       self.previous_page = previous_page
       self.app_window = self.app.window
       self.app_widget = self.app.widget
       self.app_widget_list = self.app.widget_list

       self.current_mode_selected = None

    def render(self) -> None:
        """
        Display 3 different types of gamemodes
        """
        self.app_window.root().unbind("<Escape>")
        self.app_window.clear_page(self.app_widget_list)
        self.app_window.set_size(width=1000, height=580)

        main_canvas = self.app_widget.create_canvas(width=1000, height=580, background="#1D313C", highlightthickness=0, pack={"fill": 'both', "expand": True})
        self.app_widget_list.append(main_canvas)

        inner_canvas = self.app_widget.create_canvas(parent_widget=main_canvas, width=955, height=534, background="#1D313C", highlightthickness=2, bd=0, highlightcolor='#FADAC1', relief='solid', place={"relx": 0.5, "rely": 0.5, "anchor": "center"})
        self.app_widget_list.append(inner_canvas)

        player_vs_ai_canvas = self.app_widget.create_canvas(parent_widget=inner_canvas, width=153, height=338, background="#1D313C", highlightthickness=3.5, highlightbackground='#FFCF6B', place={"x": 163, "y": 145})
        player_vs_player_canvas = self.app_widget.create_canvas(parent_widget=inner_canvas, width=153, height=338, background="#1D313C", highlightthickness=3.5, highlightbackground='#8780A9', place={"x": 400, "y": 145})
        custom_mode_canvas = self.app_widget.create_canvas(parent_widget=inner_canvas, width=153, height=338,background="#1D313C", highlightthickness=3.5, highlightbackground='#73A627', place={"x": 637, "y": 145})

        self.app_widget_list.append(player_vs_ai_canvas)
        self.app_widget_list.append(player_vs_player_canvas)
        self.app_widget_list.append(custom_mode_canvas)

        game_mode_txt = self.app_widget.create_canvas_image(inner_canvas, 360, 22, orig_image=r"src\assets\GamemodeTxt_Wshadow.png", img_width=261, img_height=44)

        pva_card = self.app_widget.create_canvas_image(player_vs_ai_canvas, 26.5, 17, orig_image=r"src\assets\pva_GamemodeCard.png", img_width=110, img_height=315)
        pvp_card = self.app_widget.create_canvas_image(player_vs_player_canvas, 26.5, 17, orig_image=r"src\assets\pvp_GamemodeCard.png", img_width=110, img_height=315)
        cm_card = self.app_widget.create_canvas_image(custom_mode_canvas, 26.5, 17, orig_image=r"src\assets\cm_GamemodeCard.png", img_width=110, img_height=315)

        self.app_widget.create_canvas_image_popper(canvas=inner_canvas, widget_to_hover=pvp_card, widget_canvas=player_vs_player_canvas,x=475, y=110, image_path=r"src\assets\pvp_Gamemode_ArrowSelection.png", img_width=51, img_height=38, debug_show=False, page = self, text = 'PVP')
        self.app_widget.create_canvas_image_popper(canvas=inner_canvas, widget_to_hover=pva_card, widget_canvas=player_vs_ai_canvas,x=238, y=110, image_path=r"src\assets\pva_Gamemode_ArrowSelection.png", img_width=51, img_height=38, debug_show=False, page = self, text = 'PVA')
        self.app_widget.create_canvas_image_popper(canvas=inner_canvas, widget_to_hover=cm_card, widget_canvas=custom_mode_canvas,x=712, y=110, image_path=r"src\assets\cm_Gamemode_ArrowSelection.png", img_width=51, img_height=38, debug_show=False, page = self, text = 'CM')

        self.handle_inputs(inner_canvas, pva_card, player_vs_ai_canvas, pvp_card, player_vs_player_canvas, cm_card, custom_mode_canvas)


    def handle_inputs(self, canvas, pva_card, pva_canvas, pvp_card, pvp_canvas, cm_card, cm_canvas) -> None:
       
        self.app_widget.create_canvas_keybind_sign(master_canvas=canvas, key_bind='B', x_coordinate=883, y_coordinate=519,image_path=r'src\assets\keyboard_bindings.png', img_width=22, img_height=22, text='Back', gap=40, font=("SF Pixelate", 10), command=self.previous_page.render)

        self.app_widget.create_canvas_keybind_sign(master_canvas=canvas, key_bind='D', x_coordinate=688, y_coordinate=519,image_path=r'src\assets\keyboard_bindings.png', img_width=22, img_height=22, text='Right Selection', gap=83, font=("SF Pixelate", 10))

        self.app_widget.create_canvas_keybind_sign(master_canvas=canvas, key_bind='A', x_coordinate=483, y_coordinate=519,image_path=r'src\assets\keyboard_bindings.png', img_width=22, img_height=22, text='Left Selection', gap=80, font=("SF Pixelate", 10))

        self.app_widget.apply_canvas_cursor_auto_move(canvas=canvas, point_coordinates=[(239.5, 314), (476.5, 314), (713.5, 314)], navigations="WASD", avail_work_navs = [1,3])

        pva_canvas.tag_bind(pva_card, "<Button-1>", lambda event: self.app.playground_selection.render('PVA'))
        pvp_canvas.tag_bind(pvp_card, "<Button-1>", lambda event: self.app.playground_selection.render('PVP'))
        cm_canvas.tag_bind(cm_card, "<Button-1>", lambda event: self.app.playground_selection.render('CM'))

        canvas.bind("<Return>", lambda event: self.select_mode())

    
    def select_mode(self) -> None:
        valid_modes = ['PVA', 'PVP', 'CM']

        if self.current_mode_selected and self.current_mode_selected.upper() in valid_modes:
            self.app.playground_selection.render(self.current_mode_selected)

    
    def change_selection(self, gamemode: str) -> None:
        self.current_mode_selected = gamemode


