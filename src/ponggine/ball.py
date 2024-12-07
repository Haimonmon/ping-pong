import tkinter as tk

class Ball:
    """
    First ping pong ball of all time! 🔴
    """
    def __init__(self, ball_x_pos: int, ball_y_pos: int) -> None:
        # self.window = tk.Tk()
        # self.window.title("Test ping-pong Ball")
        # self.window.geometry("600x400")

        self.ball_x_pos = ball_x_pos
        self.ball_y_pos = ball_y_pos

    
    def ball_movement(self) -> None:
         pass

    def render_ball(self) -> None:
         pass
    
    def calculate_trajectory(self) -> None:
        """
        this will be using sin, cos and research will be having for math formulas 🦖
        """
        pass
    
    def test_run(self) -> None:
         self.window.mainloop()
         print('Running...')


if __name__ == "__main__":
      ball = Ball()
      ball.test_run()