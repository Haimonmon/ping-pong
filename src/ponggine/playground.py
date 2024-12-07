import tkinter as tk

class PlayGround:
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.title("Test ping-pong Ball")


        self.width = 1000
        
        # self.width = 1000

        self.height = 400
        self.window.geometry(f"{self.width}x{self.height}")

    def render_court(self) -> None:
        pass

    def test_run(self) -> None:
         print('Welcome to the Ping pong\'s PlayGround')
         self.window.mainloop()

if __name__ == "__main__":
      playground = PlayGround()
      playground.test_run()