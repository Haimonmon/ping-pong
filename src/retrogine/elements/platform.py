import tkinter as tk

class Platform:
    def __init__(self, playground: object, width: int, height: int, padding: int = 100, color: str = 'black', responsive: bool = False, new_width: int = None, new_height: int = None):
        self.width = width # * Original width
        self.height = height # * Original Height
        
        self.new_width = new_width
        self.new_height = new_height

        self.padding = padding // 2

        self.color = color

        self.responsive = responsive

        self.playground = playground

        self.canvas = None

        self.render()


    def render(self) -> None:
        if not self.new_height or not self.new_width or not self.responsive:
            platform_width = self.width + self.padding * 2
            platform_height = self.height + self.padding * 2
        elif self.new_height and self.new_width and self.responsive:
            platform_width = self.new_width + self.padding * 2
            platform_height = self.new_height + self.padding * 2


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