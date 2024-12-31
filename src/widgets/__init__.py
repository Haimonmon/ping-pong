"""
Widgets
=======

A package that provides a collection of reusable Tkinter widgets to simplify GUI development.

Overview
--------

This package offers a set of pre-built Tkinter widgets that can be easily 
integrated into your projects. 

The `WidgetGenerator` class is a builder that allows you to create custom Tkinter widgets 
in a concise and readable way.

Usage
-----
``` python
import widgets as tkw

# Create a WidgetGenerator instance
widgets = tkw.WidgetGenerator(root)

widgets.create_label(text = "Hello World", fg = "green")  #it will automatically return Label Widget
```

Creator:
    >>> package by: Haimonmonify
"""

from widgets.tk_window_generator import WindowGenerator