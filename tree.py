import turtle as t
import random
import math
import time

WIDTH = 640
HEIGHT = 480

def getTreeFactors():
    DAMP_FACTOR = random.random() * 1.75 + 0.25 
    SEC_LENGTH = random.randint(5, 20)
    BRANCH_FACTOR = random.random() * 0.69 + 0.01

    BRANCH_ANGLE = random.random() * (math.pi / 3) + math.pi / 24
    BRANCH_DAMP = random.random() * 0.5 + 0.25

    TRUNK_COLOR = (random.random(), random.random(), random.random())
    LEAF_COLOR = (random.random(), random.random(), random.random())

    INIT_WIDTH = random.randint(5, 50)
    
    tree_factors = {
        "damp_factor"   : DAMP_FACTOR,
        "sec_length"    : SEC_LENGTH,
        "branch_factor" : BRANCH_FACTOR,
        "branch_angle"  : BRANCH_ANGLE,
        "branch_damp"   : BRANCH_DAMP,
        "trunk_color"   : TRUNK_COLOR,
        "leaf_color"    : LEAF_COLOR,
        "init_width"    : INIT_WIDTH
    }
    return tree_factors

def init():
    """
    Initializes turtle settings and turtle window for the rest of program
    """
    t.tracer(0)
    t.screensize(WIDTH, HEIGHT)
    t.setworldcoordinates(0, 0, WIDTH, HEIGHT)
    drawStage()

def reset():
    t.clear()
    t.showturtle()
    drawStage()

def getAngle(angle):
    """
    returns new angle based on supplied angle
    """
    return angle + ((math.pi / 6) * random.random() - (math.pi / 12))

def drawSection(width, base_angle, angle, mid_x, y, factors):
    """
    returns new avg. x position
    """
    t.color(factors["trunk_color"])

    x = mid_x + (factors["sec_length"] * math.sin(angle + base_angle))
    y_p = y + (factors["sec_length"] * math.cos(angle + base_angle))
    width_p = width - factors["damp_factor"]

    points = [
        (mid_x - width * math.cos(base_angle), y + width * math.sin(base_angle)),
        (mid_x + width * math.cos(base_angle), y - width * math.sin(base_angle)),
        (x + width_p * math.cos(base_angle), y_p - width_p * math.sin(base_angle)),
        (x - width_p * math.cos(base_angle), y_p + width_p * math.sin(base_angle))
    ]
    t.penup()
    t.setpos(points[0][0], points[0][1])
    t.begin_fill()
    for point in points:
        t.setpos(point[0], point[1])
    t.end_fill()
    return x, y_p

def drawStage():
    """
    Draws the ground for the tree to live on
    """
    t.penup()
    t.left(90)
    t.setpos(20, 20)
    t.pendown()
    t.setpos(WIDTH - 20, 20)

def drawLeaf(x, y, angle, color):
    """
    Draws a predefined leaf shape at the given x, y position and at the given
    angle.
    """
    t.color(color)

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

def drawTree(x, y, width, angle, tree_factors):
    """
    Draws a tree growing from (x, y) with defined starting width.
    Provided angle is the base angle for the rest of the tree.
    Function uses recursive calls with changes to the angle as a way of
    drawing branches
    """
    base_angle = angle
    max_angle = angle + math.pi / 4
    min_angle = angle - math.pi / 4
    while width > 0:
        x, y = drawSection(width, base_angle, angle, x, y, tree_factors)
        width -= tree_factors["damp_factor"]
        angle = getAngle(angle)

        if angle < min_angle:
            angle = min_angle
        elif angle > max_angle:
            angle = max_angle
        if (y > 20) and (y < HEIGHT) and (x > 0) and (x < WIDTH):
            left_branch = random.random()
            right_branch = random.random()
            if 0 < left_branch < tree_factors["branch_factor"]:
                drawTree(x, y, width * tree_factors["branch_damp"], angle + tree_factors["branch_angle"], tree_factors)
            if 0 < right_branch < tree_factors["branch_factor"]:
                drawTree(x, y, width * tree_factors["branch_damp"], angle - tree_factors["branch_angle"], tree_factors)

    drawLeaf(x, y, angle, tree_factors["leaf_color"])

def main():
    init()
    while True:
        reset()
        factors = getTreeFactors()
        drawTree(WIDTH / 2, 20, factors["init_width"], 0, factors)
        t.hideturtle()
        t.update()
        print("turtle updated")
        time.sleep(3)

if __name__ == "__main__":
    main()