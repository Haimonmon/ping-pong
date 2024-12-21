import time
import random
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

        # * Controlled by ?
        self.controlled = controlled

        # * Paddle locking 🏓🔒
        self.lock = threading.Lock()

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

        # * Added for customize paddle movement keys ⬆️
        self.keys = f'{keys[0].lower()}{keys[1].lower()}'

        self.check_paddle()

        self.collision = PaddleCollisionHandler(self)
        self.movement = PaddleMovementHandler(self)

        self.rendered_lines = []

        self.render()

        # * Parallel Threading for movements in a seperate thread
        self.thread = threading.Thread(target=self.movement.paddle_movement)
        self.thread.daemon = True
        self.thread.start()

       

    def render(self) -> None:
        """
        Render paddle 2d moddel
        """
       
        for start_bottom, end_bottom, start_top, end_top in self.coordinates:
            bottom_line: tk.Canvas = self.platform.create_line(start_bottom[0], start_bottom[1], end_bottom[0], end_bottom[1], fill='yellow')
            top_line: tk.Canvas = self.platform.create_line(start_top[0], start_top[1], end_top[0], end_top[1], fill='yellow')

            # * Can be used for later movements of paddle
            self.rendered_lines.append(bottom_line)
            self.rendered_lines.append(top_line)

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

        self.paddle_direction = self.paddle.keys[random.choice([0,1])]

        self.paddle.playground.window.bind(self.paddle.keys[0], self.change_direction)
        self.paddle.playground.window.bind(self.paddle.keys[1], self.change_direction)

        self.run = True

  
    def paddle_movement(self):
        """
        Start movement of Paddle
        """
        while self.run:
            self.continue_move()
            time.sleep(0.01)


    def continue_move(self) -> None:
        """
        Movements for the paddle will be apply base on the position direction both of its side
        """
        is_paddle_horizontal = self.paddle.position[2] == 'horizontal'
        is_paddle_vertical = self.paddle.position[2] == 'vertical'


        if is_paddle_vertical:
            self.move_vertical()

        if is_paddle_horizontal:
            pass


    def change_direction(self, event):
        """
        Change the paddle's movement direction based on given or customized keypress 🚥
        """

        if event.keysym.lower() == self.paddle.keys[0].lower():  
            self.paddle_direction = self.paddle.keys[0]

        
        elif event.keysym.lower() == self.paddle.keys[1].lower():  
            self.paddle_direction = self.paddle.keys[1]



    def move_vertical(self) -> None:
        """
        Goes ⬆️ Ups and Downs ⬇️
        """

        with self.paddle.lock:
            x, y, alignment = self.paddle.position

            side1_stop_range = self.paddle.collision.side1_stop_range
            side2_stop_range = self.paddle.collision.side2_stop_range

            if self.paddle.controlled == 'player' and self.paddle_direction == self.paddle.keys[0]:
                if y > side1_stop_range[2]:
                    y -= 2.5
                else:
                    y = side1_stop_range[2]
                
            if self.paddle.controlled == 'player' and self.paddle_direction == self.paddle.keys[1]:
                if y < side2_stop_range[2]:
                    y += 2.5
                else:
                    y = side2_stop_range[2]
                
        self.update_paddle(x, y, alignment, y - self.paddle.position[1])

    
    def update_paddle(self, x: float, y: float, alignment: str, dy: float) -> None:
        """
        Update paddle coordinates
        """
        with self.paddle.lock:
            for line in self.paddle.rendered_lines:
                self.paddle.platform.move(line, 0, dy)

            self.paddle.position = (x, y, alignment)

            self.paddle.polish_paddle()  # * This will update the coordinates after movement occur 



class PaddleCollisionHandler:
    def __init__(self, paddle: Paddle):
        self.paddle = paddle

        self.paddle_segments = self.paddle.corner_midpoint

        self.wall_in_direction = []

        self.side1_stop_range = None

        self.side2_stop_range = None

        self.wall_in_paddle_direction()


    def check_obstacle(self):
        pass

    def vertical_partial_collision(self, paddle_segments: List[Tuple[int, int]], wall1: List[Tuple[int, int]], wall2: List[Tuple[int, int]], direction: str):
        """
        Detects obstacle that in paddles movemen depends on its alignment
        """
        gap = 2

        # print(direction)
      
        for segment in paddle_segments:
            (seg_x1, seg_y1), (seg_x2, seg_y2) = segment

            wall1_x1, wall1_y1 = wall1[0]
            wall1_x2, wall1_y2 = wall1[1]
            
            overlap = max(0, min(seg_x2, wall1_x2) - max(seg_x1 - gap, wall1_x1))

            if seg_x1 - gap == wall1_x2 or seg_x2 == wall1_x1:
                overlap = max(1, overlap)

            
            if direction == 'top':
                # * Upper part of the vertical paddle
                if overlap > 0 and (seg_y1 >= wall1_y1 or wall2[0][1] <= seg_y1 <= wall1_y1):
                    if wall2[0][1] <= seg_y1 <= wall1_y1:
                        self.side1_stop_range: Tuple = (seg_x1, seg_x2, (seg_y2) + (self.paddle.width // 2))
                        return
                    
                    if self.side1_stop_range is None or seg_y1 >= self.side1_stop_range[2]:
                        self.side1_stop_range: Tuple = (seg_x1, seg_x2, (wall1_y1 + 10) + (self.paddle.width // 2))
                        return
                    
                   
            if direction == 'down':
                # * Lower part of the vertical paddle
                if overlap > 0 and (seg_y1 <= wall1_y1 or wall2[0][1] >= seg_y1 >= wall1_y1):
                    
                    if wall2[0][1] >= seg_y1 >= wall1_y1:
                        self.side2_stop_range: Tuple = (seg_x1, seg_x2, (seg_y2) - (self.paddle.width // 2))
                        return
                    
                    if self.side2_stop_range is None or seg_y1 <= self.side2_stop_range[2]:
                        self.side2_stop_range: Tuple = (seg_x1, seg_x2, (wall1_y1 - 10) - (self.paddle.width // 2))
                        return
        

    def wall_in_paddle_direction(self) -> None:
        with self.paddle.lock:
            for wall in self.paddle.playground.wall.coordinates:
                bottom_side: Tuple = wall[0], wall[1]  
                top_side: Tuple = wall[2], wall[3]

                # horizontal_wall =  bottom_side[0][1] == bottom_side[1][1] or top_side[0][1] == top_side[1][1]
                # vertical_wall = bottom_side[0][0] == bottom_side[1][0] or top_side[0][0] == top_side[1][0]

                is_paddle_horizontal = self.paddle.position[2] == 'horizontal'
                is_paddle_vertical = self.paddle.position[2] == 'vertical'

                if is_paddle_vertical:
                    wall1 = (bottom_side[1], top_side[1])
                    wall2 = (bottom_side[0], top_side[0])
                    self.vertical_partial_collision(self.paddle_segments['right_segment'], wall1, wall2, 'top')
                    self.vertical_partial_collision(self.paddle_segments['left_segment'], wall2, wall1, 'down')

                if is_paddle_horizontal:
                    pass
                

        print('Side 1 Stop: ', self.side1_stop_range)
        print('Side 2 Stop: ', self.side2_stop_range)

if __name__ == "__main__":
      paddle = Paddle()
      paddle.test_run()

      # TODO:
      # ! Add paddle control customization , this can help for seperate player paddle key handlings
      # ! Add locking
      # ! Add Paddle Horizontal Collision on wall direction logic