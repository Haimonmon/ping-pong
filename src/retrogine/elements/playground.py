import random
import threading
import tkinter as tk

from .ball import Ball
from .wall import Wall
from .paddle import Paddle
from .platform import Platform

from typing import List, Tuple, Dict, Callable

# 0D0D0D
class PlayGround:
     """
     Players playground or court 🏓
     """
     def __init__(self, window: tk.Tk, width: int, height: int, color: str = "black", game: object = None) -> None:
          self.window = window

          # * Playground tkinter canvas
          self.master = None

          self.width = width
          self.height = height 

          self.window.geometry(f"{self.width}x{self.height}")
         
          self.__platform_width = None
          self.__platform_height = None

          self.__platform_new_width = None
          self.__platform_new_height = None

          self.platform_padding = None

          # * Map states
          self.color = color
          self.window.configure(background = self.color)

          self.render()

          # * Platform 🎯
          self.__platform = None
          
          # * Walls 🧱
          self.__wall = None
          
          # * Paddles 🏓
          self.__paddles = []

          # * Pong Balls 🔴
          self.__balls = None

          # * Gamemode chosen 💖
          self.game = game

 
     @property
     def platform(self) -> int:
          """
          Returns playground tkinter widget canvas used.
          """
          return self.__platform.canvas
     

     @property
     def wall(self) -> object:
          """
          Returns playground wallings
          """
          return self.__wall
     

     @property
     def paddles(self) -> List[object]:
          """
          Returns a List of Paddle objects
          """
          return self.__paddles
     

     @property
     def platform_dimension(self) -> Dict:
          """
          Returns an object contains the dimension of platform to be played with
          """
          return {
               'width': self.__platform_width, 'height': self.__platform_height,
               'new_width': self.__platform_new_width, 'new_height': self.__platform_new_height
               }
     

     @property
     def kit(self) -> Dict:
          return {
               "platform": self.__platform,
               "wall": self.__wall,
               "paddles": self.__paddles,
               "balls": self.__balls.balls
          }
     

     def add_walls(self, coordinates: List[List[Tuple[int,int]]], color: str = "white", thickness = 20) -> None:
          """
          Adds Walls into the Platoform

          Example coordinates:
          ```python
            create_walls(
               [
                    # * Top Walls
                    [(0, 0), (200, 0)], [(400, 0), (self.__platform_width, 0)],
                    # * Bottom Walls
                    [(0, self.__platform_height), (200, self.__platform_height)], [(400, self.__platform_height), (self.__platform_width, self.__platform_height)],
                    # * Left Walls
                    [(0, 0), (0, 200)], [(0, 500), (0, self.__platform_height)],
                    # * Right Walls
                    [(500, 0), (500, self.__platform_height)]
               ]
          )

          ```
          [ ♻️ Note ]: Walls are only valid for Horizontal and Vertical positions for now.
          """
          if self.__platform_new_width and self.__platform_new_height and self.__platform.responsive:
               coordinate = self.help_adjust(coordinates)
          else:
               coordinate = coordinates

          self.__wall = Wall(coordinate, self, color, thickness, self.__platform.responsive)
               

     def add_pong_ball(self, color: str = "red", speed: float = 4, size: int = 10, num: int = 1) -> None:
          """
          Adds pong ball into the PLatform
          """
          self.__balls = BallManager(self) # * Lmao Balls .... wala nakong maisip na variable names :,D
          self.__balls.add_ball(color, speed, size, num)
     
     
     def add_paddle(self, height: float, width: float,position: Tuple[int, int, str], keys: str, controlled: str) -> None:
          """
          Adds paddle into the Platform

          [ ♻️ Note ]: Vertical paddle will be only available for now
          """
          paddle = Paddle(self, position, keys, height, width, controlled)
          self.__paddles.append(paddle)

     
     def add_platform(self, width: int, height: int, color: str = 'black', padding: int = 100, responsive: bool = False, new_width: int = None, new_height: int = None) -> None:
          """
          Adds the platform where the fun and game round happens 🎯
          """

          platform = Platform(self, width, height, padding, color, responsive, new_width, new_height)

          self.__platform_width = width
          self.__platform_height = height

          self.__platform_new_width = new_width
          self.__platform_new_height = new_height

          self.platform_padding = platform.padding

          self.__platform = platform



     def help_adjust(self, coordinates) -> List:
        new_coordinates: List = []

        scale_width = self.__platform_new_width / self.__platform_width 
        scale_height = self.__platform_new_height / self.__platform_height

        for start, end in coordinates:
            new_start = [self.scale_coordinate(start[0], scale_width), self.scale_coordinate(start[1], scale_height)]
            new_end = [self.scale_coordinate(end[0], scale_width), self.scale_coordinate(end[1], scale_height)]

            new_coordinates.append([new_start, new_end])
        
        return new_coordinates


     def scale_coordinate(self, coordinate: int, scale: float) -> int:
        return int(coordinate * scale)


     def render(self) -> None:
          """
          Displays court designs
          """
          self.master = tk.Canvas(self.window, width=self.__platform_width, height=self.__platform_height, background=self.color, highlightthickness=0, bd=0)
          self.master.pack(fill=tk.BOTH, expand=True)


     def unrender(self) -> None:
          """
          To save memory consumption
          """
          self.__platform.delete("all")


     def config_playground_style(self, **kwargs) -> None:
          self.window.configure(**kwargs)


     def start(self) -> None:
          """
          Let the Party begin 💖🪄
          """
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

          self.__balls = []

     
     @property
     def balls(self) -> None:
          return self.__balls

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
          if len(self.__balls) >= self.MAX_BALL:
               raise MaximumPongBalls(f"Number of Pong Ball Reach Maximum limit of {self.MAX_BALL}. ⚡")

          ball = Ball(self.playground, ball_size, ball_color, ball_speed)
          self.__balls.append(ball)


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

     # * Default wall coordinates for now
     # self.add_walls(
     #      [
     #           # * Top side Walls
     #           [(0, 0),(100,0)], [(400, 0), (self.__platform_width, 0)],
     #           # * Bottom side Walls
     #           [(0, self.__platform_height), (250, self.__platform_height)], [(400, self.__platform_height), (self.__platform_width, self.__platform_height)],
     #           # * Left side Walls
     #           [(0, 0), (0, 150)], [(0, 450), (0, self.__platform_height)],

     #           # * Right side Walls
     #           [(self.__platform_width, 200), (self.__platform_width, 400)],

     #           # * Testing Middle Obstacle
     #           [(200,205), (200,355)],

     #           [(700,205), (700,355)]
     #      ]
     # )
