import random
import threading
import tkinter as tk

from .ball import Ball
from .wall import Wall
from .paddle import Paddle

from typing import List, Tuple


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
          self.add_walls(
               [
                    # * Top side Walls
                    [(0, 0),(100,0)], [(400, 0), (self.__width, 0)],
                    # * Bottom side Walls
                    [(0, self.__height), (250, self.__height)], [(400, self.__height), (self.__width, self.__height)],
                    # * Left side Walls
                    [(0, 0), (0, 150)], [(0, 450), (0, self.__height)],
                    # * Right side Walls
                    [(self.__width, 0), (self.__width, self.__height)]
               ]
          )
          
          # * Paddles 🏓
          self.__paddles = None

          # * Pong Balls 🔴
          self.__balls = None

 
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
     

     @property
     def platform_dimension(self) -> dict:
          """
          Returns an object contains the dimension of platform to be played with
          """
          return {'width': self.__width, 'height': self.__height}
     

     def add_walls(self, coordinates: List[List[Tuple[int,int]]]) -> None:
          """
          Adds the platform Walls on the given playground

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
               

     def add_pong_ball(self, color: str = "red", speed: float = 4, size: int = 10, num: int = 1) -> None:
          """
          Adds pong ball on the PLayground
          """
          self.balls = BallManager(self)
          self.balls.add_ball(color, speed, size, num)
     
     
     def add_paddle(self) -> None:
          """
          Adds paddle on the PLayground
          """
          pass

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


class MaximumPongBalls(Exception):
     pass

class BallManager:
     """
     Manages Ball on the Playground by: Creating, Customize
     """
     def __init__(self, playground: PlayGround):
          self.playground = playground

          self.MAX_BALL = 10

          self.balls = []


     def add_ball(self, color, speed, size, num) -> None:
          if (color == 'random'):
               ball_color = self.color_randomizer()
          else:
               ball_color = color

          if (size == 'random'):
               ball_size = self.size_randomizer()
          else:
               ball_size = size

          if (speed == 'random'):
               ball_speed = self.speed_randomizer()
          else:
               ball_speed = speed
          
          for _ in range(num):
               self.create_ball(ball_size, ball_color, ball_speed)
          
          print(f'Successfully added {num} balls 🏓')

     
     def create_ball(self, ball_size, ball_color, ball_speed) -> None:
          """
          Creates Ball Object on the Playground
          """
          if len(self.balls) >= self.MAX_BALL:
               raise MaximumPongBalls(f"Number of Pong Ball Reach Maximum limit of {self.MAX_BALL}. ⚡")

          ball = Ball(self.playground, ball_size, ball_color, ball_speed)
          self.balls.append(ball)


     def color_randomizer(self) -> str:
          colors = ['red', 'blue', 'green', 'yellow', 'purple']
          return random.choice(colors)

     def size_randomizer(self) -> int:
          return random.randint(8, 20)  

     def speed_randomizer(self) -> float:
          return random.uniform(2.0, 6.0)


class PaddleManager:
     def __init__(self, playground: PlayGround):
          self.playground = playground

if __name__ == "__main__":
     playground = PlayGround()
     #  playground.test_run()
     #  print(playground.canvas)
     #  print("wall coordinates: ", playground.get_wall_coordinates())


     # TODO:
     # ! Add customizable wall coordinates for DIY maps in the future
     # ! Possible add lockings