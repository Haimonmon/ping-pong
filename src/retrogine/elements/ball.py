import os
import time
import math
import random
import threading
import tkinter as tk

from typing import Tuple

class NoPlayground(Exception):
    pass

class TheFlash(Exception):
    pass

class Ball:
    """
    First ping pong ball of all time! 🔴
    """
    def __init__(self, playground: object, size: int = 10, color: str = "red", speed: float = 4) -> None:
        if not playground:
            raise NoPlayground("The pong no where to be placed amigo 🏓")
        
        if speed >= 9:
            raise TheFlash(f'Cant handle that speed for now ⚡: {speed}')

        # * Object PlayGround()
        self.playground = playground
        
        # * Wall Coordinates
        if self.playground.wall:
            self.wall = self.playground.wall.coordinates
        else:
            self.wall = None

        # * Starting position at the center ;)
        self.ball_x_pos = self.playground.platform_dimension['width'] // 2
        self.ball_y_pos = self.playground.platform_dimension['height'] // 2

        # * Ball Customization for now
        self.color = color
        self.size = size

        # * Fixed speed for dx and dy
        self.speed = speed

        # * Ball directions on x and y axis
        self.ball_dx = 0
        self.ball_dy = 0

        self.radius = self.size / 2

        # * Locking of thread to avoid critical sections of live performance of task
        self.lock = threading.Lock()
        
        # * display ping pong ball
        self.ball = self.render()

        # ? Allow Thread to Run
        self.run = True

        # * Helper classes
        self.collision = CollisionHandler(self)
        self.physics = PhysicsHandler(self)

        # * Sets the speed trajectory once the round starts
        self.physics.fix_ball_speed()

        # * Parallel Threading for movements in a seperate thread
        self.thread = threading.Thread(target=self.physics.ball_movement)
        self.thread.daemon = True
        self.thread.start()

    
    def render(self) -> int:
        return self.playground.platform.create_oval(self.ball_x_pos - self.size, self.ball_y_pos - self.size, self.ball_x_pos + self.size, self.ball_y_pos + self.size, fill = self.color)
    
    def stop(self) -> None:
        self.run = False
        self.thread.join()


class CollisionHandler:
    """
    Does it hit?? 🧨💥
    """
    def __init__(self, ball: Ball) -> None:
        self.ball = ball
        self.playground = ball.playground

    
    def check_paddle_boundaries(self, paddles) -> None:
        with self.ball.lock:
            coordinates: list = self.playground.platform.coords(self.ball.ball)

            ball_left = coordinates[0]
            ball_top = coordinates[1]
            ball_right = coordinates[2]
            ball_bottom = coordinates[3]

            for paddle in paddles:
                paddle_coordinates = paddle.coordinates

                for wall in paddle_coordinates:
                    bottom_side: Tuple = wall[0], wall[1]
                    top_side: Tuple = wall[2], wall[3]

                    horizontal_wall: bool = bottom_side[0][1] == bottom_side[1][1] or top_side[0][1] == top_side[1][1]

                    vertical_wall: bool = bottom_side[0][0] == bottom_side[1][0] or top_side[0][0] == top_side[1][0]

                    # * Check for horizontal wall collision
                    if horizontal_wall:
                        self.check_horizontal_collision(bottom_side, top_side, ball_left, ball_right, ball_top, ball_bottom)

                    # * Check for vertical wall collision
                    if vertical_wall:
                        self.check_vertical_collision(bottom_side, top_side, ball_left, ball_right, ball_top, ball_bottom)
    
    
    
    def check_wall_boundaries(self) -> None:
            # * Reference [How to get the specific widget coordinates.]: https://stackoverflow.com/questions/50699664/change-coords-of-line-in-python-tkinter-canvas
            with self.ball.lock:
                coordinates: list = self.playground.platform.coords(self.ball.ball)

                # * Ball Direction
                ball_left = coordinates[0]
                ball_top = coordinates[1]
                ball_right = coordinates[2]
                ball_bottom = coordinates[3]

                for wall in self.playground.wall.coordinates:
                    bottom_side: Tuple = wall[0], wall[1]  
                    top_side: Tuple = wall[2], wall[3]
                    
                    horizontal_wall: bool = bottom_side[0][1] == bottom_side[1][1] or top_side[0][1] == top_side[1][1]
                    
                    vertical_wall: bool = bottom_side[0][0] == bottom_side[1][0] or top_side[0][0] == top_side[1][0]
        
                    # * Check for horizontal wall collision
                    if horizontal_wall:
                        self.check_horizontal_collision(bottom_side, top_side, ball_left, ball_right, ball_top, ball_bottom)
                        

                    # * Check for vertical wall collision
                    if vertical_wall:
                        self.check_vertical_collision(bottom_side, top_side, ball_left, ball_right, ball_top, ball_bottom)

                    # ! Fix Out of bounds range
                    out_of_bounds: bool = (
                            ball_left < -105 or
                            ball_right > self.playground.platform_dimension['width'] + 105 or
                            ball_top < -105 or
                            ball_bottom > self.playground.platform_dimension['height'] + 105
                        )
        
                    if out_of_bounds:
                        self.ball.physics.reset_direction()
    


    def check_horizontal_collision(self, bottom_wall_side: Tuple, top_wall_side: Tuple, ball_left: float, ball_right: float, ball_top: float, ball_bottom: float) -> None:
        """
        Checks for ball horizontal wall collision 
        """
        if bottom_wall_side[0][0] <= ball_left and bottom_wall_side[1][0] >= ball_right and (ball_top <= bottom_wall_side[0][1] <= ball_bottom):
            if self.ball.ball_dy > 0:
                self.ball.physics.reverse_y_direction() # * Already Locked

        if bottom_wall_side[0][0] <= ball_left and bottom_wall_side[1][0] >= ball_right and (ball_top <= top_wall_side[0][1] <= ball_bottom):
            if self.ball.ball_dy < 0:
                self.ball.physics.reverse_y_direction()  # * Already Locked



    def check_vertical_collision(self, bottom_wall_side: Tuple, top_wall_side: Tuple, ball_left: float, ball_right: float, ball_top: float, ball_bottom: float) -> None:
        """
        Checks for ball vertical wall collision
        """

        if (bottom_wall_side[0][1] <= ball_bottom and bottom_wall_side[1][1] >= ball_top and ball_left <= bottom_wall_side[0][0] <= ball_right):
            if self.ball.ball_dx > 0:
                self.ball.physics.reverse_x_direction() # * Already Locked

        if bottom_wall_side[0][1] <= ball_bottom and bottom_wall_side[1][1] >= ball_top and (ball_left <= top_wall_side[0][0] <= ball_right):
            if self.ball.ball_dx < 0:
                self.ball.physics.reverse_x_direction()  # * Already Locked

                 
class PhysicsHandler:
    """
    Calculates trajectories 🤓☝️
    """
    def __init__(self, ball: Ball):
        self.ball = ball
        self.collision = ball.collision
        self.playground = ball.playground

        self.paddles = self.ball.playground.paddles


    def ball_movement(self) -> None:
         """
         While loop will be on seperated looping task by the help of thread
         """
         while self.ball.run:
            self.move_ball()
            time.sleep(0.01)


    def move_ball(self) -> None:
        """
        Enable ball movements
        """
    
        with self.ball.lock:
            
            self.playground.platform.move(self.ball.ball, self.ball.ball_dx, self.ball.ball_dy)
            

        if len(self.paddles) != 0:
            self.collision.check_paddle_boundaries(self.paddles)

        if self.ball.wall:
            self.collision.check_wall_boundaries()



    def fix_ball_speed(self, recursion_attempt: int = 0) -> None:
        """
        Fixes the ball on its desired speed at any direction
        """
        # * Set default value to avoid recursion stacking :>
        if recursion_attempt >= 2:
            self.ball.ball_dx = 2
            self.ball.ball_dy = -2
            return
            
        directions: list = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]
        
        ball_dx = random.choice(directions)
        ball_dy = random.choice(directions)
        # self.ball.ball_dx = -4
        # self.ball.ball_dy = 2

        magnitude = math.sqrt(ball_dx**2 + ball_dy**2)
        
        # ! To avoid dx, dy both 0 so it will not cause any errors for the divisions
        if ball_dx == 0 and ball_dy == 0:
            return self.fix_ball_speed(recursion_attempt + 1)

    
        self.ball.ball_dx = int((ball_dx / magnitude) * self.ball.speed)
        self.ball.ball_dy = int((ball_dy / magnitude) * self.ball.speed)

        # ! Ensures the ball will not be in perfect vertical trajectory
        if self.ball.ball_dx == 0:
            return self.fix_ball_speed(recursion_attempt + 1)


    def reverse_x_direction(self) -> None:
            self.ball.ball_dx *= -1


    def reverse_y_direction(self) -> None:
            self.ball.ball_dy *= -1


    def reset_direction(self) -> None:
        """
        Resets ball Position in order to reset the round and replay it and have fun again :)
        """
        
        self.playground.platform.coords(
            self.ball.ball, 
            self.ball.ball_x_pos - self.ball.size, 
            self.ball.ball_y_pos - self.ball.size, 
            self.ball.ball_x_pos + self.ball.size, 
            self.ball.ball_y_pos + self.ball.size
        )

        self.fix_ball_speed()


    def set_speed(self, speed:int) -> None:
        with self.ball.lock:
            self.ball_speed = speed


if __name__ == "__main__":
    ball = Ball()
    ball.test_run()

    # TODO: 
    # ! Add paddle collision logic

    