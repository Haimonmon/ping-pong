import tkinter as tk
from ctypes import windll

from typing import Callable, Literal
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

    key_binds = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(WindowGenerator, cls).__new__(cls)
            cls.__instance.__root = tkr.Tk()
            cls.__instance.__root.minimized = False
            cls.__instance.__root.maximized = False
            cls.__instance.__root.title("Reused Tkinter OwO | Window")
        return cls.__instance

    # __root = tkr.Tk()
    # __root.title("Reused Tkinter OwO | Window")

    @classmethod
    def root(cls) -> tk.Tk:
        return cls.__instance.__root
    
    @classmethod
    def widget_generator(cls) -> WidgetGenerator:
        """ Make an instance of it and ready to go """
        return WidgetGenerator(cls.__instance.__root, cls)


    @classmethod         
    def set_title(cls,title :str) -> None:
        """ Sets tkinter window title bar """
        cls.__instance.__root.title(title)


    @classmethod
    def set_size(cls,width:int, height:int) -> None:
        """ Sets the tkinter window size by customizing width and height. """
        cls.__instance.__root.geometry(f"{width}x{height}+100+100")


    @classmethod
    def customize_title_bar(cls, color:str = "white", window_title: Literal['owo', 'meow', "Tk"] = "Tk", window_title_text_size: int = 10, title_bar_height: int = 30):
        root = cls.__instance.__root

        title_bar = tk.Frame(root, bg = color, relief = 'raised', bd = 0, highlightthickness = 0 , height = title_bar_height)
        title_bar.pack(fill = 'x')
        title_bar.pack_propagate(False)

        # close_button = tk.Button(title_bar, text='  ×  ', command = cls.__instance.__root.destroy() ,bg='#10121f',padx=2,pady=2,font=("calibri", 13),bd=0,fg='white',highlightthickness=0)
        expand_button = tk.Button(title_bar, text=' 🗖 ', command = lambda: cls.__instance._maximize_me(expand_button), bg='#10121f',padx=2,pady=2,bd=0,fg='white',font=("calibri", 13),highlightthickness=0)
        minimize_button = tk.Button(title_bar, text=' 🗕 ',command= lambda: cls.__instance._minimize_me(), bg='#10121f',padx=2,pady=2,bd=0,fg='white',font=("calibri", 13),highlightthickness=0)

        title_bar_title = tk.Label(title_bar, text=window_title, bg = color,bd = 0, fg = 'black' ,font=("Helvetica", window_title_text_size), highlightthickness=0)

        # close_button.pack(side=RIGHT,ipadx=7,ipady=1)
        expand_button.pack(side='right',ipadx=7,ipady=1)
        minimize_button.pack(side='right',ipadx=7,ipady=1)
        title_bar_title.pack(side='left', padx=10)

        cls.__instance.__root.bind("<Map>", cls.__instance._deminimize_me)
    

    @classmethod
    # * 💡 creditz to: https://github.com/Terranova-Python/Tkinter-Menu-Bar/blob/main/main.py#L59
    def _set_appwindow(cls, mainWindow: tk.Tk) -> None:
        GWL_EXSTYLE = -20
        WS_EX_APPWINDOW = 0x00040000
        WS_EX_TOOLWINDOW = 0x00000080
        # Magic
        hwnd = windll.user32.GetParent(mainWindow.winfo_id())
        stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        stylew = stylew & ~WS_EX_TOOLWINDOW
        stylew = stylew | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)

        mainWindow.wm_withdraw()
        mainWindow.after(10, lambda: mainWindow.wm_deiconify())
    

    @classmethod
    # * 💡 creditz fix from: https://stackoverflow.com/questions/63217105/tkinter-overridedirect-minimizing-and-windows-task-bar-issues
    def _minimize_me(cls) -> None:
        # so you can't see the window when is minimized
        cls.__instance.__root.state('withdrawn')
        cls.__instance.__root.overrideredirect(False)
        cls.__instance.__root.state('iconic')
        cls.__instance.__root.minimized = True


    @classmethod
    # * 💡 creditz fix from: https://stackoverflow.com/questions/63217105/tkinter-overridedirect-minimizing-and-windows-task-bar-issues
    def _deminimize_me(cls, event) -> None:
        cls.__instance.__root.focus()
        # so you can see the window when is not minimized
        cls.__instance.__root.overrideredirect(True)
        if cls.__instance.__root.minimized == True:
            cls.__instance.__root.minimized = False


    @classmethod
    def _maximize_me(cls, expand_button: tk.Button) -> None:
        if cls.__instance.__root.maximized == False:  # if the window was not maximized
            cls.__instance.__root.normal_size = cls.__instance.__root.geometry()
            expand_button.config(text=" 🗗 ")
            cls.__instance.__root.geometry(f"{cls.__instance.__root.winfo_screenwidth()}x{
                        cls.__instance.__root.winfo_screenheight()}+0+0")
            cls.__instance.__root.maximized = not cls.__instance.__root.maximized
            # now it's maximized

        else:  # if the window was maximized
            expand_button.config(text=" 🗖 ")
            cls.__instance.__root.geometry(cls.__instance.__root.normal_size)
            cls.__instance.__root.maximized = not cls.__instance.__root.maximized
            # now it is not maximized

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
    def set_cursor(cls, cursor_hidden: bool) -> None:
        """ Hides the cursor for no reason :) """
        if cursor_hidden:
            cls.__instance.__root.config(cursor = 'none')


    @classmethod
    def disable_titlebar(cls) -> None:
        cls.__instance.__root.overrideredirect(True)


    @classmethod
    def exit(cls, widget_list):
        """ It close the tkinter window to stop """
        cls.__instance.clear_page(widget_list)
        cls.__instance.__root.quit()
        cls.__instance.__root.destroy()


    @classmethod
    def clear_page(cls, group_widget_list: list) -> None:  
        """ 
        it helps prevent the creation of new windows by clearing the entire window page.
        """
        group_widget_list.reverse()

        cls.key_binds.clear()

        if isinstance(group_widget_list, list):
            for page in group_widget_list:
                if isinstance(page, tk.Canvas):
                    page.delete("all")  # * Clears all items from the canvas
                page.destroy() # * Destroy previous widgets to allow different layout on each pages
            group_widget_list.clear()
            return


    @classmethod
    def clear_canvas(cls, canvas: tk.Canvas, clear_binds: bool = True) -> None:
        """
        Allow for reuse of canvas 
        """
        if not isinstance(canvas, tk.Canvas):
            return
        
        if clear_binds:
            cls.key_binds.clear()
        
        canvas.delete("all")

    
    @classmethod
    def run(cls,func: Callable = None, icon_path:str = None, cursor_path: str = None, window_width:int = 400, window_height:int = 200, window_title:str = None, resize_status:bool = None, cursor_hidden = False) -> None:
        """ It enables tkinter window to run """
        if func:
            func() # * This is for pages that needed to showup first when the application open

        # if disable_title_bar:
        #     cls.__instance.disable_titlebar()

        cls.__instance.set_cursor(cursor_hidden)
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
   

