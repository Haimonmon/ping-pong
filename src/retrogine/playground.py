import tkinter as tk

from typing import List, Tuple
from .wall import Wall

class PlayGround:
     """
     Players playground or court 🏓
     """
     def __init__(self, width: int = 500, height: int = 600, color: str = "#0D0D0D", window_title: str = "PongClassic", wall_thickness: int = 20) -> None:
          self.window = tk.Tk()
          self.window.title(window_title)

          self.__width = width
          self.__height = height
          self.window.geometry(f"{self.__width}x{self.__height}")
         

          # * Map states
          self.color = color
          self.window.configure(background = self.color)
          self.__wall_thickness = wall_thickness

          self.__platform = None
          self.render() 

          # * Walls 🧱
          self.__wall = None

          # * Default wall coordinates for now
          self.create_walls(
               [
                    # * Top side Walls
                    [(0, 0),(100,0)], [(400, 0), (self.__width, 0)],
                    # * Bottom side Walls
                    [(0, self.__height), (100, self.__height)], [(400, self.__height), (self.__width, self.__height)],
                    # * Left side Walls
                    [(0, 0), (0, 150)], [(0, 450), (0, self.__height)],
                    # * Right side Walls
                    [(self.__width, 0), (self.__width, self.__height)]
               ]
          )
          
          # * Paddles 🏓
          self.__paddles = []

 
     @property
     def platform(self) -> int:
          """
          Returns playground tkinter widget canvas used.
          """
          return self.__platform
    

     @property
     def wall(self) -> object:
          """
          Returns playground wallings
          """
          return self.__wall
     

     @property
     def paddles(self) -> List:
          """
          Returns a List of Paddle objects
          """
          return self.__paddles
     

     def create_walls(self, coordinates: List[List[Tuple[int,int]]]) -> None:
          """
          Creates the platform Walls and set it as an Object

          Example coordinates:
          ```python
            create_walls(
               [
                    # * Top Walls
                    [(0, 0), (200, 0)], [(400, 0), (self.__width, 0)],
                    # * Bottom Walls
                    [(0, self.__height), (200, self.__height)], [(400, self.__height), (self.__width, self.__height)],
                    # * Left Walls
                    [(0, 0), (0, 200)], [(0, 500), (0, self.__height)],
                    # * Right Walls
                    [(500, 0), (500, self.__height)]
               ]
          )

          ```
          [ ♻️ Note ]: Walls are only valid for Horizontal and Vertical positions for now.
          """
          self.__wall = Wall(coordinates, self.__wall_thickness, self.__platform, self.__width, self.__height)
               

     def render(self) -> None:
          """
          Displays court designs
          """
          self.__platform = tk.Canvas(self.window, width=self.__width, height=self.__height, background=self.color, highlightthickness=0, bd=0)
          self.__platform.pack()


     def unrender(self) -> None:
          """
          To save memory consumption
          """
          self.__platform.delete("all")


     def config_playground_style(self, **kwargs) -> None:
          self.window.configure(**kwargs)


     def test_run(self) -> None:
          print('Welcome to the Ping pong\'s PlayGround')
          self.window.mainloop()


if __name__ == "__main__":
     playground = PlayGround()
     #  playground.test_run()
     #  print(playground.canvas)
     #  print("wall coordinates: ", playground.get_wall_coordinates())


     # TODO:
     # ! Add customizable wall coordinates for DIY maps in the future
     # ! Possible add lockings