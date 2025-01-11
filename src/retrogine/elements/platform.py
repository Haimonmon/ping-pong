import tkinter as tk

class Platform:
    def __init__(self, playground: object, width: int, height: int, padding: int = 100, color: str = 'black', responsive: bool = False, canvas: tk.Canvas = None, new_width: int = None, new_height: int = None, pos_x: int = 0.5, pos_y: int = 0.5, border_color: str = '#FADAC1', border_size: int = 2.5):
        self.width = width # * Original width
        self.height = height # * Original Height
        
        self.new_width = new_width
        self.new_height = new_height

        self.padding = padding // 2

        self.color = color

        self.responsive = responsive

        self.playground = playground

        
        self.master_canvas = canvas
       
        self.canvas = None

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.border_color = border_color
        self.border_size = border_size

        self.render()


    def render(self) -> None:
        if not self.new_height or not self.new_width or not self.responsive:
            platform_width = self.width + self.padding * 2
            platform_height = self.height + self.padding * 2
        elif self.new_height and self.new_width and self.responsive:
            platform_width = self.new_width + self.padding * 2
            platform_height = self.new_height + self.padding * 2

        if self.master_canvas:
            master = self.master_canvas
        else:
            master = self.playground.master

        print(master)
        platform = tk.Canvas(
             master = master, 
             width = platform_width,
             height = platform_height, 
             background = self.color, 
             highlightthickness = self.border_size, 
             bd = 0,
             highlightcolor = self.border_color,
             relief='solid'
            )
        
        platform.pack()

        platform.place(relx=self.pos_x, rely=self.pos_y, anchor="center")

        self.canvas = platform

if __name__ == "__main__":
      pass