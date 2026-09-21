Hi! This is a simple maze game I made using a Raspberry Pi and Sense HAT.

The game uses the Sense HAT’s 8×8 LED display as the game screen.
You control the green LED by physically tilting the Sense HAT, so there are no WASD controls.

🔵 Blue = walls
⬛ Black = paths
🟢 Green = player
🟡 Yellow = finish

The accelerometer detects the direction you tilt the board and moves the player through the maze. The game also has 5 lives, and hitting a wall causes you to lose a life.

The Sense HAT is calibrated at the start, so make sure to keep it still during calibration. The joystick can also be used for some game controls.

The terminal is mainly used to show game information, while the actual gameplay happens on the LED matrix.

To run it, connect the Sense HAT and use:
