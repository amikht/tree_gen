import turtle as t
import random
import math

WIDTH = 640
HEIGHT = 480

DAMP_FACTOR = 1
SEC_LENGTH = 20

def init():
    t.speed(9)
    t.screensize(WIDTH, HEIGHT)
    t.setworldcoordinates(0, 0, WIDTH, HEIGHT)
    drawStage()

def getAngle(angle):
    """
    returns new angle based on supplied angle
    """
    return angle + (math.pi / 6) * random.random() - (math.pi / 12)

def drawSection(width, angle, mid_x, y):
    """
    Assumes turtle is facing north

    returns new avg. x position and width
    """

    x = mid_x + (SEC_LENGTH * math.tan(angle))
    points = [
        (mid_x - width, y),
        (mid_x + width, y),
        (x + width - DAMP_FACTOR, y + SEC_LENGTH),
        (x - width + DAMP_FACTOR, y + SEC_LENGTH)
    ]
    t.penup()
    t.setpos(points[0][0], points[0][1])
    t.begin_fill()
    for point in points:
        t.setpos(point[0], point[1])
    t.end_fill()
    return x

def drawStage():
    t.penup()
    t.left(90)
    t.setpos(20, 20)
    t.pendown()
    t.setpos(WIDTH - 20, 20)

def drawLeaf(x, y, angle):
    print("drawing leaf")

    leaf_len = 10
    internal_angle = math.radians(30)
    maj_axis = 2 * leaf_len * math.cos(internal_angle)
    points = [
        (x, y),
        (x + leaf_len * math.sin(angle - internal_angle),
            y + leaf_len * math.cos(angle - internal_angle)),
        (x + maj_axis * math.sin(angle), y + maj_axis * math.cos(angle)),
        (x + leaf_len * math.sin(angle + internal_angle),
            y + leaf_len * math.cos(angle + internal_angle))
    ]

    t.penup()
    t.setpos(points[0][0], points[0][1])
    t.begin_fill()
    for point in points:
        t.setpos(point[0], point[1])
    t.end_fill()

def drawTree(x, y, width, angle):
    print("drawing tree")
    while width > 0:
        x = drawSection(width, angle, x, y)
        y += SEC_LENGTH
        width -= DAMP_FACTOR
        angle = getAngle(angle)
    drawLeaf(x, y, angle)
    t.done()

def main():
    init()
    drawTree(WIDTH / 2, 20, 20, getAngle(0))

if __name__ == "__main__":
    main()