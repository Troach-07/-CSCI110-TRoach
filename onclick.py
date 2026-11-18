from pynput import keyboard, mouse
import sys


position = [0, 0]
GRID_SIZE = 20


def on_press(key):
    if key == keyboard.Key.esc:
        return False

    x = position[0]
    y = position[1]
    if key == keyboard.Key.up:
        position[1] = (y - 1) % GRID_SIZE
    elif key == keyboard.Key.down:
        position[1] = (y + 1) % GRID_SIZE
    elif key == keyboard.Key.right:
        position[0] = (x + 1) % GRID_SIZE
    elif key == keyboard.Key.left:
        position[0] = (x - 1) % GRID_SIZE
    else:
        return

    if key in (keyboard.Key.up, keyboard.Key.down, keyboard.Key.left, keyboard.Key.right):
        print_pos(position)


def on_click(x, y, button, pressed):
    if pressed:
        print(f"Clicked {button} at screen position ({x}, {y})")


def print_pos(position):
    sys.stdout.write("\033[2J\033[H")
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            cell = "x" if [x, y] == position else " "
            print(cell, end="")
        print()
    print(f"X: {position[0]}, Y: {position[1]}")

def main():
    print("Use the arrow keys to move. Click to see click coordinates; press Escape to quit.")
    print_pos(position)

    keyboard_listener = keyboard.Listener(on_press=on_press)
    mouse_listener = mouse.Listener(on_click=on_click)

    try:
        keyboard_listener.start()
        mouse_listener.start()

        while keyboard_listener.is_alive():
            keyboard_listener.join(timeout=0.1)
            mouse_listener.join(timeout=0.1)
    except OSError as error:
        print(f"Could not listen for input: {error}", file=sys.stderr)
        if sys.platform == "darwin":
            print(
                "Allow this terminal or Python in System Settings > "
                "Privacy & Security > Accessibility, then try again.",
                file=sys.stderr,
            )
    finally:
        keyboard_listener.stop()
        mouse_listener.stop()
        if keyboard_listener.is_alive():
            keyboard_listener.join()
        if mouse_listener.is_alive():
            mouse_listener.join()


if __name__ == "__main__":
    main()