from tkinter import *
import math

master = Tk()

canvas_width = 800
canvas_height = 600
w = Canvas(master,
           width=canvas_width,
           height=canvas_height)
w.pack()

y = int(canvas_height / 2)
w.create_line(0, 0, canvas_width, y, fill="#476042")
r = 50
w.create_oval(100, 200, 100 + r, 100 + r, fill="blue", width=0.5)

min_radius = 3;
max_radius = 10;
sideViewHeight = 25;


class Offset:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    x = 0
    y = 0


class CenteredPart:
    def paint(self, canvas):
        pass

    center = Offset(0, 0)
    weight = 0

    def setHeight(self, height):
        self.height = height

    height = 1

class MobilePart ( CenteredPart ):
    def __init__(self, radius, color, gap):
        self.radius = radius
        self.color = color
        self.gap = gap
#assert(radius != null),
#assert(radius >= _min_radius),
#assert(radius <= _max_radius),
#assert(color != null)
        weight =  2 * math.pi * radius * radius;

    radius = 0
    weight = 0


mainloop()
