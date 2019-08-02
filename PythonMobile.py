from tkinter import *
import math

master = Tk()

#   colors
blue = '#2196F3'
black = '#000000'
green = '#6bde54'
red = '#cc3030'

theta = math.pi/256
updatePeriod = int(round(1000 / 60))

canvas_width = 800
canvas_height = 600
canvas = Canvas(master,
           width=canvas_width,
           height=canvas_height)
canvas.pack()

min_radius = 3
max_radius = 10


class Offset:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    x = 0
    y = 0


class CenteredPart:
    def paint(self):
        pass

    center = Offset(0, 0)
    weight = 0


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

    def paint(self):
        canvas.create_oval(self.center.x-self.radius, self.center.y-self.radius, self.center.x+self.radius,
                           self.center.y+self.radius, fill=self.color, width=0.5)

    radius = 0
    weight = 0


class CrossBar(CenteredPart):
    def __init__(self, partEnd, joinEnd):
        self.partEnd = partEnd
        self.joinEnd = joinEnd
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
        # assert((partEnd.weight * partLength - joinEnd.weight * joinLength).abs() < 1e-9)

    # @override
    def paint(self):
        #  draw the part
        self.partEnd.center = Offset(self.center.x - self.partLength * math.cos(self.theta), 
                                     self.center.y - self.partLength * math.sin(self.theta))
        self.joinEnd.center = Offset(self.center.x + self.joinLength * math.cos(self.theta),
                                     self.center.y + self.joinLength * math.sin(self.theta))
        #  up view
        # final paint = Paint();
        # paint.color = Colors.black;
        # paint.strokeWidth = 3;
        # canvas.drawLine(partEnd.center, joinEnd.center, paint);
        canvas.create_line(self.partEnd.center.x, self.partEnd.center.y, self.joinEnd.center.x, self.joinEnd.center.y,
                           fill="#476042")
        #  recurse down
        self.partEnd.paint()
        self.joinEnd.paint()

    # MobilePart partEnd
    # CenteredPart joinEnd
    # balanceRatio #  partEnd.weight/joinEnd.weight
    #  partLength
    #  joinLength
    #  theta = 0


#   parts list, note that the radius is in relative units here
mobileParts = [MobilePart(10, black, 4),
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
for i in range(len(mobileParts) - 1, 0, -1):
    part = mobileParts[i]
    if lastPart is not None:
        lastX += (lastPart.gap + lastPart.radius) / 100 * canvas_width
    lastPart = part

    #  scale to display size
    r = part.radius / 100 * canvas_width
    part.radius = r
    lastX += r

    part.center = Offset(lastX, y)

#  compute cross arms
#  i.e. derive arm length from initial positions
#  derive balance points from weights
dTheta = math.pi / 25
theta = 0
lastCenteredPart = None
for i in range(len(mobileParts) - 1, 0, -1):
    part = mobileParts[i]
    if lastCenteredPart is not None:
        crossBar = CrossBar(part, lastCenteredPart)
        theta += dTheta
        crossBar.theta = theta
        crossBars.append(crossBar)
        lastCenteredPart = crossBar
    else:
        lastCenteredPart = part

lastCenteredPart = crossBars[len(crossBars) - 1]
if lastCenteredPart is not None:
    lastCenteredPart.center = Offset(0.5 * canvas_width, y)


#   once a vertical task
def task():
    #theta += math.pi/256
    crossBars[0].paint()
    master.after(updatePeriod, task)  # reschedule event in 2 seconds


master.after(updatePeriod, task)

master.mainloop()
