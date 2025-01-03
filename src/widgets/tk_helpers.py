"""
button_image_hover() -> None:  Button Image hover state effects turning its image to its assigned substitute image 
                        button_image_unhover() -> None:  Button Image unhover state effects returning its image to its original image
"""
from typing import Dict, Any, List
from PIL import Image, ImageTk
from abc import ABC, abstractmethod

import tkinter as tk

class ImageFrames:
    def __init__(self, image_path):
        self.__image_path = image_path
        

    def get_image_frames(self) -> List[tk.Image]: 
        """ separating a gif into individual images which give a gif's frames similar to a flipbook!
        """
        gif = Image.open(self.__image_path)
        frames = []
        try:
            while True:
                resized_gif = gif.resize((395, 658))
                frame = ImageTk.PhotoImage(resized_gif)
                frames.append(frame)
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass
        return frames
    
    def get_frame(self):
        frames = self.get_image_frames()
        return frames
    
class OpenImage:
  def __init__(self, image_path: str, image_width:int = None, image_height:int = None):
      self.__image_path = image_path
      self.__image_width = image_width
      self.__image_hieght = image_height

      self.__photo_reference = []

  def open_image(self) -> tk.PhotoImage: 
        """ make the image path to a portable pyimage for tkinter uses

        ?Note: Soon this function will support animated GIF's 
        """
        try:
            original_image = Image.open(self.__image_path)
            if self.__image_width is not None and self.__image_hieght is not None:
                changed_image_size = original_image.resize((self.__image_width,self.__image_hieght))
                image = ImageTk.PhotoImage(changed_image_size)
            else:
                unchange_image_size = original_image
                image = ImageTk.PhotoImage(unchange_image_size)
            
            self.__photo_reference.append(image)

            return image
        except FileNotFoundError as error:
            print(f"File {error} is not Existed")
        except AttributeError as error:
            print(f"! Invalid Attribute {error}")


class GeometryManager():  
    """
    Initialize the GeometryManager with a widget, geometry type, and optional attributes.
        
            `Args`:
            ```
                widget:          (tk.Widget)  :The Tkinter widget to manage.
                geometry_type:   (str)  :must be in a string format ('pack', 'grid', or 'place').
                **kwargs:        (Dict[str, Any])  :Additional attributes for the geometry manager.
            ```
            `Methods`:
            ```
                set_geometry() -> None:  Sets the geometry manager for widget.
                pack() -> None: set the widget geometry using pack manager
                grid() -> None: set the widget geometry using grid manager
                place() -> None: set the widget geometry using place manager
            ```
    """
    def __init__(self,widget: tk.Widget, geometry_type: str , geometry_attrbutes = None) -> None:
        self.widget = widget
        self.geometry_type = geometry_type
        self.geometry_attributes = geometry_attrbutes
        self.geometry_managers = {"pack": self.pack,
                                  "grid": self.grid,
                                  "place": self.place
                                  }
       
    def set_geometry(self) -> None:
        """
        Sets the geometry manager for widget.
        """
        if not isinstance(self.geometry_type,str):
            raise TypeError("\n Your Geometry type must be string")
        
        if self.geometry_type not in self.geometry_managers:
            raise ValueError("\n Unsupported layout type: {self.geometry_type}")
        
        self.geometry_managers[self.geometry_type]()
    
    def pack(self) -> None:
        """ set the widget geometry using pack manager """
        self.widget.pack(**self.geometry_attributes)

    def grid(self) -> None:
        """ set the widget geometry using grid manager """
        self.widget.grid(**self.geometry_attributes)

    def place(self) -> None:
        """ set the widget geometry using place manager """
        self.widget.place(**self.geometry_attributes)
    

class ControlHelpers:
    def __init__(self):
        pass
    


