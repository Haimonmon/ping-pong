from .tk_helpers import GeometryManager as geometry
from abc import ABC , abstractmethod
from typing import Dict , Any

import tkinter as tk

class Widget(ABC):
    @abstractmethod
    def create(self):
        pass

class Frame(Widget):
    def __init__(self, parent_widget: tk.Widget | None = None, geometry_type: str = None, geometry_attributes: Dict[str,Any] = None,**kwargs: Dict[str,Any]) -> None:
        self.__parent_widget = parent_widget
        self.__frame_attributes = kwargs
        self.__geometry_type = geometry_type
        self.__geometry_attributes = geometry_attributes

    def create(self) -> tk.Frame:
        """ Create and pack the tkinter Frame.

        Returns:
                tk.Frame: The created tkinter Frame widget.
        """
        frame = tk.Frame(self.__parent_widget, **self.__frame_attributes)
        geometry(frame,self.__geometry_type,self.__geometry_attributes).set_geometry()
        return frame
    
class FrameLabel(Widget):
    def __init__(self, master: tk.Widget = None, **kwargs: Dict[str,Any]) -> None:
        self.__frame = master
        self.__label_attributes = kwargs
     
    def create(self) -> tk.Label:
        """ Create and pack the tkinter Label.

        Returns:
                tk.Label: The created tkinter Frame Label widget.
        """
        label = tk.Label(self.__frame, **self.__label_attributes)
        geometry(label,"pack")
        return label

class FrameButton(Widget):
    def __init__(self, frame: tk.Frame, **kwargs: Dict[str,Any]):
        self.__frame = frame
        self.__button_attributes = kwargs

    def create(self) -> tk.Button:
        """ Create and packs the tkinter Button.

        Returns:
                tk.Button: The created tkinter Frame Button widget.
        """
        button = tk.Button(self.__frame, **self.__button_attributes) #It can be use by Lambda
        geometry(button, "pack")
        return button

class FrameImage(Widget):
    def __init__(self, frame: tk.Frame, image_path: str, **kwargs):
        self.__frame = frame
        self.__image_path = image_path
        self.__image_label_attributes = kwargs

    def create(self) -> tk.Label:
        """ Create and packs the tkinter Label.

        `Returns`:
                tk.Label: The created `tkinter Label widget that have an attribute of image`.
        """
        photo_label = tk.Label(self.__frame, image = self.__image_path, **self.__image_label_attributes)
        geometry(photo_label, "pack")
        return photo_label

class FrameEntry(Widget):
    def __init__(self, frame: tk.Frame ,**kwargs: Dict[str,Any]):
        self.__frame = frame
        self.__entry_attributes = kwargs

    def create(self) -> tk.Entry:
        """ `Create and packs the tkinter Entry.`

        Returns:
                tk.Entry: The created `tkinter Entry widget`.
        """
        entry = tk.Entry(self.__frame, **self.__entry_attributes)
        geometry(entry, "pack")
        return entry