class Paddle:
    """
    The Ping pong classic first paddle 🏓
    """
    def __init__(self, paddle_height: int , paddle_width: int, paddle_x_pos: int, paddle_y_pos: int) -> None:
        self.paddle_height = paddle_height
        self.paddle_width = paddle_width

        # ? Starting position of the paddle 🏓
        #self.paddle_coordinates = [paddle_x_pos, paddle_y_pos]

        self.paddle_x_pos = paddle_x_pos
        self.paddle_y_pos = paddle_y_pos

        # * Added for customize paddle movement keys ⬆️
        self.paddle_movements = {}


    def render(self) -> None:
        pass

    def move(self) -> None:
        pass

    def test_run(self) -> None:
        pass

    def display_movements(self) -> None:
        pass

    def edit_movements(self) -> None:
        pass
if __name__ == "__main__":
      paddle = Paddle()
      paddle.test_run()