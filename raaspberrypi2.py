# ============================================================
# 🍓 RASPBERRY PI SENSE HAT MAZE ADVENTURE
# ============================================================
#
# Tilt-controlled maze game using:
#   • Raspberry Pi
#   • Sense HAT LED matrix
#   • Sense HAT accelerometer
#   • Sense HAT joystick
#
# ============================================================

from sense_hat import SenseHat
import time


# ============================================================
# INITIALISE SENSE HAT
# ============================================================

sense = SenseHat()
sense.low_light = False


# ============================================================
# GAME SETTINGS
# ============================================================

MAX_LIVES = 5

TILT_THRESHOLD = 0.35
NEUTRAL_THRESHOLD = 0.18
CALIBRATION_SAMPLES = 30
MOVE_COOLDOWN = 0.20


# ============================================================
# COLOURS
# ============================================================

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 100, 0)


# ============================================================
# MAZE SYMBOLS
# ============================================================

WALL = "#"
PATH = "."
PLAYER = "P"
FINISH = "F"


# ============================================================
# 🗺️ MAZE
# ============================================================
#
# EXACT 8 x 8 MAP
#
# # = wall
# . = empty/path
# P = player
# F = finish
#
# Board layout:
#
# ########
# #P..#..#
# ###.#.##
# #......#
# #.####.#
# #....#.#
# ####.#.#
# ####..F#
#
# ============================================================

LEVELS = [

    {
        "name": "MAZE",
        "maze": [
            "########",
            "#P..#..#",
            "###.#.##",
            "#......#",
            "#.####.#",
            "#....#.#",
            "####.#.#",
            "####..F#"
        ],
        "time_limit": 180
    }

]


# ============================================================
# GAME VARIABLES
# ============================================================

current_level = 0

maze = []

player_row = 0
player_col = 0

finish_row = 0
finish_col = 0

lives = MAX_LIVES
score = 0
moves = 0

start_time = 0

paused = False


# ============================================================
# SENSOR CALIBRATION
# ============================================================

x_offset = 0
y_offset = 0


def calibrate_sensor():

    global x_offset
    global y_offset

    sense.clear()

    # Calibration indicator
    sense.set_pixel(3, 3, CYAN)
    sense.set_pixel(4, 3, CYAN)
    sense.set_pixel(3, 4, CYAN)
    sense.set_pixel(4, 4, CYAN)

    time.sleep(1)

    x_total = 0
    y_total = 0

    for _ in range(CALIBRATION_SAMPLES):

        acceleration = sense.get_accelerometer_raw()

        x_total += acceleration["x"]
        y_total += acceleration["y"]

        time.sleep(0.03)

    x_offset = x_total / CALIBRATION_SAMPLES
    y_offset = y_total / CALIBRATION_SAMPLES

    sense.clear()

    # Calibration complete
    for _ in range(2):

        sense.clear(GREEN)
        time.sleep(0.15)

        sense.clear(BLACK)
        time.sleep(0.15)


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

            if maze[row][col] == PLAYER:

                player_row = row
                player_col = col

            elif maze[row][col] == FINISH:

                finish_row = row
                finish_col = col


# ============================================================
# LOAD MAZE
# ============================================================

def load_level(level_number):

    global current_level
    global maze

    current_level = level_number

    maze = LEVELS[level_number]["maze"].copy()

    find_positions()


# ============================================================
# DRAW MAZE ON 8 x 8 LED BOARD
# ============================================================

def draw_maze():

    pixels = []

    for row in range(8):

        for col in range(8):

            # PLAYER = GREEN
            if row == player_row and col == player_col:

                pixels.append(GREEN)

            # FINISH = YELLOW
            elif row == finish_row and col == finish_col:

                pixels.append(YELLOW)

            # WALL = BLUE
            elif maze[row][col] == WALL:

                pixels.append(BLUE)

            # EMPTY PATH = BLACK
            else:

                pixels.append(BLACK)

    sense.set_pixels(pixels)


# ============================================================
# SHOW MAZE AT START
# ============================================================

def show_level_intro():

    for _ in range(2):

        sense.clear(GREEN)
        time.sleep(0.25)

        sense.clear(BLACK)
        time.sleep(0.25)

    draw_maze()

    time.sleep(1)


# ============================================================
# ❤️ SHOW LIVES
# ============================================================

def show_lives():

    sense.clear()

    for x in range(lives):

        sense.set_pixel(
            x,
            0,
            RED
        )

    time.sleep(0.7)

    draw_maze()


# ============================================================
# 💥 HIT WALL
# ============================================================

def hit_wall():

    global lives
    global score

    lives -= 1

    score = max(0, score - 50)

    print("Wall hit!")
    print("Lives:", lives)
    print("Score:", score)

    # Red flash
    for _ in range(2):

        sense.clear(RED)
        time.sleep(0.15)

        draw_maze()
        time.sleep(0.15)

    if lives > 0:

        show_lives()


# ============================================================
# GET ACCELEROMETER DATA
# ============================================================

def get_acceleration():

    acceleration = sense.get_accelerometer_raw()

    x = acceleration["x"] - x_offset
    y = acceleration["y"] - y_offset

    return x, y


# ============================================================
# GET TILT DIRECTION
# ============================================================

def get_direction():

    x, y = get_acceleration()

    # Use the stronger tilt direction
    if abs(x) > abs(y):

        if x > TILT_THRESHOLD:
            return "RIGHT"

        elif x < -TILT_THRESHOLD:
            return "LEFT"

    else:

        if y > TILT_THRESHOLD:
            return "DOWN"

        elif y < -TILT_THRESHOLD:
            return "UP"

    return None


# ============================================================
# WAIT UNTIL BOARD IS NEUTRAL
# ============================================================

def wait_for_neutral():

    while True:

        x, y = get_acceleration()

        if (
            abs(x) < NEUTRAL_THRESHOLD
            and abs(y) < NEUTRAL_THRESHOLD
        ):

            return

        time.sleep(0.05)


# ============================================================
# MOVE PLAYER
# ============================================================

def move_player(direction):

    global player_row
    global player_col
    global moves
    global score

    new_row = player_row
    new_col = player_col

    # Calculate new position

    if direction == "UP":

        new_row -= 1

    elif direction == "DOWN":

        new_row += 1

    elif direction == "LEFT":

        new_col -= 1

    elif direction == "RIGHT":

        new_col += 1


    # ========================================================
    # CHECK BOARD BOUNDARY
    # ========================================================

    if new_row < 0 or new_row >= 8:

        hit_wall()
        return False

    if new_col < 0 or new_col >= 8:

        hit_wall()
        return False


    # ========================================================
    # CHECK BLUE WALL
    # ========================================================

    if maze[new_row][new_col] == WALL:

        hit_wall()
        return False


    # ========================================================
    # MOVE PLAYER
    # ========================================================

    player_row = new_row
    player_col = new_col

    moves += 1
    score += 10

    print(
        "Player:",
        "row", player_row,
        "column", player_col
    )


    # ========================================================
    # CHECK FINISH
    # ========================================================

    if (
        player_row == finish_row
        and player_col == finish_col
    ):

        return True


    # Update LED board
    draw_maze()

    return False


# ============================================================
# 🏆 LEVEL SCORE
# ============================================================

def calculate_level_score():

    elapsed = time.time() - start_time

    base = 500

    time_bonus = max(
        0,
        int(300 - elapsed * 3)
    )

    life_bonus = lives * 100

    move_bonus = max(
        0,
        200 - moves * 5
    )

    return (
        base
        + time_bonus
        + life_bonus
        + move_bonus
    )


# ============================================================
# 🎉 LEVEL COMPLETE
# ============================================================

def level_complete():

    global score

    level_score = calculate_level_score()

    score += level_score

    print("🎉 MAZE COMPLETE!")
    print("Moves:", moves)
    print("Level score:", level_score)
    print("Total score:", score)

    # Celebration
    for _ in range(3):

        sense.clear(GREEN)
        time.sleep(0.2)

        sense.clear(YELLOW)
        time.sleep(0.2)

    # Show finish position
    sense.set_pixel(
        finish_col,
        finish_row,
        GREEN
    )

    time.sleep(1)


# ============================================================
# 🏆 FINAL VICTORY
# ============================================================

def final_victory():

    for _ in range(3):

        sense.clear(GREEN)
        time.sleep(0.25)

        sense.clear(CYAN)
        time.sleep(0.25)

        sense.clear(YELLOW)
        time.sleep(0.25)


    # Checkmark
    checkmark = [

        BLACK, BLACK, BLACK, BLACK,
        BLACK, BLACK, GREEN, BLACK,

        BLACK, BLACK, BLACK, BLACK,
        BLACK, GREEN, BLACK, BLACK,

        BLACK, BLACK, BLACK, BLACK,
        GREEN, BLACK, BLACK, BLACK,

        BLACK, BLACK, BLACK, GREEN,
        BLACK, BLACK, BLACK, BLACK,

        BLACK, BLACK, GREEN, BLACK,
        BLACK, BLACK, BLACK, BLACK,

        BLACK, GREEN, BLACK, BLACK,
        BLACK, BLACK, BLACK, BLACK,

        GREEN, BLACK, BLACK, BLACK,
        BLACK, BLACK, BLACK, BLACK,

        BLACK, BLACK, BLACK, BLACK,
        BLACK, BLACK, BLACK, BLACK

    ]

    sense.set_pixels(checkmark)

    print("🏆 YOU WON!")
    print("Final score:", score)

    time.sleep(2)


# ============================================================
# 💔 GAME OVER
# ============================================================

def game_over_screen():

    print("GAME OVER")

    for _ in range(3):

        sense.clear(RED)
        time.sleep(0.3)

        sense.clear(BLACK)
        time.sleep(0.3)


    # X pattern

    x_pattern = [

        RED, BLACK, BLACK, BLACK,
        BLACK, BLACK, BLACK, RED,

        BLACK, RED, BLACK, BLACK,
        BLACK, BLACK, RED, BLACK,

        BLACK, BLACK, RED, BLACK,
        BLACK, RED, BLACK, BLACK,

        BLACK, BLACK, BLACK, RED,
        RED, BLACK, BLACK, BLACK,

        BLACK, BLACK, BLACK, RED,
        RED, BLACK, BLACK, BLACK,

        BLACK, BLACK, RED, BLACK,
        BLACK, RED, BLACK, BLACK,

        BLACK, RED, BLACK, BLACK,
        BLACK, BLACK, RED, BLACK,

        RED, BLACK, BLACK, BLACK,
        BLACK, BLACK, BLACK, RED

    ]

    sense.set_pixels(x_pattern)

    time.sleep(2)


# ============================================================
# ⏸️ PAUSE GAME
# ============================================================

def pause_game():

    global paused

    paused = True

    sense.clear(MAGENTA)

    time.sleep(0.5)

    while paused:

        event = sense.stick.get_event()

        if event is not None:

            if event.action == "pressed":

                if event.direction == "middle":

                    paused = False

        time.sleep(0.05)

    draw_maze()


# ============================================================
# 🎮 START MENU
# ============================================================

def start_menu():

    print("================================")
    print("🍓 SENSE HAT MAZE")
    print("================================")
    print("Tilt the Sense HAT to move.")
    print("Press the joystick to pause.")
    print("You have 5 lives.")
    print("================================")

    for _ in range(2):

        sense.clear(GREEN)
        time.sleep(0.2)

        sense.clear(BLACK)
        time.sleep(0.2)

    return 0


# ============================================================
# 🎮 PLAY MAZE
# ============================================================

def play_level(level_number):

    global lives
    global moves
    global start_time

    # Load exact maze
    load_level(level_number)

    # Display maze
    show_level_intro()

    start_time = time.time()
    moves = 0

    while True:

        # ====================================================
        # CHECK LIVES
        # ====================================================

        if lives <= 0:

            game_over_screen()

            return False


        # ====================================================
        # CHECK TIMER
        # ====================================================

        elapsed = time.time() - start_time

        time_limit = LEVELS[level_number]["time_limit"]

        if elapsed >= time_limit:

            lives -= 1

            print("Time is up!")
            print("Lives:", lives)

            if lives <= 0:

                game_over_screen()

                return False

            # Restart the SAME maze
            load_level(level_number)

            start_time = time.time()

            show_lives()

            continue


        # ====================================================
        # CHECK JOYSTICK
        # ====================================================

        event = sense.stick.get_event()

        if event is not None:

            if event.action == "pressed":

                if event.direction == "middle":

                    pause_game()

                    continue


        # ====================================================
        # GET TILT
        # ====================================================

        direction = get_direction()


        # ====================================================
        # MOVE
        # ====================================================

        if direction is not None:

            finished = move_player(direction)

            # Wait for tilt to return to neutral
            wait_for_neutral()

            time.sleep(MOVE_COOLDOWN)

            # =================================================
            # FINISHED
            # =================================================

            if finished:

                level_complete()

                return True


        time.sleep(0.05)


# ============================================================
# 🚀 RUN GAME
# ============================================================

def run_game():

    global lives
    global score

    lives = MAX_LIVES
    score = 0

    # Calibrate while Sense HAT is flat
    calibrate_sensor()

    # Start
    selected_level = start_menu()

    # Play exact maze
    completed = play_level(selected_level)

    if completed:

        final_victory()


# ============================================================
# ▶️ PROGRAM START
# ============================================================

try:

    run_game()

except KeyboardInterrupt:

    print("Game stopped.")

finally:

    sense.clear()