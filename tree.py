import turtle as t
import random
import math
import time

WIDTH = 640
HEIGHT = 480

def random_range(top):
    return ((random.random() + 1) / 2) * top

def get_random_tree_factors():
    # How much the width of the tree should be reduced between each section
    DAMP_FACTOR = random.randint(1, 3)

    # How long ("tall") each section of the tree is
    SEC_LENGTH = random.randint(10, 30)

    # Scaling factor for the width + length of branches
    BRANCH_FACTOR = random_range(.15) + 0.05

    # What angle the branch should have relative to its parent
    BRANCH_ANGLE = random_range(math.pi / 3)
    BRANCH_DAMP = random_range(0.3) + 0.4

    TRUNK_COLOR = (random.random(), random.random(), random.random())
    LEAF_COLOR = (random.random(), random.random(), random.random())
    GROUND_COLOR = (random.random(), random.random(), random.random())

    INIT_WIDTH = random.randint(20, 70)
    
    tree_factors = {
        "damp_factor"   : DAMP_FACTOR,
        "sec_length"    : SEC_LENGTH,
        "branch_factor" : BRANCH_FACTOR,
        "branch_angle"  : BRANCH_ANGLE,
        "branch_damp"   : BRANCH_DAMP,
        "trunk_color"   : TRUNK_COLOR,
        "leaf_color"    : LEAF_COLOR,
        "ground_color"  : GROUND_COLOR,
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

def reset(color):
    """
    Resets the stage in preparation for the next tree to be drawn
    """
    t.clear()
    t.showturtle()
    draw_stage(color)

def get_branch_angle(tree_angle):
    return (random.random() * (tree_angle/4)) + tree_angle

def get_adjusted_angle(angle):
    """
    returns new angle based on supplied angle
    """
    angle += ((math.pi / 6) * random.random() - (math.pi / 12))
    if angle < 0:
        angle = angle + random_range(math.pi / 16)
    elif angle > 0:
        angle = angle - random_range(math.pi / 16)
    return angle

def draw_section(width, base_angle, angle, mid_x, y, factors):
    """
    width -> 1/2 base width of section
    base_angle -> 
    angle -> 
    mid_x -> x coord of the center of the section to draw
    returns new avg. x position
    """
    t.color(factors["trunk_color"])

    x = mid_x + (factors["sec_length"] * math.sin(angle + base_angle))
    y_p = y + (factors["sec_length"] * math.cos(angle + base_angle))
    width_p = width - factors["damp_factor"]
    if width_p < 0:
        width_p = 0

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

def draw_stage(color):
    """
    Draws the ground for the tree to live on using the randomly generated
    ground color for this tree.
    """
    t.penup()
    t.left(90)
    t.color(color)
    t.setpos(20, 20)
    t.pendown()
    t.setpos(WIDTH - 20, 20)

def draw_leaf(x, y, angle, color):
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

def draw_tree(x, y, width, angle, tree_factors):
    """
    Draws a tree growing from (x, y) with defined starting width.
    Provided angle is the base angle for the rest of the tree.
    Function uses recursive calls with changes to the angle as a way of
    drawing branches.
    """

    # TODO: Rewrite to be fully recursive rather than utilizing while loop

    branch_prob = 0
    base_angle = angle
    while width > 0:
        # If we are still on the screen...
        if (0 < x < WIDTH and 10 < y < HEIGHT):
            # Decide if branches should be drawn and draw them
            if (y > 20) and (y < HEIGHT) and (x > 0) and (x < WIDTH):
                left_branch = random.random()
                right_branch = random.random()
                branch_made = False
                if 0 < left_branch < branch_prob:
                    branch_made = True
                    branch_factors = dict(tree_factors)
                    branch_factors["sec_length"] = tree_factors["branch_damp"] * tree_factors["sec_length"]
                    draw_tree(x + width / 2, y, width * tree_factors["branch_damp"], get_branch_angle(angle + tree_factors["branch_angle"]), branch_factors)
                if 0 < right_branch < branch_prob:
                    branch_made = True
                    branch_factors = dict(tree_factors)
                    branch_factors["sec_length"] = tree_factors["branch_damp"] * tree_factors["sec_length"]
                    draw_tree(x - width / 2, y, width * tree_factors["branch_damp"], get_branch_angle(angle - tree_factors["branch_angle"]), branch_factors)
                if branch_made:
                    branch_prob = 0
            
            # Draw the current section
            x, y = draw_section(width, base_angle, angle, x, y, tree_factors)

            # Decrease the width of the next tree section
            width -= tree_factors["damp_factor"]
            
            # Randomly adjust the angle of the next tree section for organic look
            angle = get_adjusted_angle(angle)

            # Increase the probability of the next section having a branch
            branch_prob += tree_factors["branch_factor"]

        else:
            break
    # Draws the leaf at original angle of branch to prevent random leaf angles looking weird
    draw_leaf(x, y, base_angle, tree_factors["leaf_color"])
    # Draw the completed branch. Nice visual + helps debugging
    t.update()

def main():
    init()
    # TODO: Add user control over progressing to the next tree
    while True:
        factors = get_random_tree_factors()
        reset(factors["ground_color"])
        draw_tree(WIDTH / 2, 20, factors["init_width"], 0, factors)
        t.hideturtle()
        t.update()
        print("turtle updated")
        time.sleep(3)

if __name__ == "__main__":
    main()