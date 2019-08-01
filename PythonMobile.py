from tkinter import *
import math

master = Tk()

#   colors
blue = '#2196F3'
black = '#000000'
green = '#6bde54'
red = '#cc3030'

theta = 0.01

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
        self.weight = 2 * math.pi * radius * radius

    radius = 0
    weight = 0

class CrossBar(CenteredPart):
    def __init__(self, partEnd, joinEnd):
        self.weight = partEnd.weight + joinEnd.weight
        self.balanceRatio = joinEnd.weight / self.weight
        d = (partEnd.center.x - joinEnd.center.x)
        self.center = Offset(
            partEnd.center.x * self.balanceRatio +
            joinEnd.center.x * (1 - self.balanceRatio),
            partEnd.center.y * self.balanceRatio +
            joinEnd.center.y * (1 - self.balanceRatio))
        self.partLength = d * self.balanceRatio
        self.joinLength = d * (1 - self.balanceRatio)
        #assert((partEnd.weight * partLength - joinEnd.weight * joinLength).abs() < 1e-9)

    # @override
    # void paint(Canvas canvas) {
    # //  draw the part
    # partEnd.center = Offset(center.dx - partLength * cos(theta),
    # center.dy - partLength * sin(theta));
    # joinEnd.center = Offset(center.dx + joinLength * cos(theta),
    # center.dy + joinLength * sin(theta));
    #
    # //  up view
    # final paint = Paint();
    # paint.color = Colors.black;
    # paint.strokeWidth = 3;
    # canvas.drawLine(partEnd.center, joinEnd.center, paint);
    # canvas.drawCircle(center, 6, paint);
    #
    # //  side view
    # double y = sideViewHeight + sideViewHeight * _height;
    # canvas.drawLine(
    # Offset(partEnd.center.dx, y), Offset(joinEnd.center.dx, y), paint);
    # canvas.drawCircle(Offset(center.dx, y), 6, paint);
    # canvas.drawLine(Offset(joinEnd.center.dx, y),
    # Offset(joinEnd.center.dx, y + sideViewHeight), paint);
    #
    # //  recurse down
    # partEnd.paint(canvas);
    # joinEnd.paint(canvas);
    # }

    # @override
    # void setHeight(int height) {
    # super.setHeight(height);
    # partEnd.setHeight(height + 1);
    # joinEnd.setHeight(height + 1);
    # }

    # MobilePart partEnd
    # CenteredPart joinEnd
    # balanceRatio #  partEnd.weight/joinEnd.weight
    #  partLength
    #  joinLength
    #  theta = 0


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



#   initialize parts
lastX = 0.5 * canvas_width
y = 0.5 * canvas_width

partLimit = len(mobileParts)

#  locate parts initial position
lastPart = None
for i in range(len(mobileParts)-1, 0, -1):
    part = mobileParts[i]
    if lastPart is not None:
        lastX += (lastPart.gap + lastPart.radius) / 100 * canvas_width
    lastPart = part

    #  scale to display size
    r = part.radius / 100 * canvas_width
    lastX += r

    part.center = Offset(lastX, y)

i = 0
for x in mobileParts:
    print("{} {} {}".format(i, x.radius, x.color))
    i += 1

#  compute cross arms
#  i.e. derive arm length from initial positions
#  derive balance points from weights
dTheta = math.pi / 25
theta = 0
lastCenteredPart = None
for i in range(len(mobileParts)-1, 0,-1):
    part = mobileParts[i]
    if lastCenteredPart is not None:
        crossBar = CrossBar(part, lastCenteredPart)
        theta += dTheta
        crossBar.theta = theta
        crossBars.append(crossBar)
        lastCenteredPart = crossBar
    else:
        lastCenteredPart = part

lastCenteredPart = crossBars[len(crossBars)-1]
if lastCenteredPart is not None:
    lastCenteredPart.center = Offset(0.5 * canvas_width, y)
    lastCenteredPart.height = 0


mainloop()

