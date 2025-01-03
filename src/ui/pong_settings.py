class SettingsUI:
    def __init__(self, app, previous_page = None):
        self.app = app
        self.previous_page = previous_page
        self.app_window = self.app.window
        self.app_widget = self.app.widget
        self.app_widget_list = self.app.widget_list

        self.option_canvas = None
        self.inner_canvas = None

        self.appearance = AppearanceSettings(self)
        self.controls = ControlSettings(self)
        self.sound = SoundSettings(self)


    def render(self) -> None:
        self.app_window.set_title('Pong Classic | Settings ( Alpha )')
        self.app_window.clear_page(self.app_widget_list)

        main_canvas = self.app_widget.create_canvas(width=1000, height=580, background="#1D313C", highlightthickness=0, pack={"fill": 'both', "expand": True})
        self.app_widget_list.append(main_canvas)

        print('Main Canvas: ', main_canvas)

        self.inner_canvas = self.app_widget.create_canvas(parent_widget=main_canvas, width=955, height=534, background="#1D313C", highlightthickness=2, bd=0, relief='solid', highlightcolor='#FADAC1', place={"relx": 0.5, "rely": 0.5, "anchor": "center"})
        self.app_widget_list.append(self.inner_canvas)

        self.option_canvas = self.app_widget.create_canvas(parent_widget=main_canvas, width=498, height=403, background="#1D313C", highlightthickness=2, bd=0, relief='solid', highlightbackground='#FADAC1', place={"relx": 0.521, "rely": 0.55, "anchor": "center"})


        self.controls.render()


    def handle_inputs(self) -> None:
        pass


class AppearanceSettings:
    def __init__(self, settings: SettingsUI):
        self.settings = settings
        

    def render(self) -> None:
        self.settings.app_window.clear_canvas(self.settings.app_widget_list[1])

        self.settings.app_widget.create_canvas_button(master_canvas=self.settings.inner_canvas, text='Controls', width=159, height=42, x_coordinate=251,
                                                      y_coordinate = 38, command=self.settings.controls.render, background_color='#1D313C', border_color='#FADAC1', text_color='#FADAC1')
        
        self.settings.app_widget.create_canvas_button(master_canvas=self.settings.inner_canvas, text='Sound', width=159, height=42, x_coordinate=590,
                                                      y_coordinate = 38, command=self.settings.sound.render, background_color='#1D313C', border_color='#FADAC1', text_color='#FADAC1')
        
        self.settings.app_widget.create_canvas_button(master_canvas=self.settings.inner_canvas, text='Appearance', width=180, height=42, x_coordinate=410,
                                                      y_coordinate = 38, command=self.settings.appearance.render, background_color='#1D313C', border_color='#F37844', text_color='#F37844')
        
        self.settings.app_widget.create_canvas_keybind_sign(master_canvas=self.settings.inner_canvas, key_bind='B', x_coordinate=890 - 4, y_coordinate=523 - 4,
                                                            image_path=r'assets\keyboard_bindings.png', img_width=22, img_height=22, text='Back', gap=40, font=("SF Pixelate", 10), command=self.settings.previous_page.render)

      
class ControlSettings:
    def __init__(self, settings: SettingsUI):
        self.settings = settings

    def render(self) -> None:
        self.settings.app_window.clear_canvas(self.settings.app_widget_list[1])

        self.settings.app_widget.create_canvas_button(master_canvas = self.settings.inner_canvas, text = 'Appearance', width = 180, height = 42, x_coordinate = 410, 
                                                      y_coordinate = 38, command = self.settings.appearance.render, background_color = '#1D313C', border_color = '#FADAC1', text_color = '#FADAC1')
        
        self.settings.app_widget.create_canvas_button(master_canvas=self.settings.inner_canvas, text='Controls', width=159, height=42, x_coordinate=251,
                                                      y_coordinate = 38, command=self.settings.controls.render, background_color='#1D313C', border_color='#F37844', text_color='#F37844')
        
        self.settings.app_widget.create_canvas_button(master_canvas = self.settings.inner_canvas, text = 'Sound', width = 159, height = 42, x_coordinate = 590, 
                                                      y_coordinate = 38, command = self.settings.sound.render, background_color = '#1D313C', border_color = '#FADAC1', text_color = '#FADAC1')

        self.settings.app_widget.create_canvas_keybind_sign(master_canvas = self.settings.inner_canvas, key_bind='B', x_coordinate=890 - 4, y_coordinate=523 - 4,
                                                            image_path=r'assets\keyboard_bindings.png', img_width=22, img_height=22, text='Back', gap=40, font=("SF Pixelate", 10), command=self.settings.previous_page.render)



class SoundSettings:
    def __init__(self, settings: SettingsUI):
        self.settings = settings


    def render(self) -> None:
        self.settings.app_window.clear_canvas(self.settings.app_widget_list[1])

        self.settings.app_widget.create_canvas_button(master_canvas = self.settings.inner_canvas, text = 'Appearance', width = 180, height = 42, x_coordinate = 410, 
                                                      y_coordinate = 38, command = self.settings.appearance.render, background_color = '#1D313C', border_color = '#FADAC1', text_color = '#FADAC1')
        
        self.settings.app_widget.create_canvas_button(master_canvas=self.settings.inner_canvas, text='Controls', width=159, height=42, x_coordinate=251,
                                                      y_coordinate = 38, command=self.settings.controls.render, background_color='#1D313C', border_color='#FADAC1', text_color='#FADAC1')
        
        self.settings.app_widget.create_canvas_button(master_canvas = self.settings.inner_canvas, text = 'Sound', width = 159, height = 42, x_coordinate = 590, 
                                                      y_coordinate = 38, command = self.settings.sound.render, background_color = '#1D313C', border_color = '#F37844', text_color = '#F37844')

        self.settings.app_widget.create_canvas_keybind_sign(master_canvas=self.settings.inner_canvas, key_bind='B', x_coordinate=890 - 4, y_coordinate=523 - 4,
                                                            image_path=r'assets\keyboard_bindings.png', img_width=22, img_height=22, text='Back', gap=40, font=("SF Pixelate", 10), command = self.settings.previous_page.render)
class SettingsManager:
    def __init__(self):
        pass