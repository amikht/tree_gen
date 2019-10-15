import turtle as t
import random
import math

WIDTH = 640
HEIGHT = 480

DAMP_FACTOR = 5
SEC_LENGTH = 20

def init():
    t.speed(9)
    t.screensize(WIDTH, HEIGHT)
    t.setworldcoordinates(0, 0, WIDTH, HEIGHT)
    drawStage()

def drawSection(width, angle, mid_x, mid_y):
    """
    Assumes turtle is facing north

    returns new avg. x position and width
    """

    print("Drawing section")

    unit_width = width / 2
    BLx = mid_x - unit_width
    BLy = mid_y - (SEC_LENGTH / 2)
    
    TLx = BLx + (SEC_LENGTH * math.tan(angle - 5))
    TLy = BLy + SEC_LENGTH
    
    BRx = mid_x + unit_width
    BRy = mid_y - (SEC_LENGTH / 2)

    TRx = BRx + (SEC_LENGTH * math.tan(angle + 5))
    TRy = BRy + SEC_LENGTH

    t.penup()
    t.setpos(BLx, BLy)
    
    t.pendown()
    t.setpos(TLx, TLy)
    t.setpos(TRx, TRy)
    t.setpos(BRx, BRy)

    return ((TRx + TRy) / 2, TRx - TLx)


def drawStage():
    t.penup()
    t.left(90)
    t.setpos(20, 20)
    t.pendown()
    t.setpos(WIDTH - 20, 20)

def drawTree():
    print("drawing tree")
    x = WIDTH / 2
    y = 20 + (SEC_LENGTH / 2)
    width = 20
    angle = random.random() - 0.5
    while width > 0:
        x, width = drawSection(width, angle, x, y)
        y += SEC_LENGTH

        angle += random.random() - 0.5
    t.done()

def main():
    init()
    drawTree()

if __name__ == "__main__":
    main()