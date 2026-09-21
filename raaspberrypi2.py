# ============================================================
# RASPBERRY PI SENSE HAT MAZE GAME
# Tilt-Controlled 8x8 LED Maze
# ============================================================

from sense_hat import SenseHat
import time


# ============================================================
# SETUP
# ============================================================

sense = SenseHat()
sense.clear()

# ============================================================
# GAME SETTINGS
# ============================================================

MAX_LIVES = 5

TILT_THRESHOLD = 0.35

MOVE_DELAY = 0.25

# ============================================================
# COLOURS
# ============================================================

BLACK = (0, 0, 0)

BLUE = (0, 0, 255)

GREEN = (0, 255, 0)

RED = (255, 0, 0)

YELLOW = (255, 255, 0)

WHITE = (255, 255, 255)

CYAN = (0, 255, 255)


# ============================================================
# MAZE
# ============================================================
#
# # = wall
# . = empty path
# P = player
# F = finish
#
# IMPORTANT:
# The maze MUST be exactly 8 x 8.
#
# ============================================================

maze = [
    "########",
    "#P.....#",
    "######.#",
    "#......#",
    "#.######",
    "#......#",
    "#.######",
    "#.....F#"
]

# ============================================================
# FIND PLAYER AND FINISH
# ============================================================

def find_positions():

    global player_row
    global player_col

    global finish_row
    global finish_col

    for row in range(8):

        for col in range(8):

            if maze[row][col] == "P":

                player_row = row
                player_col = col

            elif maze[row][col] == "F":

                finish_row = row
                finish_col = col


# ============================================================
# GAME VARIABLES
# ============================================================

player_row = 0
player_col = 0

finish_row = 0
finish_col = 0

lives = MAX_LIVES

score = 0

moves = 0

game_over = False

game_won = False


# ============================================================
# DISPLAY MAZE ON SENSE HAT
# ============================================================

def display_maze():

    pixels = []

    for row in range(8):

        for col in range(8):

            # ----------------------------------------------
            # PLAYER
            # ----------------------------------------------

            if row == player_row and col == player_col:

                pixels.append(GREEN)

            # ----------------------------------------------
            # FINISH
            # ----------------------------------------------

            elif row == finish_row and col == finish_col:

                pixels.append(YELLOW)

            # ----------------------------------------------
            # WALL
            # ----------------------------------------------

            elif maze[row][col] == "#":

                pixels.append(BLUE)

            # ----------------------------------------------
            # EMPTY PATH
            # ----------------------------------------------

            else:

                pixels.append(BLACK)

    sense.set_pixels(pixels)


# ============================================================
# SHOW START SCREEN
# ============================================================

def start_screen():

    # Green flash

    for i in range(2):

        sense.clear(GREEN)

        time.sleep(0.25)

        sense.clear(BLACK)

        time.sleep(0.25)

    display_maze()


# ============================================================
# SHOW LIVES
# ============================================================

def show_lives():

    # Show lives briefly using the top row.

    sense.clear()

    for i in range(lives):

        if i < 8:

            sense.set_pixel(
                i,
                0,
                RED
            )

    time.sleep(0.8)

    display_maze()


# ============================================================
# WALL COLLISION
# ============================================================

def hit_wall():

    global lives
    global score

    lives -= 1

    # Lose points
    score = max(0, score - 10)

    # Flash red

    sense.clear(RED)

    time.sleep(0.2)

    display_maze()

    time.sleep(0.2)

    # Terminal is ONLY for status/debugging
    print("Wall hit!")
    print("Lives:", lives)
    print("Score:", score)


# ============================================================
# MOVE PLAYER
# ============================================================

def move_player(direction):

    global player_row
    global player_col

    global moves
    global score

    global game_won

    new_row = player_row
    new_col = player_col


    # ========================================================
    # CALCULATE NEW POSITION
    # ========================================================

    if direction == "UP":

        new_row -= 1

    elif direction == "DOWN":

        new_row += 1

    elif direction == "LEFT":

        new_col -= 1

    elif direction == "RIGHT":

        new_col += 1


    # ========================================================
    # CHECK BOUNDARY
    # ========================================================

    if (
        new_row < 0
        or new_row >= 8
        or new_col < 0
        or new_col >= 8
    ):

        hit_wall()

        return

    
    # ========================================================
    # CHECK WALL
    # ========================================================

    if maze[new_row][new_col] == "#":

        hit_wall()

        return


    # ========================================================
    # MOVE PLAYER
    # ========================================================

    player_row = new_row

    player_col = new_col

    moves += 1

    score += 10


    # ========================================================
    # CHECK FINISH
    # ========================================================

    if (
        player_row == finish_row
        and player_col == finish_col
    ):

        game_won = True

        return


    # Update LEDs
    display_maze()


# ============================================================
# READ TILT SENSOR
# ============================================================

def get_direction():

    acceleration = sense.get_accelerometer_raw()

    x = acceleration["x"]

    y = acceleration["y"]


    # ========================================================
    # HORIZONTAL TILT
    # ========================================================

    if abs(x) > abs(y):

        if x > TILT_THRESHOLD:

            return "RIGHT"

        elif x < -TILT_THRESHOLD:

            return "LEFT"


    # ========================================================
    # VERTICAL TILT
    # ========================================================

    else:

        if y > TILT_THRESHOLD:

            return "DOWN"

        elif y < -TILT_THRESHOLD:

            return "UP"


    return None


# ============================================================
# WAIT FOR SENSOR TO RETURN TO CENTRE
# ============================================================

def wait_for_neutral():

    while True:

        acceleration = sense.get_accelerometer_raw()

        x = acceleration["x"]

        y = acceleration["y"]

        if (
            abs(x) < 0.20
            and abs(y) < 0.20
        ):

            break

        time.sleep(0.05)


# ============================================================
# WIN ANIMATION
# ============================================================

def win_animation():

    # Green and yellow flashing

    for i in range(4):

        sense.clear(GREEN)

        time.sleep(0.2)

        sense.clear(YELLOW)

        time.sleep(0.2)

    sense.clear()

    # Simple check mark

    check = [

        BLACK, BLACK, BLACK, BLACK,
        BLACK, BLACK, GREEN, BLACK,

        BLACK, BLACK, BLACK, BLACK,
        BLACK, GREEN, BLACK, BLACK,

        BLACK, BLACK, BLACK, GREEN,
        BLACK, BLACK, BLACK, BLACK,

        BLACK, BLACK, GREEN, BLACK,
        BLACK, BLACK, BLACK, BLACK,

        BLACK, GREEN, BLACK, BLACK,
        BLACK, BLACK, BLACK, BLACK,

        GREEN, BLACK, BLACK, BLACK,
        BLACK, BLACK, BLACK, BLACK,

        BLACK, BLACK, BLACK, BLACK,
BLACK, BLACK, BLACK, BLACK,

        BLACK, BLACK, BLACK, BLACK,
        BLACK, BLACK, BLACK, BLACK
    ]

    sense.set_pixels(check)

    time.sleep(2)


# ============================================================
# GAME OVER ANIMATION
# ============================================================

def lose_animation():

    for i in range(3):

        sense.clear(RED)

        time.sleep(0.25)

        sense.clear(BLACK)

        time.sleep(0.25)

    time.sleep(1)


# ============================================================
# MAIN GAME
# ============================================================

def main():

    global lives
    global score
    global moves
    global game_over
    global game_won

    # --------------------------------------------------------
    # RESET GAME
    # --------------------------------------------------------

    lives = MAX_LIVES

    score = 0

    moves = 0

    game_over = False

    game_won = False


    # --------------------------------------------------------
    # Find positions
    # --------------------------------------------------------

    find_positions()


    # --------------------------------------------------------
    # Start screen
    # --------------------------------------------------------

    start_screen()

    print("================================")
    print("   RASPBERRY PI MAZE GAME")
    print("================================")
    print("Tilt the Sense HAT to move!")
    print("Lives:", lives)
    print("================================")


    # --------------------------------------------------------
    # GAME LOOP
    # --------------------------------------------------------

    while not game_over and not game_won:

        # Check if player has no lives

        if lives <= 0:

            game_over = True

            break


        # ----------------------------------------------------
        # Read tilt
        # ----------------------------------------------------

        direction = get_direction()


        # ----------------------------------------------------
        # Move player
        # ----------------------------------------------------

        if direction is not None:

            move_player(direction)

            # Prevent one long tilt from moving
            # the player repeatedly.

            wait_for_neutral()

            time.sleep(MOVE_DELAY)


        time.sleep(0.05)


    # ========================================================
    # GAME FINISHED
    # ========================================================

    if game_won:

        print()
        print("🎉 YOU WIN!")
        print("Score:", score)
        print("Moves:", moves)
        print("Lives remaining:", lives)

        win_animation()


    elif game_over:

        print()
        print("GAME OVER")
        print("Final score:", score)

        lose_animation()


# ============================================================
# RUN GAME
# ============================================================

try:

    main()

except KeyboardInterrupt:

    print("Game stopped.")

finally:

    sense.clear()