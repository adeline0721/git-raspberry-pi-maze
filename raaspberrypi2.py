# ============================================================
# 🍓 RASPBERRY PI MAZE ADVENTURE
# Tilt-Controlled LED Ball Maze
#
# Developed as a Raspberry Pi Project
#
# TEST_MODE = True
#     → Run on Windows using keyboard
#
# TEST_MODE = False
#     → Run on Raspberry Pi using MPU6050 sensor
# ============================================================

import time
import os
# ============================================================
# 🎮 GAME SETTINGS
# ============================================================

# ------------------------------------------------------------
# IMPORTANT
# ------------------------------------------------------------
# True  = Test on your Windows computer
# False = Run on Raspberry Pi
# ------------------------------------------------------------

TEST_MODE = True
# Number of lives
MAX_LIVES = 3

# Sensor sensitivity
SENSOR_THRESHOLD = 0.35

# Delay between movements
MOVE_DELAY = 0.25
# ============================================================
# 🎨 TERMINAL COLOURS
# ============================================================
RESET = "\033[0m"
BOLD = "\033[1m"

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
GRAY = "\033[90m"
# ============================================================
# 🍓 RASPBERRY PI HARDWARE
# ============================================================

if not TEST_MODE:

    from gpiozero import LED
    from smbus2 import SMBus

    # --------------------------------------------------------
    # MPU6050
    # --------------------------------------------------------

    MPU6050_ADDRESS = 0x68

    PWR_MGMT_1 = 0x6B

    ACCEL_XOUT_H = 0x3B
    ACCEL_YOUT_H = 0x3D

    # I2C bus
    bus = SMBus(1)

    # Wake up MPU6050
    bus.write_byte_data(
        MPU6050_ADDRESS,
        PWR_MGMT_1,
        0)
# --------------------------------------------------------
    # LED PINS
    # --------------------------------------------------------

    GREEN_LED_PIN = 17
    RED_LED_PIN = 27
    BLUE_LED_PIN = 22

    green_led = LED(GREEN_LED_PIN)
    red_led = LED(RED_LED_PIN)
    blue_led = LED(BLUE_LED_PIN)


else:
 # ========================================================
    # 💻 FAKE LEDs FOR COMPUTER TESTING
    # ========================================================

    class FakeLED:

        def on(self):
            pass

        def off(self):
            pass

        def blink(self):
            pass


    green_led = FakeLED()
    red_led = FakeLED()
    blue_led = FakeLED()

# ============================================================
# 🧩 MAZE LEVELS
# ============================================================

LEVEL_1 = [
    "############################",
    "#P                         #",
    "# ####### ################ #",
    "#       #                  #",
    "####### ################# #",
    "#                         #",
    "# ####################### #",
    "#                         #",
    "# ####################### #",
    "#                       F #",
    "############################"
]


LEVEL_2 = [
    "############################",
    "#P       #                #",
    "# ###### # ############## #",
    "#      # #              # #",
    "###### # ################ #",
    "#      #                  #",
    "# ###################### #",
    "#                        #",
    "# ####################### #",
    "#                       F#",
    "############################"
]


LEVEL_3 = [
    "############################",
    "#P     #       #          #",
    "##### # ##### # ######### #",
    "#     #     # #           #",
    "# ######### # ########### #",
    "#         # #             #",
    "######### # ############# #",
    "#         #               #",
    "# ####################### #",
    "#                       F#",
    "############################"
]


LEVELS = [
    LEVEL_1,
    LEVEL_2,
    LEVEL_3
]


# ============================================================
# 🎮 GAME VARIABLES
# ============================================================

current_level = 0

maze = []

player_row = 0
player_col = 0

lives = MAX_LIVES

score = 0

moves = 0

start_time = 0

game_over = False


# ============================================================
# 🧹 CLEAR SCREEN
# ============================================================

def clear_screen():

    os.system("cls" if os.name == "nt" else "clear")


# ============================================================
# 🧭 FIND PLAYER
# ============================================================

def find_player():

    global player_row
    global player_col

    for row in range(len(maze)):

        for col in range(len(maze[row])):

            if maze[row][col] == "P":

                player_row = row
                player_col = col

                return


# ============================================================
# 📋 LOAD LEVEL
# ============================================================

def load_level(level_number):

    global maze
    global current_level

    current_level = level_number

    # Make a copy so the original level isn't changed
    maze = LEVELS[level_number].copy()

    find_player()


# ============================================================
# 🎨 PRINT TITLE
# ============================================================

def print_title():

    print()
    print(CYAN + BOLD + "╔══════════════════════════════════════════════╗" + RESET)
    print(CYAN + BOLD + "║                                              ║" + RESET)
    print(CYAN + BOLD + "║        🍓 RASPBERRY PI MAZE ADVENTURE       ║" + RESET)
    print(CYAN + BOLD + "║                                              ║" + RESET)
    print(CYAN + BOLD + "╚══════════════════════════════════════════════╝" + RESET)
    print()


# ============================================================
# 🏠 MAIN MENU
# ============================================================

def main_menu():

    while True:

        clear_screen()

        print_title()

        print(BOLD + "                    MAIN MENU" + RESET)
        print()

        print(GREEN + "       [1] " + RESET + "Start Game")
        print(BLUE + "       [2] " + RESET + "How To Play")
        print(YELLOW + "       [3] " + RESET + "About")
        print(RED + "       [4] " + RESET + "Exit")

        print()

        choice = input(
            "       Select an option: "
        ).strip()

        if choice == "1":

            return

        elif choice == "2":

            instructions()

        elif choice == "3":

            about()

        elif choice == "4":

            print()
            print("Thanks for playing! 👋")
            exit()

        else:

            print()
            print(RED + "Please select 1, 2, 3 or 4." + RESET)
            time.sleep(1)


# ============================================================
# 📖 INSTRUCTIONS
# ============================================================

def instructions():

    clear_screen()

    print_title()

    print(BOLD + "                 HOW TO PLAY" + RESET)
    print()

    print("🎯 " + BOLD + "Objective" + RESET)
    print("Guide the LED ball from the starting point")
    print("to the finish point without getting stuck.")
    print()

    print("🧱 " + BOLD + "Maze Walls" + RESET)
    print("# = Wall")
    print("P = LED Ball")
    print("F = Finish")
    print("  = Open path")
    print()

    if TEST_MODE:

        print("⌨️ " + BOLD + "Computer Controls" + RESET)
        print("W = Move Up")
        print("S = Move Down")
        print("A = Move Left")
        print("D = Move Right")

    else:

        print("📐 " + BOLD + "Sensor Controls" + RESET)
        print("Tilt the maze to control the LED ball.")

    print()

    print("❤️ You have 3 lives.")
    print("💥 Hitting a wall costs one life.")
    print("🏆 Complete the maze to earn points.")
    print()

    input("Press ENTER to return to the menu...")


# ============================================================
# ℹ️ ABOUT
# ============================================================

def about():

    clear_screen()

    print_title()

    print(BOLD + "                    ABOUT" + RESET)
    print()

    print("This project combines:")
    print()
    print("🍓 Raspberry Pi")
    print("📐 Motion / tilt sensor")
    print("💡 LEDs")
    print("🐍 Python")
    print("🧩 Physical maze")
    print()

    print(
        "The sensor detects the direction in which "
        "the maze is tilted."
    )

    print(
        "The Raspberry Pi processes the sensor data "
        "and moves the LED ball accordingly."
    )

    print()

    print("Created as a Raspberry Pi programming project.")
    print()

    input("Press ENTER to return to the menu...")


# ============================================================
# 🧱 DISPLAY MAZE
# ============================================================

def display_maze():

    clear_screen()

    print_title()

    # ========================================================
    # GAME INFORMATION
    # ========================================================

    elapsed = time.time() - start_time

    print(
        f"{CYAN}Level:{RESET} {current_level + 1}/{len(LEVELS)}    "
        f"{RED}❤️ Lives:{RESET} {lives}    "
        f"{YELLOW}⭐ Score:{RESET} {score}"
    )

    print(
        f"{MAGENTA}⏱️ Time:{RESET} {elapsed:.1f}s    "
        f"{BLUE}👣 Moves:{RESET} {moves}"
    )

    print()

    # ========================================================
    # MAZE
    # ========================================================

    print(CYAN + "      " + "━" * 28 + RESET)

    for row in maze:

        display_row = ""

        for character in row:

            if character == "#":

                # Wall
                display_row += BLUE + "█" + RESET

            elif character == "P":

                # Player / LED ball
                display_row += GREEN + "●" + RESET

            elif character == "F":

                # Finish
                display_row += YELLOW + "★" + RESET

            else:

                # Empty path
                display_row += GRAY + "·" + RESET

        print("      " + display_row)

    print(CYAN + "      " + "━" * 28 + RESET)

    print()

    # ========================================================
    # LEGEND
    # ========================================================

    print(
        f"{GREEN}●{RESET} You    "
        f"{YELLOW}★{RESET} Finish    "
        f"{BLUE}█{RESET} Wall    "
        f"{GRAY}·{RESET} Path"
    )

    print()

    if TEST_MODE:

        print(
            f"{CYAN}Controls:{RESET} "
            f"{BOLD}W{RESET} ↑   "
            f"{BOLD}A{RESET} ←   "
            f"{BOLD}S{RESET} ↓   "
            f"{BOLD}D{RESET} →   "
            f"{BOLD}Q{RESET} Quit"
        )

    else:

        print(
            f"{CYAN}Controls:{RESET} "
            f"{BOLD}Tilt the maze to move the ball{RESET}"
        )

    print()


# ============================================================
# 💥 WALL COLLISION
# ============================================================

def wall_collision():

    global lives
    global score

    lives -= 1

    # Penalty
    score = max(0, score - 50)

    red_led.on()

    print()
    print(
        RED
        + BOLD
        + "💥 WALL COLLISION!"
        + RESET
    )

    print(
        RED
        + f"❤️ Lives remaining: {lives}"
        + RESET
    )

    time.sleep(0.3)

    red_led.off()


# ============================================================
# 🏆 CALCULATE SCORE
# ============================================================

def calculate_score():

    elapsed = time.time() - start_time

    # Base points
    base_score = 1000

    # Faster completion = more points
    time_bonus = max(0, int(500 - elapsed * 5))

    # Remaining lives
    life_bonus = lives * 200

    # Fewer moves = more points
    move_bonus = max(0, 300 - moves * 5)

    total = (
        base_score
        + time_bonus
        + life_bonus
        + move_bonus
    )

    return total


# ============================================================
# 🚶 MOVE PLAYER
# ============================================================

def move_player(direction):

    global player_row
    global player_col
    global moves
    global score

    new_row = player_row
    new_col = player_col

    # --------------------------------------------------------
    # Determine new position
    # --------------------------------------------------------

    if direction == "UP":

        new_row -= 1

    elif direction == "DOWN":

        new_row += 1

    elif direction == "LEFT":

        new_col -= 1

    elif direction == "RIGHT":

        new_col += 1

    else:

        return False


    # --------------------------------------------------------
    # Safety check
    # --------------------------------------------------------

    if (
        new_row < 0
        or new_row >= len(maze)
        or new_col < 0
        or new_col >= len(maze[new_row])
    ):

        return False


    # --------------------------------------------------------
    # Check wall
    # --------------------------------------------------------

    if maze[new_row][new_col] == "#":

        wall_collision()

        return False


    # --------------------------------------------------------
    # Check finish
    # --------------------------------------------------------

    if maze[new_row][new_col] == "F":

        player_row = new_row
        player_col = new_col

        score += calculate_score()

        green_led.on()
        blue_led.on()

        return True


    # --------------------------------------------------------
    # Remove old player
    # --------------------------------------------------------

    maze[player_row] = (
        maze[player_row][:player_col]
        + " "
        + maze[player_row][player_col + 1:]
    )


    # --------------------------------------------------------
    # Update player position
    # --------------------------------------------------------

    player_row = new_row
    player_col = new_col

    moves += 1

    score += 10


    # --------------------------------------------------------
    # Add player
    # --------------------------------------------------------

    maze[player_row] = (
        maze[player_row][:player_col]
        + "P"
        + maze[player_row][player_col + 1:]
    )

    return False


# ============================================================
# ⌨️ COMPUTER CONTROLS
# ============================================================

def get_keyboard_direction():

    command = input(
        "Move: "
    ).strip().lower()

    if command == "w":

        return "UP"

    elif command == "s":

        return "DOWN"

    elif command == "a":

        return "LEFT"

    elif command == "d":

        return "RIGHT"

    elif command == "q":

        return "QUIT"

    return None


# ============================================================
# 📐 SENSOR FUNCTIONS
# ============================================================

def read_word(high_register):

    high = bus.read_byte_data(
        MPU6050_ADDRESS,
        high_register
    )

    low = bus.read_byte_data(
        MPU6050_ADDRESS,
        high_register + 1
    )

    value = (high << 8) | low

    if value >= 32768:

        value -= 65536

    return value


def read_acceleration():

    accel_x = read_word(
        ACCEL_XOUT_H
    )

    accel_y = read_word(
        ACCEL_YOUT_H
    )

    x = accel_x / 16384.0
    y = accel_y / 16384.0

    return x, y


# ============================================================
# 📐 CONVERT SENSOR DATA TO DIRECTION
# ============================================================

def get_sensor_direction(x, y):

    threshold = SENSOR_THRESHOLD

    if abs(x) > abs(y):

        if x > threshold:

            return "RIGHT"

        elif x < -threshold:

            return "LEFT"

    else:

        if y > threshold:

            return "UP"

        elif y < -threshold:

            return "DOWN"

    return None


# ============================================================
# ❤️ GAME OVER
# ============================================================

def game_over_screen():

    clear_screen()

    print()
    print(RED + BOLD)
    print("╔══════════════════════════════════════════════╗")
    print("║                                              ║")
    print("║              💔 GAME OVER                   ║")
    print("║                                              ║")
    print("╚══════════════════════════════════════════════╝")
    print(RESET)

    print()
    print(f"⭐ Final Score: {score}")
    print(f"👣 Moves: {moves}")

    print()

    input("Press ENTER to return to the menu...")


# ============================================================
# 🏆 WIN SCREEN
# ============================================================

def win_screen():

    elapsed = time.time() - start_time

    clear_screen()

    print()
    print(GREEN + BOLD)
    print("╔══════════════════════════════════════════════╗")
    print("║                                              ║")
    print("║            🎉 MAZE COMPLETE!                ║")
    print("║                                              ║")
    print("╚══════════════════════════════════════════════╝")
    print(RESET)

    print()

    print(
        GREEN
        + "🏁 Congratulations! You reached the finish!"
        + RESET
    )

    print()

    print(f"⏱️ Completion Time : {elapsed:.1f} seconds")
    print(f"👣 Total Moves     : {moves}")
    print(f"❤️ Lives Remaining : {lives}")
    print(f"⭐ Final Score     : {score}")

    print()

    # --------------------------------------------------------
    # Performance message
    # --------------------------------------------------------

    if lives == MAX_LIVES:

        print(
            GREEN
            + "✨ Perfect run! You didn't hit any walls!"
            + RESET
        )

    elif lives == 1:

        print(
            YELLOW
            + "😮 That was close! You finished with 1 life!"
            + RESET
        )

    else:

        print(
            CYAN
            + "👍 Nice job! You successfully completed the maze!"
            + RESET
        )

    print()

    input("Press ENTER to continue...")


# ============================================================
# 🎮 PLAY GAME
# ============================================================

def play_game():

    global lives
    global score
    global moves
    global start_time

    lives = MAX_LIVES
    score = 0
    moves = 0

    load_level(0)

    green_led.on()

    time.sleep(1)

    start_time = time.time()

    # --------------------------------------------------------
    # GAME LOOP
    # --------------------------------------------------------

    while True:

        # ----------------------------------------------------
        # Check lives
        # ----------------------------------------------------

        if lives <= 0:

            green_led.off()

            game_over_screen()

            return


        # ----------------------------------------------------
        # Display
        # ----------------------------------------------------

        display_maze()


        # ----------------------------------------------------
        # Get input
        # ----------------------------------------------------

        if TEST_MODE:

            direction = get_keyboard_direction()

            if direction == "QUIT":

                green_led.off()

                return

            if direction is None:

                print(
                    YELLOW
                    + "⚠️ Use W, A, S, D or Q."
                    + RESET
                )

                time.sleep(1)

                continue

        else:

            x, y = read_acceleration()

            direction = get_sensor_direction(
                x,
                y
            )

            if direction is None:

                continue


        # ----------------------------------------------------
        # Move
        # ----------------------------------------------------

        finished = move_player(direction)


        # ----------------------------------------------------
        # Check win
        # ----------------------------------------------------

        if finished:

            green_led.on()
            blue_led.on()

            win_screen()

            green_led.off()
            blue_led.off()

            return


        # ----------------------------------------------------
        # Movement delay
        # ----------------------------------------------------

        time.sleep(MOVE_DELAY)


# ============================================================
# 🚀 MAIN PROGRAM
# ============================================================

def main():

    while True:

        main_menu()

        play_game()


# ============================================================
# ▶️ RUN PROGRAM
# ============================================================

try:

    main()

except KeyboardInterrupt:

    print()
    print()
    print(
        YELLOW
        + "Game stopped by user."
        + RESET
    )

finally:

    green_led.off()
    red_led.off()
    blue_led.off()

    if not TEST_MODE:

        bus.close()