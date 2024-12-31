import retro
import widgets as tkw


class PongClassic:
    def __init__(self):
        self.__window = tkw.WindowGenerator()

        self.widget = self.__window.widget_generator()

        self.widget_list = []

        self.__window.run(func=self.display_main_menu(), window_width=1000,window_height=580, window_title="Pong Classic", resize_status=False)

        
    def display_main_menu(self) -> None:
        """
        Main Menu of the game or so called Home
        """
        self.__window.clear_page(self.widget_list)

        main_canvas = self.widget.create_canvas(width=1000, height=580, background="#1D313C", highlightthickness=0, pack={"fill": 'both', "expand": True})

        inner_canvas = self.widget.create_canvas(parent_widget=main_canvas, width=955, height=534, background="#1D313C", highlightthickness=2, bd=0, relief='solid', highlightbackground='#FADAC1', place={"relx": 0.5, "rely": 0.5, "anchor": "center"})

        menu_option_canvas = self.widget.create_canvas(parent_widget=inner_canvas, width=325, height=264, background="#1D313C", highlightthickness=2, bd=0, relief='solid', highlightbackground='#FADAC1', place={"x": 325, "y": 243})
        self.widget_list.append(menu_option_canvas)
        self.widget_list.append(inner_canvas)
        self.widget_list.append(main_canvas)

        self.widget.create_canvas_image(inner_canvas, 325, 60, orig_image=r"assets\Paddle_Wshadow.png", img_width=33, img_height=140)
        self.widget.create_canvas_image(inner_canvas, 380, 70, orig_image=r"assets\PongTxt_Wshadow.png", img_width=243, img_height=63)
        self.widget.create_canvas_image(inner_canvas, 380, 138, orig_image=r"assets\ClassicTxt_Wshadow.png", img_width=245, img_height=45)
        self.widget.create_canvas_image(inner_canvas, 633, 60, orig_image=r"assets\Paddle_Wshadow.png", img_width=33, img_height=140)


        start_button = self.widget.create_canvas_button_text(menu_option_canvas, 162.5 ,60,orig_text="Start",sub_text=">>    Start    <<",font=("Pixelify Sans",14), fill='#F37844')
        settings_button = self.widget.create_canvas_button_text(menu_option_canvas, 162.5 ,108,orig_text="Settings",sub_text=">>    Settings    <<",font=("Pixelify Sans",14), fill='#FADAC1')
        about_button = self.widget.create_canvas_button_text(menu_option_canvas, 162.5 ,157,orig_text="About",sub_text=">>    About    <<",font=("Pixelify Sans",14), fill='#FADAC1')
        quit_button = self.widget.create_canvas_button_text(menu_option_canvas, 162.5 ,206,orig_text="Quit",sub_text=">>    Quit    <<",font=("Pixelify Sans",14), fill='#F37844')

        menu_option_canvas.tag_bind(start_button, "<Button-1>", lambda event: self.display_game_modes())
        menu_option_canvas.tag_bind(quit_button, "<Button-1>",lambda event: self.quit())


    def display_game_modes(self) -> None:
        """
        Shows 3 different types of gamemodes
        """
        self.__window.clear_page(self.widget_list)

        main_canvas = self.widget.create_canvas(width=1000, height=580, background="#1D313C", highlightthickness=0, pack={"fill": 'both', "expand": True})

        inner_canvas = self.widget.create_canvas(parent_widget=main_canvas, width=955, height=534, background="#1D313C", highlightthickness=2, bd=0, relief='solid', highlightbackground='#FADAC1', place={"relx": 0.5, "rely": 0.5, "anchor": "center"})
        self.widget_list.append(inner_canvas)
        self.widget_list.append(main_canvas)

        player_vs_ai_canvas =  self.widget.create_canvas(parent_widget= inner_canvas, width = 153, height = 338, background="#1D313C", highlightthickness=3.5, highlightbackground='#FFCF6B', place={"x": 163, "y": 145})
        player_vs_player_canvas =  self.widget.create_canvas(parent_widget = inner_canvas, width = 153, height = 338, background="#1D313C", highlightthickness=3.5, highlightbackground='#8780A9', place={"x": 400, "y": 145})
        custom_mode_canvas =  self.widget.create_canvas(parent_widget= inner_canvas, width = 153, height = 338, background="#1D313C", highlightthickness=3.5, highlightbackground='#73A627', place={"x": 637, "y": 145})

        self.widget_list.append(player_vs_ai_canvas)
        self.widget_list.append(player_vs_player_canvas)
        self.widget_list.append(custom_mode_canvas)

        game_mode_txt = self.widget.create_canvas_image(inner_canvas, 360, 22, orig_image=r"assets\GamemodeTxt_Wshadow.png", img_width=261, img_height=44)
        print(game_mode_txt)

        pva_card = self.widget.create_canvas_image(player_vs_ai_canvas, 26.5, 17, orig_image=r"assets\pva_GamemodeCard.png", img_width=110, img_height=315)
        pvp_card = self.widget.create_canvas_image(player_vs_player_canvas, 26.5, 17, orig_image=r"assets\pvp_GamemodeCard.png", img_width=110, img_height=315)
        cm_card = self.widget.create_canvas_image(custom_mode_canvas, 26.5, 17, orig_image=r"assets\cm_GamemodeCard.png", img_width=110, img_height=315)

        self.widget.create_canvas_image_popper(canvas = inner_canvas,widget_to_hover = pvp_card, widget_canvas = player_vs_player_canvas, x = 475,y = 110, image_path = r"assets\pvp_Gamemode_ArrowSelection.png", img_width = 51, img_height = 38, debug_show = False)
        self.widget.create_canvas_image_popper(canvas = inner_canvas,widget_to_hover = pva_card, widget_canvas = player_vs_ai_canvas, x = 238,y = 110, image_path = r"assets\pva_Gamemode_ArrowSelection.png", img_width = 51, img_height = 38, debug_show = False)
        self.widget.create_canvas_image_popper(canvas = inner_canvas,widget_to_hover = cm_card, widget_canvas = custom_mode_canvas, x = 712,y = 110, image_path = r"assets\cm_Gamemode_ArrowSelection.png", img_width = 51, img_height = 38, debug_show = False)

        self.widget.apply_canvas_cursor_auto_move(canvas= inner_canvas, movement_coordinates=[(239.5, 314), (476.5, 314), (713.5, 314)], navigations = "WASD")


    def quit(self) -> None:
        print(' Boinking as always :), Thank you. . . . <3')
        self.__window.exit(self.widget_list)

if __name__ == "__main__":
    app = PongClassic()

