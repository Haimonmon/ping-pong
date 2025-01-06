import tkinter as tk

class Platform:
    def __init__(self, playground: object, width: int, height: int, padding: int = 100, color: str = 'black'):
        self.width = width
        self.height = height

        self.padding = padding // 2

        self.color = color

        self.playground = playground

        self.canvas = None

        self.render()

    def render(self) -> None:
        platform_width = self.width + self.padding * 2
        platform_height = self.height + self.padding * 2

        platform = tk.Canvas(
             self.playground.master, 
             width = platform_width,
             height = platform_height, 
             background = self.color, 
             highlightthickness = 1, 
             bd = 1,
             relief='solid',
             highlightbackground = 'white'
            )
        
        platform.pack()

        platform.place(relx=0.5, rely=0.5, anchor="center")

        self.canvas = platform

if __name__ == "__main__":
      pass