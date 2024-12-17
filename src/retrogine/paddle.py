import time
import threading
import tkinter as tk

from typing import List, Tuple, Dict


class InvalidPaddleCoordinates(Exception):
    pass

class MissingPositionData(Exception):
    pass

class PositionExceed(Exception):
    pass

class Paddle:
    """
    The Ping pong classic first paddle 🏓
    """
    def __init__(self, playground: object, position: Tuple[int,int], keys: str, height: float = 30, width:float = 200 ,controlled:str = 'player', color: str = 'yellow') -> None:

        self.height = height
        self.width = width

        self.color = color

        # * Starting position of the paddle 🏓
        self.position = position

        # * Added for customize paddle movement keys ⬆️
        self.keys = keys
        
        # * Controlled by ?
        self.controlled = controlled

        # * Paddle margin between platform width and height
        self.range_margin = 10

        # * Paddle Full Coordinates
        self.coordinates = None
        self.polish_paddle()

        # * PlayGround
        self.playground = playground

        # * Platform
        self.platform = self.playground.platform

        # * Wall 🧱
        self.platform_wall = self.playground.wall

        self.check_paddle()

        self.collision = PaddleCollisionHandler(self)
        self.movement = PaddleMovementHandler(self)

        self.render()

        # * Parallel Threading for movements in a seperate thread
        # self.thread = threading.Thread(target=self.movement.move)
        # self.thread.daemon = True
        # self.thread.start()

       

    def render(self) -> None:
        """
        Render paddle 2d moddel
        """
        for start_bottom, end_bottom, start_top, end_top in self.coordinates:
            self.platform.create_line(start_bottom[0], start_bottom[1], end_bottom[0], end_bottom[1], fill='yellow')
            self.platform.create_line(start_top[0], start_top[1], end_top[0], end_top[1], fill='yellow')


    def check_paddle(self):
        """
        Checks if paddle coordinates is valid
        """
        if not isinstance(self.position, tuple) or len(self.position) != 3:
            raise InvalidPaddleCoordinates(
                f"Position must be a tuple of 3 elements: (x, y, alignment). Got: {self.position}"
            )

        x, y, alignment = self.position

        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise InvalidPaddleCoordinates(
                f"Position coordinates (x, y) must be numeric. Got: x={x}, y={y}"
            )


        # if alignment == 'vertical':
        #     if self. > self.playground.platform_dimension['height'] - range_margin or x < range_margin:
        #         raise PositionExceed(
        #             f' platform height is {self.playground.platform_dimension['height']}. Got: x = {x}'
        #         )


    def polish_paddle(self) -> None:
        """
        Applies full coordinates of the paddle that turns the stick into a full 2d model
        """
        if not isinstance(self.position, tuple) or len(self.position) != 3:
            raise InvalidPaddleCoordinates(
                f"Position must be a tuple of 3 elements: (x, y, alignment). Got: {self.position}"
            )
        x, y, alignment = self.position

        half_width = self.width / 2
        half_height = self.height / 2

        if alignment == 'vertical':
            # * Rotated horizontal Coordinates
            self.coordinates = [
                [
                    # * Top side
                    (x - half_height, y - half_width), (x - half_height, y + half_width),
                    # * Bottom side
                    (x + half_height, y - half_width), (x + half_height, y + half_width)
                ],
                [
                    # * Left side
                    (x - half_height, y + half_width), (x + half_height, y + half_width),
                    # * Right side
                    (x - half_height, y - half_width), (x + half_height, y - half_width)
                ]
            ]

    @property
    def corner_midpoint(self) -> Dict[str, List[Tuple[int, int]]]:
        """
        Gets paddle midpoint
        """

        if self.position[2] == 'vertical':
            # * Upper or top of the vertical paddle
            (x1, y1), (x2, y2) = self.coordinates[1][2], self.coordinates[1][3]

            # * Lower or bottom of the vertical paddle
            (x3, y3), (x4, y4) = self.coordinates[1][0], self.coordinates[1][1]

            right_segment = self.get_midpoint(x1, y1, x2, y2)

            left_segment = self.get_midpoint(x3, y3, x4, y4)

            return {
                'right_segment': right_segment,
                'left_segment': left_segment
            }

        if self.position[2] == 'horizontal':
            pass
    
    def get_midpoint(self, x1, y1, x2, y2) -> List[Tuple[int, int]]:
        midpoint_x = (x1 + x2) / 2

        first_half = [(x1, y1), (midpoint_x, y1)]
        second_half = [(midpoint_x, y2), (x2, y2)]

        return [first_half, second_half]


    def display_movements(self) -> None:
        pass

    def edit_movements(self) -> None:
        pass


class PaddleMovementHandler:
    """
    Enables Paddle Movements base on its alignment 🚦
    """
    def __init__(self, paddle: Paddle):
        self.paddle = paddle

        self.paddle_alignment = self.paddle.position[2]
        
        self.wall_coordinates = self.paddle.platform_wall.coordinates
        
  
    def move(self):
        """
        Start movement of Paddle
        """
        while True:
            self.continue_move()
            time.sleep(0.05)


    def continue_move(self) -> None:
        print(self.wall_coordinates)


    def change_move(self):
        pass
        print("Walls in paddle's direction:", self.wall_in_direction)


class PaddleCollisionHandler:
    def __init__(self, paddle: Paddle):
        self.paddle = paddle

        self.paddle_segments = self.paddle.corner_midpoint

        self.wall_in_direction = []

        self.wall_in_paddle_direction()


    def check_obstacle(self):
        pass


    def check_partial_collision(self, paddle_segments: List[Tuple[int, int]], wall: List[Tuple[int, int]]):
        """
        Detects obstacle that in paddles movemen depends on its alignment
        """
        for segment in paddle_segments:
            (seg_x1, seg_y1), (seg_x2, seg_y2) = segment

            wall_x1, wall_y1, wall_x2, wall_y2 = wall
            
            # print(f'max(0, min({seg_x2}, {wall_x2}) + max({seg_x1}, {wall_x1}))')
            overlap = max(0, min(seg_x2, wall_x2) - max(seg_x1, wall_x1))
            # print('lapping: ', overlap)

            if seg_x1 == wall_x2 or seg_x2 == wall_x1:
                overlap = max(1, overlap)

            if overlap > 0 and seg_y1 >= wall_y1:
                # print(f"Collision Onn segment: {segment}")
                return True

        # print('bruh no collision')
        return False

    def wall_in_paddle_direction(self) -> None:
        
        for wall in self.paddle.playground.wall.coordinates:
            print(wall)

if __name__ == "__main__":
      paddle = Paddle()
      paddle.test_run()

      # TODO:
      # ! Add paddle control customization , this can help for seperate player paddle key handlings
      # ! Add locking