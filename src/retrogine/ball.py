import time
import math
import random
import threading
import tkinter as tk


class NoPlayground(Exception):
    pass


class Ball:
    """
    First ping pong ball of all time! 🔴
    """
    def __init__(self, playground: object, ball_size: int = 10, ball_color: str = "red", ball_speed: float = 5.5) -> None:
        if not playground:
            raise NoPlayground("The pong no where to be placed amigo 🏓")

        # * Object PlayGround()
        self.playground = playground
        self.playground_coordinates = self.playground.get_wall_coordinates()

        # * Starting position
        self.ball_x_pos = self.playground_coordinates["right"] // 2
        self.ball_y_pos = self.playground_coordinates["bottom"] // 2

        self.ball_color = ball_color
        self.ball_size = ball_size

        # * Fixed speed for dx and dy
        self.ball_speed = ball_speed

        # * Ball directions on x and y axis
        self.ball_dx = 0
        self.ball_dy = 0

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
        self.playground.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        self.check_boundaries()


    def fix_ball_speed(self) -> None:
        """
        Fixes the ball on its desired speed at any direction
        """
        directions: list = [-3, -2, -1, 1 ,2 ,3]
        self.ball_dx = random.choice(directions)
        self.ball_dy = random.choice(directions)

        # * Pythagoream theorem
        magnitude = math.sqrt(self.ball_dx**2 + self.ball_dy**2)

        self.ball_dx = int((self.ball_dx / magnitude) * self.ball_speed)
        self.ball_dy = int((self.ball_dy / magnitude) * self.ball_speed)



    def check_boundaries(self) -> None:
        """
        For collision checking of ball
        """
        # * Reference [How to get the specific widget coordinates.]: https://stackoverflow.com/questions/50699664/change-coords-of-line-in-python-tkinter-canvas
        coordinates: list = self.playground.canvas.coords(self.ball)

        top_collision: bool = int(coordinates[1]) <= self.playground_coordinates['top']
        bottom_collision: bool = int(coordinates[3]) >= self.playground_coordinates['bottom']

        left_wall_collision: bool = int(coordinates[0]) <= self.playground_coordinates['left']
        right_wall_collision: bool = int(coordinates[2]) >= self.playground_coordinates['right']

        out_of_bounds: bool = (int(coordinates[1]) < self.playground_coordinates['top'] - 5 or 
                               int(coordinates[3]) > self.playground_coordinates['bottom'] + 5 or 
                               int(coordinates[0]) < self.playground_coordinates['left'] - 5 or 
                               int(coordinates[2]) > self.playground_coordinates['right'] + 5)
        
        if top_collision or bottom_collision:
            self.ball_dy *= -1

        # if left_wall_collision or right_wall_collision:
        #     self.ball_dx *= -1

        if out_of_bounds:
            self.reset_ball()


    def reset_ball(self) -> None:
        """
        Reset's ball stats and position for the next round
        """
        self.playground.canvas.coords(self.ball, self.ball_x_pos - self.ball_size, self.ball_y_pos - self.ball_size, self.ball_x_pos + self.ball_size, self.ball_y_pos + self.ball_size)

        # * Reset ball speed =🔴
        self.fix_ball_speed()


    
    def set_ball_speed(self, speed) -> None:
        self.ball_speed = speed

 
if __name__ == "__main__":
    ball = Ball()
    ball.test_run()

    