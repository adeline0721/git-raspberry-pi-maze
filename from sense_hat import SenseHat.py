
import time


# ============================================================
# MAZE GAME - SENSE HAT TILT CONTROL
# ============================================================

# Colours
WALL = (255, 255, 255)
PATH = (0, 0, 0)
PLAYER = (0, 0, 255)
GOAL = (0, 255, 0)
HEART = (255, 0, 0)
TEXT = (255, 255, 255)

# ============================================================
# 8 x 8 MAZE
#
# # = wall
# . = path
# P = player starting position
# G = goal
# ============================================================

maze = [
    "########",
    "#P.....#",
    "#####..#",
    "#.....##",
    "#.######",
    "#......#",
    "#.####.#",
    "#.....G#"
]

# Find player and goal positions
player_x = 1
player_y = 1

goal_x = 6
goal_y = 7

# Number of lives
lives = 3

# ============================================================
# DRAW MAZE
# ============================================================

def draw_maze():
    sense.clear()

    for y in range(8):
        for x in range(8):

            if maze[y][x] == "#":
                sense.set_pixel(x, y, WALL)

            elif x == player_x and y == player_y:
                sense.set_pixel(x, y, PLAYER)

            elif x == goal_x and y == goal_y:
                sense.set_pixel(x, y, GOAL)

            else:
                sense.set_pixel(x, y, PATH)


# ============================================================
# SHOW LIVES
# ============================================================

def show_lives():
    sense.clear()

    # Display 3 hearts across the top
    heart_pattern = [
        (1, 1), (2, 1),
        (0, 2), (1, 2), (2, 2), (3, 2),
        (1, 3), (2, 3)
    ]

    for life in range(lives):
        offset = life * 3

        for x, y in heart_pattern:
            if x + offset < 8:
                sense.set_pixel(
                    x + offset,
                    y,
                    HEART
                )

    time.sleep(1)

    draw_maze()


# ============================================================
# CHECK WHETHER POSITION IS VALID
# ============================================================

def can_move(x, y):

    # Outside the 8x8 grid
    if x < 0 or x > 7 or y < 0 or y > 7:
        return False

    # Wall
    if maze[y][x] == "#":
        return False

    return True


# ============================================================
# RESET PLAYER
# ============================================================

def reset_player():
    global player_x, player_y

    player_x = 1
    player_y = 1

    draw_maze()


# ============================================================
# WIN SCREEN
# ============================================================

def win_game():

    sense.clear(GOAL)

    time.sleep(0.5)

    sense.show_message(
        "YOU WIN!",
        text_colour=GOAL,
        scroll_speed=0.08
    )

    sense.clear()

    # Flash the entire screen
    for i in range(3):
        sense.clear(GOAL)
        time.sleep(0.3)

        sense.clear()
        time.sleep(0.3)


# ============================================================
# GAME OVER
# ============================================================

def game_over():

    sense.clear(HEART)

    time.sleep(0.5)

    sense.show_message(
        "GAME OVER",
        text_colour=HEART,
        scroll_speed=0.08
    )

    sense.clear()


# ============================================================
# MAIN GAME
# ============================================================

draw_maze()

last_move_time = 0

while lives > 0:

    # --------------------------------------------------------
    # READ ACCELEROMETER
    # --------------------------------------------------------

    acceleration = sense.get_accelerometer_raw()

    x = acceleration["x"]
    y = acceleration["y"]

    # --------------------------------------------------------
    # MOVEMENT COOLDOWN
    #
    # Prevents the ball from moving MANY spaces at once
    # when the Sense HAT is tilted.
    # --------------------------------------------------------

    current_time = time.time()

    if current_time - last_move_time < 0.35:
        time.sleep(0.05)
        continue

    new_x = player_x
    new_y = player_y

    # --------------------------------------------------------
    # TILT RIGHT
    # --------------------------------------------------------

    if x > 0.45:
        new_x += 1

    # --------------------------------------------------------
    # TILT LEFT
    # --------------------------------------------------------

    elif x < -0.45:
        new_x -= 1

    # --------------------------------------------------------
    # TILT FORWARD
    # --------------------------------------------------------

    elif y > 0.45:
        new_y += 1

    # --------------------------------------------------------
    # TILT BACKWARD
    # --------------------------------------------------------

    elif y < -0.45:
        new_y -= 1

    # --------------------------------------------------------
    # TRY TO MOVE
    # --------------------------------------------------------

    if new_x != player_x or new_y != player_y:

        last_move_time = current_time

        if can_move(new_x, new_y):

            player_x = new_x
            player_y = new_y

            draw_maze()

            # ------------------------------------------------
            # CHECK GOAL
            # ------------------------------------------------

            if player_x == goal_x and player_y == goal_y:
                win_game()
                break

        else:

            # Hit a wall
            lives -= 1

            # Flash red
            sense.clear(HEART)
            time.sleep(0.2)

            if lives > 0:
                show_lives()
                reset_player()

            else:
                game_over()

    time.sleep(0.05)

sense.clear()