import tkinter as tk

from typing import Callable
from .tk_helpers import OpenImage

from .tk_widget_generator import WidgetGenerator

import gc
import sys

import tkinter as tkr

class WindowGenerator:
    """
    [ Window Generator ]
    --------------------

    Overview:
    
            creates a reused tkinter window and not just window, it can also provide reused tkinter widgets.

    `✅ Methods`:
    ``` 
        set_title(title: str) -> None
        set_size (width: int, height: int) -> None
        set_resize (status: bool) -> None: 
        set_maxsize (width: int, height: int) -> None
        set_icon (icon_path: str) -> None
        set_background_color (color: str) -> None
    ```

    `✨ Special Methods`:
    ```
        widget_generator() -> WidgetGenerator
        run(func: Callable, icon_path: str, window_width: int, window_height: int, window_title:str) -> None:
        exit () -> None
    ```
   
    >>> 📪 Package by: De Castro, Vince Carlo
   
    """
    
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(WindowGenerator, cls).__new__(cls)
            cls.__instance.__root = tkr.Tk()
            cls.__instance.__root.title("Reused Tkinter OwO | Window")
        return cls.__instance

    # __root = tkr.Tk()
    # __root.title("Reused Tkinter OwO | Window") 
    
    @classmethod
    def widget_generator(cls) -> WidgetGenerator:
        """ Make an instance of it and ready to go """
        return WidgetGenerator(cls.__instance.__root)

    @classmethod         
    def set_title(cls,title :str) -> None:
        """ Sets tkinter window title bar """
        cls.__instance.__root.title(title)

    @classmethod
    def set_size(cls,width:int, height:int) -> None:
        """ Sets the tkinter window size by customizing width and height. """
        cls.__instance.__root.geometry(f"{width}x{height}")
    
    @classmethod
    def set_resize(cls, status: bool) -> None:
        """ Sets the tkinter window status into resizable or unresizable."""
        if status:
            cls.__instance.__root.resizable(True,True)
        else:
            cls.__instance.__root.resizable(False,False)
    
    @classmethod
    def set_window_cursor(cls, cursor_path: str) -> None:
        cls.__instance.__root["cursor"] = cursor_path

    @classmethod
    def set_maxsize(cls,width:int, height:int) -> None:
        """ Sets the tkinter window to its limited resizable size. """
        cls.__instance.__root.maxsize(width,height)
    
    @classmethod
    def set_background_color(cls,color: str) -> None:
        """ Sets the tkinter window background color. """
        cls.__instance.__root.configure(background = color)

    
    @classmethod
    def set_icon(cls,icon_path: str) -> None:
        """ change the tkinter iconic feather title window icon into your liked image icon, make sure the path is in .ico format. """
        if icon_path:
            icon = OpenImage(icon_path, image_width = 50, image_height = 50).open_image()
            cls.__instance.__root.iconphoto(True,icon)

    @classmethod
    def exit(cls, widget_list):
        """ It close the tkinter window to stop """
        cls.__instance.clear_page(widget_list)
        cls.__instance.__root.quit()
        cls.__instance.__root.destroy()

    @classmethod
    def clear_page(cls, group_widget_list) -> None:  
        """ 
        it helps prevent the creation of new windows by clearing the entire window page.
        """
        for page in group_widget_list:
            if isinstance(page, tk.Canvas):  # Adjust `tkw.Canvas` to match your canvas class
                page.delete("all")  # Clears all items from the canvas
            page.destroy()  # Destroy the widget#Destroy previous widgets to allow different layout on each p
        group_widget_list.clear()

    @classmethod
    def run(cls,func: Callable = None, icon_path:str = None, cursor_path: str = None, window_width:int = 400, window_height:int = 200, window_title:str = None, resize_status:bool = None) -> None:
        """ It enables tkinter window to run """
        if func:
            func() #This is for pages that needed to showup first when the application open
        cls.__instance.set_resize(resize_status)
        cls.__instance.set_size(window_width,window_height)
        cls.__instance.set_title(window_title)
        cls.__instance.set_icon(icon_path)
        cls.__instance.set_window_cursor(cursor_path)
        cls.__instance.__root.mainloop()

    @classmethod
    def root(cls):
        return cls.__instance.__root

if __name__ == "__main__":
    pass
    

