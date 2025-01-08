"""
## Retro Engine

A Simple Pong's classic engine allows for ball, playground customization

### Usage
* Example code

==========================================
```python
    import tkinter as tk

    window = tk.Tk()

    manager = ret.PongManager()
    
    manager.setup(
        tkinter_window = window,
        playground_name = "classic",
        gamemode = "pvp",
        gametype = "double_ball"
    )
```
==========================================

[ ♻️ Note ] - Still on Testing and still alot of bugs 🐞

>>> package by: Haimonmon 🧙‍♂️
"""

from .util import PongManager
from .elements import PlayGround

__all__ = [
    'PlayGround',
    'PongManager'
]


