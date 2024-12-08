import tkinter as tk

class PlayGround:
    """
    Players playground or court 🏓
    """
    def __init__(self, width: int = 1200, height: int = 550, color: str = "#0D0D0D", window_title = "PongClassic") -> None:
        self.window = tk.Tk()
        self.window.title(window_title)

        self.__width = width
        self.__height = height
        self.window.geometry(f"{self.__width}x{self.__height}")

        # * Map changes
        self.color = color

        self.__canvas = tk.Canvas(self.window, width = self.__width, height = self.__height, background = self.color)
        self.__canvas.pack()
        

    @property
    def canvas(self) -> int:
         """
         Returns playground tkinter widget canvas used.
         """
         return self.__canvas
    

    @property
    def height(self) -> int:
         return self.__height
    

    @property
    def width(self) -> int:
         return self.__width
    
    
    def render(self) -> None:
        pass


    def get_wall_coordinates(self) -> dict:
         """
         Returns wall coordinates
         for using on collision logic on the pong's ball
         """
         return {"top": 0, "left": 0, "bottom": self.__height, "right": self.__width}


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
      playground.test_run()
      print(playground.canvas)
      print("wall coordinates: ", playground.get_wall_coordinates())