import time
import math
import random
import threading
import tkinter as tk


class NoPlayground(Exception):
    pass

class TheFlash(Exception):
    pass

class Ball:
    """
    First ping pong ball of all time! 🔴
    """
    def __init__(self, playground: object, ball_size: int = 10, ball_color: str = "red", ball_speed: float = 4) -> None:
        if not playground:
            raise NoPlayground("The pong no where to be placed amigo 🏓")
        
        if ball_speed >= 9:
            raise TheFlash(f'Cant handle that speed for now ⚡: {ball_speed}')

        # * Object PlayGround()
        self.playground = playground
        self.playground_coordinates = self.playground.wall_coordinates

        # * Wall Coordinates
        self.__walls = self.playground.wall

        # * Starting position at the center ;)
        self.ball_x_pos = self.playground_coordinates["right"] // 2
        self.ball_y_pos = self.playground_coordinates["bottom"] // 2

        self.ball_color = ball_color
        self.ball_size = ball_size

        # * Fixed speed for dx and dy
        self.ball_speed = ball_speed

        # * Ball directions on x and y axis
        self.ball_dx = 0
        self.ball_dy = 0

        # * Locking of thread to avoid critical sections of live performance of task
        self.lock = threading.Lock()

        # * Sets the speed trajectory once the round starts
        self.fix_ball_speed()
        
        # * display ping pong ball
        self.ball = self.render_ball()

        # * Parallel Threading for movements in a seperate thread
        self.thread = threading.Thread(target=self.ball_movement)
        self.thread.daemon = True
        self.thread.start()
    

    def render_ball(self) -> int:
        return self.playground.canvas.create_oval(self.ball_x_pos - self.ball_size, self.ball_y_pos - self.ball_size, self.ball_x_pos + self.ball_size, self.ball_y_pos + self.ball_size, fill = self.ball_color)
         

    def ball_movement(self) -> None:
         """
         While loop will be on seperated looping task by the help of thread
         """
         while True:
            self.move_ball()
            time.sleep(0.01)


    def move_ball(self) -> None:
        """
        Enable ball movements
        """
        with self.lock:
            self.playground.canvas.move(self.ball, self.ball_dx, self.ball_dy)
            
        self.check_boundaries()


    def fix_ball_speed(self, recursion_attempt: int = 0) -> None:
        """
        Fixes the ball on its desired speed at any direction
        """
        # * Set default value to avoid recursion stacking :>
        if recursion_attempt >= 4:
            self.ball_dx = 2 
            self.ball_dy = -2
            return
        
        directions: list = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]
        self.ball_dx = random.choice(directions)
        self.ball_dy = random.choice(directions)

        # * Pythagoream theorem
        magnitude = math.sqrt(self.ball_dx**2 + self.ball_dy**2)
        
        # ! To avoid dx, dy both 0 so it will not cause any errors for the divisions
        if self.ball_dx == 0 and self.ball_dy == 0:
            return self.fix_ball_speed(recursion_attempt + 1)

        self.ball_dx = int((self.ball_dx / magnitude) * self.ball_speed)
        self.ball_dy = int((self.ball_dy / magnitude) * self.ball_speed)

        # ! Ensures the ball will not be in perfect vertical trajectory
        if self.ball_dx == 0:
            return self.fix_ball_speed(recursion_attempt + 1)


    # def check_boundaries(self) -> None:
    #     """
    #     For collision checking of ball
    #     """
    #     with self.lock:
    #         # * Reference [How to get the specific widget coordinates.]: https://stackoverflow.com/questions/50699664/change-coords-of-line-in-python-tkinter-canvas
    #         coordinates: list = self.playground.canvas.coords(self.ball)

    #         top_collision: bool = int(coordinates[1]) <= self.playground_coordinates['top'] - self.playground.wall_thickness or int(coordinates[1]) <= self.playground_coordinates['top']
    #         bottom_collision: bool = int(coordinates[3]) >= self.playground_coordinates['bottom'] + self.playground.wall_thickness or int(coordinates[3]) >= self.playground_coordinates['bottom']

    #         left_wall_collision: bool = int(coordinates[0]) <= self.playground_coordinates['left'] - self.playground.wall_thickness or int(coordinates[0]) <= self.playground_coordinates['left']
    #         right_wall_collision: bool = int(coordinates[2]) >= self.playground_coordinates['right'] + self.playground.wall_thickness or int(coordinates[2]) >= self.playground_coordinates['right']

    #         out_of_bounds: bool = (int(coordinates[1]) < self.playground_coordinates['top'] - (self.playground.wall_thickness - 5) or 
    #                             int(coordinates[3]) > self.playground_coordinates['bottom'] + (self.playground.wall_thickness + 5) or 
    #                             int(coordinates[0]) < self.playground_coordinates['left'] - (self.playground.wall_thickness - 5) or 
    #                             int(coordinates[2]) > self.playground_coordinates['right'] + (self.playground.wall_thickness) + 5)
            
    #         if top_collision or bottom_collision:
    #             self.ball_dy *= -1

    #         # if left_wall_collision or right_wall_collision:
    #         #     self.ball_dx *= -1
            
    #         if out_of_bounds:
    #             print('Out of bounds')
    #             # * Resets ball Position in order to reset the round and replay it and have fun again :)
    #             self.playground.canvas.coords(self.ball, self.ball_x_pos - self.ball_size, self.ball_y_pos - self.ball_size, self.ball_x_pos + self.ball_size, self.ball_y_pos + self.ball_size)
    #             self.fix_ball_speed()
    

    def set_ball_speed(self, speed:int) -> None:
        with self.lock:
            self.ball_speed = speed

    
    

class CollisionHandler:
    def __init__(self, object: object):
        self.object = object
        self.object_coordinates = None
    

    def check_paddle_boundaries(self) -> None:
        pass
    
    
    def check_boundaries(self) -> None:
            # * Reference [How to get the specific widget coordinates.]: https://stackoverflow.com/questions/50699664/change-coords-of-line-in-python-tkinter-canvas
            coordinates: list = self.playground.canvas.coords(self.ball)

            top_collision: bool = int(coordinates[1]) <= self.playground_coordinates['top'] - self.playground.wall_thickness or int(coordinates[1]) <= self.playground_coordinates['top']
            bottom_collision: bool = int(coordinates[3]) >= self.playground_coordinates['bottom'] + self.playground.wall_thickness or int(coordinates[3]) >= self.playground_coordinates['bottom']

            left_wall_collision: bool = int(coordinates[0]) <= self.playground_coordinates['left'] - self.playground.wall_thickness or int(coordinates[0]) <= self.playground_coordinates['left']
            right_wall_collision: bool = int(coordinates[2]) >= self.playground_coordinates['right'] + self.playground.wall_thickness or int(coordinates[2]) >= self.playground_coordinates['right']

            out_of_bounds: bool = (int(coordinates[1]) < self.playground_coordinates['top'] - (self.playground.wall_thickness - 5) or 
                                int(coordinates[3]) > self.playground_coordinates['bottom'] + (self.playground.wall_thickness + 5) or 
                                int(coordinates[0]) < self.playground_coordinates['left'] - (self.playground.wall_thickness - 5) or 
                                int(coordinates[2]) > self.playground_coordinates['right'] + (self.playground.wall_thickness) + 5)
            
            if top_collision or bottom_collision:
                self.ball_dy *= -1

            # if left_wall_collision or right_wall_collision:
            #     self.ball_dx *= -1
            
            if out_of_bounds:
                print('Out of bounds')
                # * Resets ball Position in order to reset the round and replay it and have fun again :)
                self.playground.canvas.coords(self.ball, self.ball_x_pos - self.ball_size, self.ball_y_pos - self.ball_size, self.ball_x_pos + self.ball_size, self.ball_y_pos + self.ball_size)
                self.fix_ball_speed()


if __name__ == "__main__":
    ball = Ball()
    ball.test_run()

    # TODO: 
    # ! Fix Wall collision logic and suit it on the given wall coordinates
    # ! Add paddle collision logic
    # ! Seperate Collision logic for Single Responsibility

    