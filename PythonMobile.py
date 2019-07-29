from tkinter import *
import math

master = Tk()

#   colors
blue = '#2196F3'
black = '#000000'
green = '#6bde54'
red = '#cc3030'

theta = 0.01;

canvas_width = 800
canvas_height = 600
w = Canvas(master,
           width=canvas_width,
           height=canvas_height)
w.pack()

y = int(canvas_height / 2)
w.create_line(0, 0, canvas_width, y, fill="#476042")
r = 50
w.create_oval(100, 200, 100 + r, 100 + r, fill=blue, width=0.5)

min_radius = 3
max_radius = 10
sideViewHeight = 25


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


class MobilePart(CenteredPart):
    def __init__(self, radius, color, gap):
        self.radius = radius
        self.color = color
        self.gap = gap
        # assert(radius != null),
        # assert(radius >= _min_radius),
        # assert(radius <= _max_radius),
        # assert(color != null)
        weight = 2 * math.pi * radius * radius

    radius = 0
    weight = 0

#   parts list, note that the radius is in relative units here
mobileParts = [ MobilePart(10, black, 4),
    MobilePart(8.6, green, 4),
    MobilePart(7.4, blue, 3),
    MobilePart(6.4, red, 2),
    MobilePart(5.6, green, 2),
    MobilePart(4.8, blue, 0),
    MobilePart(4.3, black, -2),
    MobilePart(4, red, -4),
    MobilePart(3.6, green, 2),
    MobilePart(3, blue, 0)]

crossBars = []

i = 0
for x in mobileParts:
    print("{} {} {}".format(i, x.radius, x.color))
    i += 1

#   initialize parts
lastX = 0.5 * canvas_width;
y = 0.5 * canvas_width;

partLimit = len(mobileParts)

#  locate parts initial position
for x in range(len(mobileParts), 0):
    part = mobileParts[i]
    if lastPart != None:
        lastX += (lastPart.gap + lastPart.radius) / 100 * canvas_width
        lastPart = part;

    #  scale to display size
    r = part.radius / 100 * canvas_width;
    lastX += r;

    part.center = Offset(lastX, y);


#  compute cross arms
#  i.e. derive arm length from initial positions
#  derive balance points from weights
crossBars.clear();
dTheta = math.pi / 25
theta = 0
# for x in range(mobileParts.length-1, 0):
#     part = mobileParts[i]
#     if lastCenteredPart != None:
#         crossBar = CrossBar(part, lastCenteredPart);
#         theta += dTheta;
#         _crossBar.theta = theta;
#         _crossBars.add(_crossBar);
#         lastCenteredPart = _crossBar;
#     else
#         lastCenteredPart = part
#
# crossBars.last?.center = Offset(0.5 * _canvasSize, y)
# crossBars.last?.setHeight(0)


mainloop()

