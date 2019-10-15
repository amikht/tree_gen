import turtle as t
import random
import math

WIDTH = 640
HEIGHT = 480

DAMP_FACTOR = 1
SEC_LENGTH = 20

TRUNK_COLOR = (random.random(), random.random(), random.random())
LEAF_COLOR = (random.random(), random.random(), random.random())

def init():
    """
    Initializes turtle settings and turtle window for the rest of program
    """
    t.speed(9)
    t.screensize(WIDTH, HEIGHT)
    t.setworldcoordinates(0, 0, WIDTH, HEIGHT)
    drawStage()

def getAngle(angle):
    """
    returns new angle based on supplied angle
    """
    return angle + (math.pi / 6) * random.random() - (math.pi / 12)

def drawSection(width, base_angle, angle, mid_x, y):
    """
    returns new avg. x position
    """
    t.color(TRUNK_COLOR)

    x = mid_x + (SEC_LENGTH * math.tan(angle - base_angle))
    points = [
        (mid_x - width * math.cos(base_angle), y - width * math.sin(base_angle)),
        (mid_x + width * math.cos(base_angle), y + width * math.sin(base_angle)),
        (x + width * math.cos(base_angle) - DAMP_FACTOR, y + SEC_LENGTH + width * math.sin(base_angle)),
        (x - width * math.cos(base_angle) + DAMP_FACTOR, y + SEC_LENGTH - width * math.sin(base_angle))
    ]
    t.penup()
    t.setpos(points[0][0], points[0][1])
    t.begin_fill()
    for point in points:
        t.setpos(point[0], point[1])
    t.end_fill()
    return x

def drawStage():
    """
    Draws the ground for the tree to live on
    """
    t.penup()
    t.left(90)
    t.setpos(20, 20)
    t.pendown()
    t.setpos(WIDTH - 20, 20)

def drawLeaf(x, y, angle):
    """
    Draws a predefined leaf shape at the given x, y position and at the given
    angle.
    """
    t.color(LEAF_COLOR)

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
    """
    Draws a tree growing from (x, y) with defined starting width.
    Provided angle is the base angle for the rest of the tree.
    Function uses recursive calls with changes to the angle as a way of
    drawing branches
    """
    base_angle = angle
    while width > 0:
        x = drawSection(width, base_angle, angle, x, y)
        y += SEC_LENGTH
        width -= DAMP_FACTOR
        angle = getAngle(angle)
    drawLeaf(x, y, angle - base_angle)
    t.done()

def main():
    init()
    drawTree(WIDTH / 2, 20, 20, math.radians(30))

if __name__ == "__main__":
    main()