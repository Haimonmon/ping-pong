import time
import threading
import tkinter as tk

class NoPlaygroundToBePlaced(Exception):
    pass


class Ball:
    """
    First ping pong ball of all time! 🔴
    """
    def __init__(self, playground: object, ball_size: int = 10, ball_color: str = "red") -> None:
        # * Object PlayGround()
        self.playground = playground
        self.playground_coordinates = self.playground.get_wall_coordinates()

        # * Starting position
        self.ball_x_pos = self.playground_coordinates["right"] // 2
        self.ball_y_pos = self.playground_coordinates["bottom"] // 2

        self.ball_color = ball_color
        self.ball_size = ball_size

        self.ball_dx = 5
        self.ball_dy = 5

        self.ball = self.render_ball()

        # * Parallel Threading for movements in a seperate thread
        self.thread = threading.Thread(target=self.ball_movement)
        self.thread.daemon = True
        self.thread.start()
    

    def render_ball(self) -> int:
        return self.playground.canvas.create_oval(self.ball_x_pos - self.ball_size, self.ball_y_pos - self.ball_size, self.ball_x_pos + self.ball_size, self.ball_y_pos + self.ball_size, fill = "red")
         

    def ball_movement(self) -> None:
         """
         While loop will be on seperated looping task by the help of thread
         """
         while True:
             self.playground.canvas.after(1, self.move_ball)
             time.sleep(0.01)


    def move_ball(self) -> None:
        self.playground.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        self.check_boundaries()


    def check_boundaries(self) -> None:
        """
        For collision checking of ball
        """
        # * Reference [How to get the specific widget coordinates.]: https://stackoverflow.com/questions/50699664/change-coords-of-line-in-python-tkinter-canvas
        coordinates = self.playground.canvas.coords(self.ball)
        
        if coordinates[1] <= 0 or coordinates[3] >= self.playground.height:
            self.ball_dy *= -1

        if coordinates[0] <= 0 or coordinates[2] >= self.playground.width:
            self.ball_dx *= -1


    def calculate_trajectory(self) -> None:
        """
        this will be using sin, cos and research will be having for math formulas 🦖
        """
        pass
    
if __name__ == "__main__":
    ball = Ball()
    ball.test_run()

    