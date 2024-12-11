import tkinter as tk

class WallSegmentError(Exception):
     pass

class InvalidCoordinates(Exception):
     pass

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
          self.__wall_thickness = wall_thickness

          # * Default map wall coordinates
          self.wall_coordinates_segments = {
              "top": [(0, 0), (200, 0), (400, 0), (self.__width, 0), (600,0)],
              "bottom": [(0, self.__height), (200, self.__height), (400, self.__height), (self.__width, self.__height)],
              "left": [(0, 0), (0, 200), (0, 500), (0, self.__height)],
              "right": [(500, 0), (500, self.__height)]}
          
          self.check_wall_segments()

          self.__canvas = tk.Canvas(self.window, width = self.__width, height = self.__height, background = self.color)
          self.__canvas.pack()
          
          self.paddles = []

 
     @property
     def canvas(self) -> int:
          """
          Returns playground tkinter widget canvas used.
          """
          return self.__canvas
    

     @property
     def wall_thickness(self) -> int:
          return self.__wall_thickness
    

     @property
     def wall_coordinates(self) -> dict:
         """
         Returns wall coordinates
         for using on collision logic on the pong's ball
         """
         return {"top": 0, "left": 0, "bottom": self.__height, "right": self.__width}
     

     def check_wall_segments(self, wall_coordinates: int = None) -> bool:
          """
          Checks if wall coordinates given are valid
          """
          for wall_side, coordinates in self.wall_coordinates_segments.items():

               if (len(coordinates) % 2 == 1):
                    raise InvalidCoordinates(f'Coordinates on {wall_side} side needs a partner for ending and starting point. Invalid: {coordinates}')
               
               for i in range(0, len(coordinates) - 1, 2):

                    starting_wall = coordinates[i]
                    ending_wall = coordinates[i + 1]

                    is_starting_wall_exceeds = any(coord > limit or coord < 0 for coord, limit in zip(starting_wall, (self.__width, self.__height)))
                    is_ending_wall_exceeds = any(coord > limit or coord < 0 for coord, limit in zip(ending_wall, (self.__width, self.__height)))

                    if is_starting_wall_exceeds or is_ending_wall_exceeds:
                         raise WallSegmentError(
                              f"Invalid wall coordinates on the '{wall_side}' side: {coordinates}. "
                              f"Coordinates exceed the bounds (width={self.__width}, height={self.__height})."
                         )
                         
               print()
               return True

     def change_default_map(self) -> None:
          """
          For customization of maps or DIY maps, just need coordinates of each obstacles
          """
          pass
     

     def render(self) -> None:
          """
          Displays court designs
          """
          pass


     def unrender(self) -> None:
          """
          To save memory consumption
          """
          self.__canvas.delete("all")


     def test_run(self) -> None:
          print('Welcome to the Ping pong\'s PlayGround')
          self.window.mainloop()


if __name__ == "__main__":
      playground = PlayGround()
     #  playground.test_run()
     #  print(playground.canvas)
     #  print("wall coordinates: ", playground.get_wall_coordinates())