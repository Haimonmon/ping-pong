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
    def __init__(self, playground: object, size: int = 10, color: str = "red", speed: float = 4) -> None:
        if not playground:
            raise NoPlayground("The pong no where to be placed amigo 🏓")
        
        if speed >= 9:
            raise TheFlash(f'Cant handle that speed for now ⚡: {speed}')

        # * Object PlayGround()
        self.playground = playground
        
        # * Wall Coordinates
        self.wall = self.playground.wall.coordinates

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

        # * Locking of thread to avoid critical sections of live performance of task
        self.lock = threading.Lock()
        
        # * display ping pong ball
        self.ball = self.render()

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

   
class CollisionHandler:
    """
    Does it hit?? 🧨💥
    """
    def __init__(self, ball: Ball) -> None:
        self.ball = ball
        self.playground = ball.playground

    
    def check_paddle_boundaries(self) -> None:
        pass
    

    def check_boundaries(self) -> None:
            # * Reference [How to get the specific widget coordinates.]: https://stackoverflow.com/questions/50699664/change-coords-of-line-in-python-tkinter-canvas
            with self.ball.lock:
                coordinates: list = self.playground.platform.coords(self.ball.ball)

                ball_left = coordinates[0]
                ball_top = coordinates[1]
                ball_right = coordinates[2]
                ball_bottom = coordinates[3]

                for wall in self.playground.wall.coordinates:
                    wall_start = wall[0]
                    wall_end = wall[1]
                    
                    # * Checks if horizontal
                    if wall_start[1] == wall_end[1]:
                        wall_y = wall_start[1]
                        if wall_start[0] <= ball_right and wall_end[0] >= ball_left and ball_top <= wall_y <= ball_bottom:
                            self.ball.physics.reverse_y_direction()
                            break  
                    
                    # * Checks if vertical
                    elif wall_start[0] == wall_end[0]:  
                        wall_x = wall_start[0]
                        if wall_start[1] <= ball_bottom and wall_end[1] >= ball_top and ball_left <= wall_x <= ball_right:
                            self.ball.physics.reverse_x_direction()
                            break
                
                    out_of_bounds: bool = (
                            ball_left < -10 or
                            ball_right > self.playground.platform_dimension['width'] + 10 or
                            ball_top < -10 or
                            ball_bottom > self.playground.platform_dimension['height'] + 10
                        )
        
                    if out_of_bounds:
                        self.ball.physics.reset_direction()
                # top_collision: bool = int(coordinates[1]) <= self.playground_coordinates['top'] - self.playground.wall_thickness or int(coordinates[1]) <= self.playground_coordinates['top']
                # bottom_collision: bool = int(coordinates[3]) >= self.playground_coordinates['bottom'] + self.playground.wall_thickness or int(coordinates[3]) >= self.playground_coordinates['bottom']

                # left_wall_collision: bool = int(coordinates[0]) <= self.playground_coordinates['left'] - self.playground.wall_thickness or int(coordinates[0]) <= self.playground_coordinates['left']
                # right_wall_collision: bool = int(coordinates[2]) >= self.playground_coordinates['right'] + self.playground.wall_thickness or int(coordinates[2]) >= self.playground_coordinates['right']

                # out_of_bounds: bool = (int(coordinates[1]) < self.playground_coordinates['top'] - (self.playground.wall_thickness - 5) or 
                #                     int(coordinates[3]) > self.playground_coordinates['bottom'] + (self.playground.wall_thickness + 5) or 
                #                     int(coordinates[0]) < self.playground_coordinates['left'] - (self.playground.wall_thickness - 5) or 
                #                     int(coordinates[2]) > self.playground_coordinates['right'] + (self.playground.wall_thickness) + 5)
                
            # if top_collision or bottom_collision:
            #     self.ball.physics.reverse_y_direction()

            # if left_wall_collision or right_wall_collision:
            #    self.ball.physics.reverse_x_direction()
       
            # if out_of_bounds:
            #     self.ball.physics.reset_direction()


class PhysicsHandler:
    """
    Calculates trajectories 🤓☝️
    """
    def __init__(self, ball: Ball):
        self.ball = ball
        self.collision = ball.collision
        self.playground = ball.playground


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
        with self.ball.lock:
            self.playground.platform.move(self.ball.ball, self.ball.ball_dx, self.ball.ball_dy)

        self.collision.check_boundaries()


    def fix_ball_speed(self, recursion_attempt: int = 0) -> None:
        """
        Fixes the ball on its desired speed at any direction
        """
        # * Set default value to avoid recursion stacking :>
        if recursion_attempt >= 4:
            self.ball.ball_dx = 2
            self.ball.ball_dy = -2
            return
        
        directions: list = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]
        self.ball.ball_dx = random.choice(directions)
        self.ball.ball_dy = random.choice(directions)

        # * Pythagoream theorem
        magnitude = math.sqrt(self.ball.ball_dx**2 + self.ball.ball_dy**2)
        
        # ! To avoid dx, dy both 0 so it will not cause any errors for the divisions
        if self.ball.ball_dx == 0 and self.ball.ball_dy == 0:
            return self.fix_ball_speed(recursion_attempt + 1)

        self.ball.ball_dx = int((self.ball.ball_dx / magnitude) * self.ball.speed)
        self.ball.ball_dy = int((self.ball.ball_dy / magnitude) * self.ball.speed)

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
        self.playground.platform.coords(self.ball.ball, self.ball.ball_x_pos - self.ball.size, self.ball.ball_y_pos - self.ball.size, self.ball.ball_x_pos + self.ball.size, self.ball.ball_y_pos + self.ball.size)
        self.fix_ball_speed()


    def set_speed(self, speed:int) -> None:
        with self.ball.lock:
            self.ball_speed = speed


if __name__ == "__main__":
    ball = Ball()
    ball.test_run()

    # TODO: 
    # ! Fix Wall collision logic and suit it on the given wall coordinates
    # ! Add paddle collision logic
    # ! Seperate Collision logic for Single Responsibility
    # ! Critical Section Fix, Collision of wall and paddles

    