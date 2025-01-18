""" 
Widget Generator
------ ---------

Provides an  organized reusable tkinter widgets 
"""

from .canvas_widgets import *
from .frame_widgets import *

from typing import Dict , Any , List, Callable
from .tk_helpers import OpenImage


class NavigationsReachedMaximum(Exception):
    pass


class WidgetGenerator:
    """
    A Factory Class that creates different tkinter widgets using Factory Design pattern.
    """

    def __init__(self, root: tk.Tk, main) -> None: 
        self.__root = root

        self.__main = main

        self.__photo_reference = []
      
        
    def clear_page(self, group_widget_list: List) -> None:  #!Not Final: Implementing Command Design Pattern
        """ 
        it helps prevent the creation of new windows by clearing the entire window page.
        """ 
        for page in group_widget_list:
            page.delete("all") #Deleting widgets in canvas
            page.destroy() #Destroy previous widgets to allow different layout on each page
        self.__canvas_widget.stop_animation()
        group_widget_list.clear()

#*---------------------------------------------------------------------------------------Frame Section---------------------------------------------------------------------------------------*#
    def create_frame(self, **frame_attributes: Dict[str,Any]) -> tk.Frame:
        """
        creates tkinter group widget Frame
        """
        return self.__frame_widget.frame(**frame_attributes)


    def create_frame_label(self,frame: tk.Frame, **widget_attributes: Dict[str,Any]) -> tk.Label:
        """
        creates label where you can display texts
        """
        return self.__frame_widget.label(frame, **widget_attributes)
    

    def create_frame_label_image(self,frame: tk.Frame, image_path: str, image_width: int = None, image_height: int = None, **image_label_attributes: Dict[str,Any]) -> tk.Label:
        """
        creates a label that use to display pyimage
        """
        image = self.open_image(image_path, image_width, image_height)
        return self.__frame_widget.image(frame, image, **image_label_attributes)
    

    def create_frame_entry(self, frame: tk.Frame, **entry_attributes: Dict[str,Any]) -> tk.Entry:
        """
        creates a tkinter entry that uses to type or insert user texts
        """
        return self.__frame_widget.entry(frame, **entry_attributes)
    

    def create_frame_button(self, frame: tk.Frame, **button_attributes: Dict[str,Any]) -> tk.Button:
        """
        creates a tkinter button that can perform a command todo a task
        """
        return self.__frame_widget.button(frame, **button_attributes)


#*---------------------------------------------------------------------------------------Canvas Section---------------------------------------------------------------------------------------*#
    @staticmethod
    def create_canvas(parent_widget = None, pack=None, grid=None, place=None, **canvas_attributes: Dict[str, Any]) -> Canvas:
        """ 
        creates reusable tkinter group widget Canvas 
        """
        canvas = Canvas(parent_widget, pack, place, grid, **canvas_attributes).create()
        return canvas
        
    @staticmethod
    def create_canvas_button_text(canvas: tk.Canvas , x: int ,y: int,orig_text: str, sub_text: str = None, **text_button_attributes: Dict[str,Any]) -> int:
        """
        creates a canvas button but in text format, by use of <button-1> bind

        it will allow the button text to perform a command to do a task

        *Note: you can put a sub_text by putting another text that enables an hover effect

        Example:

        orig_text = hello world! :unhover state

        sub_text = hello world! << :hover state
        """
        button_text = CanvasButtonText(canvas, x, y, orig_text, sub_text, **text_button_attributes).create()
        return button_text
    

    def create_canvas_button_image(self, canvas: tk.Canvas, x: int, y: int, orig_image: str, sub_image: str = None,img_width: int = None, img_height: int = None) -> int:
        """ creates a canvas button but in pyimage format, by use of <button-1> bind
            it will allow the button image to perform a command to do a task

            *Note: you can put a sub_image argument to put another image_path that enables an hover effect

            Example:

            orig_image = sadly_face.jpg :unhover state

            sub_image = happy_face.jpg :hover state
        """
        original_image = OpenImage(orig_image,image_width=img_width,image_height=img_height).open_image()
        substitute_image = OpenImage(sub_image,image_width=img_width,image_height=img_height).open_image()

        button_image = CanvasButtonImage(canvas, x, y, original_image, substitute_image).create()
        return button_image
      

    def create_canvas_background_gif(self, canvas: tk.Canvas, img_path: str) -> int:
        """
        creates an animated background GIF image
        """
        background_gif = CanvasBackgroundGIF(canvas, img_path,self.__root).create()
        return background_gif
        

    def create_canvas_button_gif(self,canvas: tk.Canvas) -> None:
        """
        creates a button but in pyimage GIF format

        !Note: the function is still on its development
        """
        pass


    def create_canvas_image(self, canvas: tk.Canvas, x:int, y:int, orig_image: str, img_width: int = None, img_height: int = None) -> tk.Image:
        """
        Just Creates an image for the given canvas
        """
        original_image = OpenImage(orig_image,image_width=img_width,image_height=img_height).open_image()

        self.__photo_reference.append(original_image)


        image = CanvasJustImage(canvas, x, y, original_image).create()

        return image
    

    def create_canvas_image_popper(self, canvas: tk.Canvas, widget_to_hover: int, x: int, y: int, image_path: str, img_width: int, img_height: int, debug_show = False, widget_canvas = None, page = None, text = None) -> int:
        """
        No need to worry if the widget needed to hover is on different canvas

        just put the parent canvas of the widget needed to hover on the `widget_canvas`

        `canvas` is needed for where canvas the image gonna show
        """
        image = OpenImage(image_path, image_width= img_width, image_height=img_height).open_image()

        self.__photo_reference.append(image)

        image_popper = CanvasImagePopUpHover(canvas, widget_to_hover, x, y, image, debug_show, parent_widget_canvas = widget_canvas, page = page , text = text).create()

        return image_popper
    

    def apply_canvas_cursor_auto_move(self, canvas: tk.Canvas, point_coordinates: List, navigations: str, cursor_hidden: bool = False, avail_work_navs = None) -> None:
        """
        Movement coordinates consist of a tuple with a pair element of x and y coordinates

        in order to control the mouse movement , give button navigations in maximum of 4 keyboard bindings for example "WASD"

        "WA" will go to the left indexing of the movement coordinates
        "SD" will go to the right indexing of the movement cooridnates
        """

        if len(navigations) > 4:
            raise NavigationsReachedMaximum("I Only need 4 navs")
        
        AutomaticMouseSelector(master_canvas = canvas, coordinates = point_coordinates, button_navigations = navigations, hide_cursor = cursor_hidden, avail_working_nav=avail_work_navs).apply()


    def create_canvas_button(self,  master_canvas: tk.Canvas, text: str, width: int, height: int, x_coordinate: int, y_coordinate: int, command: Callable = None, background_color: str = 'gray', border_color='white', text_color: str = 'black') -> None:
        """
        Creates a canvas own button
        """
        CanvasButton(master_canvas, text, width, height, x_coordinate, y_coordinate, command, background_color, border_color, text_color).create()


    def create_canvas_keybind_sign(self, master_canvas: tk.Canvas, key_bind: str, x_coordinate: int, y_coordinate: int, image_path: tk.Image, img_width: int, img_height: int, text: str, gap=None, font=None, command = None) -> None:
        
        image =  OpenImage(image_path, image_width = img_width, image_height=img_height).open_image()

        self.__main.key_binds[key_bind] = command

        key_bind_text = key_bind

        CanvasKeybindButton(master_canvas, x_coordinate, y_coordinate, image_path = image, width = img_width, height = img_height, text = text,gap = gap, font = font, key_binds = self.__main.key_binds, key_bind_text = key_bind_text).create()


    def create_canvas_popper(self,master, x_coordinate: float = 0.5, y_coordinate: float = 0.5, apply_overlay: bool = True, **canvas_attributes: Dict) -> CanvasCanvasPopper:
        """ Creates a menu popper """
        canvas = CanvasCanvasPopper(master_canvas= master, x_pos = x_coordinate, y_pos = y_coordinate, apply_overlay = apply_overlay, **canvas_attributes).create()

        return canvas

if __name__ == "__main__":
    widget = WidgetGenerator(tk.Tk())
    widget.create_frame()