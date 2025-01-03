from .pong_playground_selection import PlayGroundSelection

class GameModesUI:
    def __init__(self, app, previous_page):
       self.app = app
       self.previous_page = previous_page
       self.app_window = self.app.window
       self.app_widget = self.app.widget
       self.app_widget_list = self.app.widget_list

       self.playground_selection = PlayGroundSelection(self.app, self)

    def render(self) -> None:
        """
        Display 3 different types of gamemodes
        """
        self.app_window.clear_page(self.app_widget_list)

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

        game_mode_txt = self.app_widget.create_canvas_image(inner_canvas, 360, 22, orig_image=r"assets\GamemodeTxt_Wshadow.png", img_width=261, img_height=44)

        pva_card = self.app_widget.create_canvas_image(player_vs_ai_canvas, 26.5, 17, orig_image=r"assets\pva_GamemodeCard.png", img_width=110, img_height=315)
        pvp_card = self.app_widget.create_canvas_image(player_vs_player_canvas, 26.5, 17, orig_image=r"assets\pvp_GamemodeCard.png", img_width=110, img_height=315)
        cm_card = self.app_widget.create_canvas_image(custom_mode_canvas, 26.5, 17, orig_image=r"assets\cm_GamemodeCard.png", img_width=110, img_height=315)

        self.app_widget.create_canvas_image_popper(canvas=inner_canvas, widget_to_hover=pvp_card, widget_canvas=player_vs_player_canvas,x=475, y=110, image_path=r"assets\pvp_Gamemode_ArrowSelection.png", img_width=51, img_height=38, debug_show=False)
        self.app_widget.create_canvas_image_popper(canvas=inner_canvas, widget_to_hover=pva_card, widget_canvas=player_vs_ai_canvas,x=238, y=110, image_path=r"assets\pva_Gamemode_ArrowSelection.png", img_width=51, img_height=38, debug_show=False)
        self.app_widget.create_canvas_image_popper(canvas=inner_canvas, widget_to_hover=cm_card, widget_canvas=custom_mode_canvas,x=712, y=110, image_path=r"assets\cm_Gamemode_ArrowSelection.png", img_width=51, img_height=38, debug_show=False)

        self.app_widget.create_canvas_keybind_sign(master_canvas=inner_canvas, key_bind='B', x_coordinate=890 - 7, y_coordinate=523 - 4,image_path=r'assets\keyboard_bindings.png', img_width=22, img_height=22, text='Back', gap=40, font=("SF Pixelate", 10), command=self.previous_page.render)

        self.app_widget.apply_canvas_cursor_auto_move(canvas=inner_canvas, point_coordinates=[(239.5, 314), (476.5, 314), (713.5, 314)], navigations="WASD")

    def handle_inputs(self, canvas) -> None:
       pass
