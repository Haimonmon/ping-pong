import time
import threading
import tkinter as tk

from typing import List, Tuple


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
        self.wall_in_direction = []

        # * Paddle wall in direction
        self.wall_in_paddle_direction()

        

    def move(self):
        while True:
            self.continue_move()
            time.sleep(0.05)

    def continue_move(self) -> None:
        print(self.wall_coordinates)

    def change_move(self):
        pass

    def wall_in_paddle_direction(self) -> None:
        """
        Detects obstacle that in paddles movemen depends on its alignment
        """

        range = 10


        if self.paddle_alignment == 'vertical':
            paddle_left_pos = (self.paddle.coordinates[1][0], self.paddle.coordinates[1][1])
            paddle_right_pos = (self.paddle.coordinates[1][2], self.paddle.coordinates[1][3])

            for wall in self.wall_coordinates:
                bottom_side: Tuple = wall[0], wall[1]  
                top_side: Tuple = wall[2], wall[3]
                
                horizontal_wall = bottom_side[0][1] == bottom_side[1][1] or top_side[0][1] == top_side[1][1]

                if horizontal_wall:
                    find = False
                    up = 0
                    down = 0
                    while not find:
                        # print(paddle_right_pos[0][1] + up)
                        left_up = (
                            paddle_right_pos[0][0] <= top_side[1][0] and
                            top_side[0][0] <= paddle_right_pos[1][0] and
                            paddle_right_pos[0][1] + up == top_side[0][1]
                        )

                        # right_collision = (
                        #     top_side[1][1] >= (paddle_right_pos[1][1] - down) >= bottom_side[0][1]
                        #     and paddle_right_pos[0][0] == bottom_side[0][0]
                        # )
                        
                        # print(f'{paddle_right_pos[0][1] + up} == {top_side[0][1]}',left_up)

                        if left_up:
                            print()
                            print(f'{paddle_right_pos[0][0]} >= {top_side[1][0]} and \n{top_side[0][0]} <= { paddle_right_pos[1][0]} and \n{paddle_right_pos[0][1] + up} == {top_side[0][1]}')
                            print(top_side)
                            print()
                            self.wall_in_direction.append(wall)
                            find = True
                            break

                        if paddle_left_pos[0][1] + up <= 0:
                            find = False
                            break

                        up -=1
                        down +=1


        

        if self.paddle_alignment == 'horizontal':
            pass
        
        print()
        print('finded wall in collision:', self.wall_in_direction)


class PaddleCollisionHandler:
    def __init__(self, paddle: Paddle):
        self.paddle = paddle

    def check_obstacle(self):
        pass

    def check_ball_collision(self):
        pass


if __name__ == "__main__":
      paddle = Paddle()
      paddle.test_run()

      # TODO:
      # ! Add paddle render
      # ! Add paddle control customization , this can help for seperate player paddle key handlings
      # ! Add locking and threading