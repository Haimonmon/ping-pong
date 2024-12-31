
from .tk_helpers import GeometryManager , ImageFrames 
from typing import Dict , Any, List
from abc import ABC, abstractmethod
from PIL import ImageTk , Image
import tkinter as tk
import pyautogui


class Widget(ABC): #Interface class
    @abstractmethod
    def create(self):
        pass


class CanvasWidget(ABC): #Abstract class
    def create(self):
        pass


class Canvas(CanvasWidget):
    """
    Initialize the tkinter Canvas with a widget arguments

            Args:
                    parent_widget:      (tk.Widget): Parent group widget (tk.Frame, tk.Canvas ,etc...).
                    **kwargs:           (Dict[str,Any]): Additional Attributes for the tkinter canvas.
            Methods:
                    create() -> tk.Canvas: Create and pack the tkinter Canvas.
    """
    def __init__(self,parent_widget: tk.Widget = None, pack = None, place = None, grid = None, **kwargs: Dict[str,Any]) -> None:
        self.__parent_widget = parent_widget
        self.__canvas_attributes = kwargs

        self.pack = pack
        self.grid = grid
        self.place = place
        
    def create(self) -> tk.Canvas:
        """
        Create and pack the tkinter Canvas.

        Returns:
                tk.Canvas: The created canvas widget.
        """
        canvas = tk.Canvas(self.__parent_widget, **self.__canvas_attributes)
        self.type_tkinter(canvas)

        return canvas
    
    def type_tkinter(self, widget) -> None:
        if self.pack is not None:
            widget.pack(self.pack)
        elif self.grid is not None:
            widget.grid(self.grid)
        elif self.place is not None:
            widget.place(self.place)


class CanvasButtonImage(CanvasWidget):
    """ Initialize the tkinter Canvas Buttob Image with a widget arguments

            Args:
                    master_canvas:      (tk.Canvas): button image group widget
                    x_coordinate:       (int): X position of the button image on the canvas
                    y_coordinate:       (int): Y position of the button image on the canvas
                    original_image:     (tk.Image): The image will be displayed on the button, and this can also serve as the unhover state.
                    substitute_image:   (tk.Image | None) : the image will be displayed on the button that is in the hover state.

            Methods:
                        create() -> int:  Creates Canvas own button image.
    """
    def __init__(self,master_canvas: tk.Canvas, x_coordinate: int, y_coordinate: int, original_image: tk.Image, substitute_image: tk.Image | None = None) -> None:
        self.__master_canvas = master_canvas
        self.__x_coordinate = x_coordinate
        self.__y_coordinate = y_coordinate
        self.__original_image = original_image
        self.__substitute_image = substitute_image

        self.__master_canvas.original_image_ref = original_image
        self.__master_canvas.substitute_image_ref = substitute_image

    def create(self) -> int:
        """ Creates Canvas own button image.
        
        Returns:
                int: The ID of created canvas button image in order to use in <button-1> bind command to do a task,
        """        
        button_image = self.__master_canvas.create_image(self.__x_coordinate, self.__y_coordinate, image=self.__original_image)


        if self.__substitute_image is not None:
                self.__master_canvas.tag_bind(button_image,"<Enter>",lambda event,button = button_image: self.button_image_hover(event,button,self.__substitute_image))
                self.__master_canvas.tag_bind(button_image,"<Leave>",lambda event,button = button_image: self.button_image_unhover(event,button,self.__original_image))
        return button_image
    
    def button_image_hover(self,event: tk.Event,  button: int, selected_image: tk.Image) -> None: #!Not Final: Implementing Command Design Pattern
        """ changing image into another image
        that results into a hover state form or selected state form
        """
        self.__master_canvas.itemconfig(button,image = selected_image)
        event.widget["cursor"] = "@assets/Link.cur" #Change mouse cursor into Hand point cursor icon

    def button_image_unhover(self,event: tk.Event ,button: int, unselected_image: tk.Image ) -> None: #!Not Final: Implementing Command Design Pattern
        """ changing image into its original image 
        that results into a unhover state form or unselected state form
        """
        self.__master_canvas.itemconfig(button,image = unselected_image)
        event.widget["cursor"] = "@assets/Alternate.cur" #Change mouse cursor into its original Arrow cursor icon


class CanvasButtonText(CanvasWidget):
    """ Initialize the tkinter Canvas Button Text with a widget arguments

            Args:
                    master_canvas:      (tk.Canvas) :Button text group widget.
                    x_coordinate:       (int) :X position of the button text on the canvas.
                    y_coordinate:       (int) :Y position of the button text on the canvas.
                    original_image:     (tk.Image) :The image will be displayed on the button and this can be also serve as the unhover state .
                    substitute_image:   (tk.Image | None) :The image will be displayed on the button that in the hover state.
                    **kwargs:           (Dict[str,Any]) :An argument where the button text attributes will be applied.

            Methods:
                        create() -> int:  Creates Canvas own button image.
    """
    def __init__(self,master_canvas: tk.Canvas, x_coordinate: int, y_coordinate: int, original_text: str, substitute_text: str, **kwargs: Dict[str,Any]):
        self.__master_canvas = master_canvas
        self.__x_coordinate = x_coordinate
        self.__y_coordinate = y_coordinate
        self.__original_text = original_text
        self.__substitute_text = substitute_text
        self.__buttontext_attributes = kwargs

    def create(self) -> int:
        """ Creates Canvas own button image.
        
        Returns:
                int: The ID of created canvas button image in order to use in <button-1> bind command to do a task.
        """
        button_text = self.__master_canvas.create_text(self.__x_coordinate, self.__y_coordinate, text = self.__original_text,**self.__buttontext_attributes)
      
        x1 , y1 , x2 , y2 = self.__master_canvas.bbox(button_text)
        hitbox = self.__master_canvas.create_rectangle(x1  , y1  , x2  , y2  , outline="",fill="") 

        if self.__substitute_text is not None:
            self.__master_canvas.tag_bind(hitbox,"<Enter>",lambda event,button = button_text: self.button_text_enterhover(event,button,self.__substitute_text))
            self.__master_canvas.tag_bind(hitbox,"<Leave>",lambda event,button = button_text: self.button_text_leavehover(event,button,self.__original_text))
        return hitbox
    
    def button_text_enterhover(self,event: tk.Event, button: int ,substitute_text: str) -> None: #!Not Final: Implementing Command Design Pattern
            """ changing the text into another text
                that results into a hover state form or selected state form
            """
            event.widget["cursor"] = "@assets/Link.cur"
            self.__master_canvas.itemconfig(button,text = f"{substitute_text}")
            self.__master_canvas.after(15,lambda: self.__master_canvas.move(button,0,-3)) 

    def button_text_leavehover(self,event:tk.Event ,button: int ,original_text: str) -> None: #!Not Final: Implementing Command Design Pattern
            """ changing the text into its original text
                that results into a unhover state form or unselected state form
            """
            event.widget["cursor"] = "@assets/Alternate.cur"
            self.__master_canvas.itemconfig(button,text = original_text)
            self.__master_canvas.after(5,lambda: self.__master_canvas.move(button,0,3))


class CanvasBackgroundGIF(CanvasWidget):
    """ Initialize the tkinter Canvas Background GIF with a widget arguments.

            Args:
                    master_canvas:    (tk.Canvas) :background GIF's group widget.
                    img_path:         (str) :image file relative path.
                    root:             (tk.Tk) :tkinter window.

            Methods:
                        create() -> int:  Creates Canvas own Background GIF.
    """
    def __init__(self,master_canvas: tk.Canvas, img_path: str, root: tk.Tk) -> None:
        self.__master_canvas = master_canvas
        self.__img_path = img_path
        self.__root = root
        self.__curent_gif_frame = 0
        self.__animation_status = None
        self.__animation_delay = 100

    def create(self) -> int:
        """ Creates Canvas own background GIF.
        
        Returns:
                int: The ID of created canvas button image.
        """
        self.stop_animation()
        self.gif_frames = self.get_image_frames() #ImageFrames(self.__img_path).get_frame() 
     
        self.gif_image_frame = self.gif_frames[self.__curent_gif_frame]

        
        self.canvas_background_gif_item =  self.__master_canvas.create_image(0, 0, anchor="nw", image = self.gif_image_frame)
        
        self.play_animation() #Allowing Animations to play
        self.animate_gif()

        return self.canvas_background_gif_item

    def get_image_frames(self) -> List[tk.Image]: 
        """ separating a gif into individual images which give a gif's frames similar to a flipbook!
        """
        gif = Image.open(self.__img_path)
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
    
    def animate_gif(self) -> None:  #!Not Final: Implementing Command Design Pattern
        """ perform animations to the gif

            Checks if the animation is enabled and the master canvas exists.
            If so, updates the current GIF frame and schedules the next animation step.
            Otherwise, stops the animation.
        """
        if self.__animation_status is True and self.__master_canvas.winfo_exists():
            self.__curent_gif_frame += 1
            if self.__curent_gif_frame >= len(self.gif_frames):
                self.__curent_gif_frame = 0  # Restart the animation loop

            self.__master_canvas.itemconfig(self.canvas_background_gif_item, image=self.gif_frames[self.__curent_gif_frame])
           
            self.animation_id = self.__root.after(self.__animation_delay, self.animate_gif)
        else:
            self.stop_animation()
            

    def play_animation(self) -> None:  #!Not Final: Implementing Command Design Pattern
        """ enabling gif animation to play
        """
        self.__animation_status = True
        
    def stop_animation(self) -> None:  #!Not Final: Implementing Command Design Pattern
        """ disabling gif animations to play
        """
        if self.__animation_status and self.animation_id is not None:
            self.__root.after_cancel(self.animation_id)
        self.__animation_status = False
        self.animation_id = None


class CanvasJustImage(CanvasWidget):
    def __init__(self, master_canvas: tk.Canvas, x_coordinate: int, y_coordinate: int, image_path: tk.Image):
        self.__master_canvas = master_canvas
        self.__x_coordinate = x_coordinate
        self.__y_coordinate = y_coordinate
        self.__image_path = image_path

        # self.__master_canvas.image_reference = image_path

    
    def create(self) -> tk.Image:
        image = self.__master_canvas.create_image(self.__x_coordinate, self.__y_coordinate, anchor="nw", image=self.__image_path)
        return image


class CanvasImagePopUpHover(CanvasWidget):
    def __init__(self, master_canvas: tk.Canvas, widget: int, x_coordinate: int, y_coordinate: int, image: tk.Image, debug_show = False, parent_widget_canvas: tk.Canvas = None):
        self.__master_canvas = master_canvas

        # * Parent canvas of the widget needed to hover
        self.__parent_widget_canvas = parent_widget_canvas

        # * Widget to Hover
        self.__widget = widget 
        self.__x_coordinate = x_coordinate
        self.__y_coordinate = y_coordinate
        self.__debug_show = debug_show
        self.__image = image

        self.__animation_active = False


    def create(self) -> int:
        image = self.__master_canvas.create_image(self.__x_coordinate, self.__y_coordinate, image=self.__image, state = "hidden")
        
        if not self.__debug_show and not self.__parent_widget_canvas:
            self.__master_canvas.tag_bind(self.__widget,"<Enter>",lambda event, show_image = image: self.widget_hover(event, show_image))
            self.__master_canvas.tag_bind(self.__widget,"<Leave>",lambda event, hide_image = image: self.widget_unhover(event, hide_image))

        elif not self.__debug_show and self.__parent_widget_canvas:
            self.__parent_widget_canvas.tag_bind(self.__widget, "<Enter>",lambda event, show_image = image: self.widget_hover(event, show_image))
            self.__parent_widget_canvas.tag_bind(self.__widget, "<Leave>",lambda event, hide_image = image: self.widget_unhover(event, hide_image))

        return image
    

    def widget_hover(self, event: tk.Event, image: tk.Image) -> None:
        """
        When hovered, the image on its position will be show by unhiding it
        """
        self.__master_canvas.itemconfig(image, state = "normal")
        self.__animation_active = True
        self.animate(image, direction = 1)


    def widget_unhover(self, event: tk.Event, image: tk.Image) -> None:
        """
        When unhovered, the image will hide on its position
        """
        self.__animation_active = False
        self.__master_canvas.itemconfig(image, state = "hidden")


    def animate(self, image: tk.Image, direction: int) -> None:
        """
        Animates the image to go up and down, illustrating the old selection on the 90s gaming ✨
        """
        if not self.__animation_active:
            return
        
          
        if direction == -1: 
            new_y = self.__y_coordinate - 7
        else: 
            new_y = self.__y_coordinate + 5

        self.__master_canvas.coords(image, self.__x_coordinate, new_y)

        
        if direction == -1: 
            next_direction = 1
        else: 
            next_direction = -1

        self.__master_canvas.after(500, self.animate, image, next_direction)


class AutomaticMouseSelector(CanvasWidget):
    def __init__(self, master_canvas: tk.Canvas, coordinates: List, button_navigations: str, hide_cursor: bool = False):
        self.__master_canvas = master_canvas
        self.__coordinates = coordinates
        self.__button_navigations = button_navigations.upper()
        self.__hide_cursor = hide_cursor
        self.__current_index = 0


    def apply(self) -> None:
        if self.__hide_cursor:
            self.__master_canvas.config(cursor = "none")
        
        self.__master_canvas.bind("<Key>", self.handle_keypress)
        self.__master_canvas.focus_set()
    

    def move_cursor_to_coordinates(self, x: int, y: int) -> None:
        canvas_x = self.__master_canvas.winfo_rootx()
        canvas_y = self.__master_canvas.winfo_rooty()

        pyautogui.moveTo(canvas_x + x, canvas_y + y)


    def handle_keypress(self, event: tk.Event) -> None:
        key = event.keysym.upper()

        if key not in self.__button_navigations:
            return
        
        if key == self.__button_navigations[0] or key == self.__button_navigations[1]:
            self.__current_index = max(0, self.__current_index - 1) # * Move on the list of coordinates given on left indexing direction
        elif key == self.__button_navigations[2] or key == self.__button_navigations[3]:
            self.__current_index = min(len(self.__coordinates) - 1, self.__current_index + 1)
        
        x, y = self.__coordinates[self.__current_index]

        self.move_cursor_to_coordinates(x, y)



class CanvasButtonGIF(CanvasWidget):
    def button_gif(self,canvas: tk.Canvas, x: int, y:int ,gif_image: tk.Image): #Soon
        pass