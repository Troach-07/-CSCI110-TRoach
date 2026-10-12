import random
import math
from pathlib import Path
import re
import sys
import tmp


WIDTH = 48
HEIGHT = 20
RESET = "\033[0m"
FIELD_COUNT = tmp.IMAGE_COUNT
MAX_POSITION_INDEX = FIELD_COUNT - 1
MAX_FIELD_POSITION = MAX_POSITION_INDEX / 2


def read_move(prompt):
    if not sys.stdin.isatty():
        return input(prompt).strip().lower()

    import termios
    import tty

    print(prompt, end="", flush=True)
    file_descriptor = sys.stdin.fileno()
    previous_settings = termios.tcgetattr(file_descriptor)
    guess = ""
    try:
        tty.setraw(file_descriptor)
        while True:
            character = sys.stdin.read(1)
            if character in "\r\n":
                print()
                return guess
            if character == "\x03":
                raise KeyboardInterrupt
            if character in "\x7f\b":
                if guess:
                    guess = guess[:-1]
                    print("\b \b", end="", flush=True)
                continue

            character = character.lower()
            if not guess and character in "wasdoq":
                print(character)
                return character
            if character in "0123456789.":
                guess += character
                print(character, end="", flush=True)
    finally:
        termios.tcsetattr(file_descriptor, termios.TCSADRAIN, previous_settings)


def rgb_background(color):
    red, green, blue = color
    return f"\033[48;2;{red};{green};{blue}m"


def blend(color_a, color_b, amount):
    amount = max(0.0, min(1.0, amount))
    return tuple(
        round(channel_a + (channel_b - channel_a) * amount)
        for channel_a, channel_b in zip(color_a, color_b)
    )


def move_position(position_index, step):
    return (position_index + step) % FIELD_COUNT


def render_field(position_index, image_path):
    randomizer = random.Random(position_index)
    sky = randomizer.choice([(155, 199, 228), (180, 218, 206), (194, 214, 236), (245, 214, 170)])
    far_green = randomizer.choice([(138, 170, 112), (147, 186, 126), (125, 158, 124)])
    grass = randomizer.choice([(72, 118, 79), (92, 136, 80), (84, 119, 73), (110, 143, 84)])
    sun_x = randomizer.randrange(4, WIDTH - 4)
    sun_y = randomizer.randrange(2, 5)
    cloud_centers = [
        (randomizer.randrange(2, WIDTH - 2), randomizer.randrange(2, 7))
        for _ in range(randomizer.randint(1, 3))
    ]
    grid = [[(sky, "  ", None) for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for row in range(HEIGHT):
        for column in range(WIDTH):
            horizon = 9 + round(1.5 * math.sin(column * 0.19 + position_index))

            if row < horizon:
                color = sky
            elif row < horizon + 4:
                blend_amount = (row - horizon) / 4.0
                color = blend(sky, far_green, blend_amount)
            else:
                ground_amount = min(1.0, (row - (horizon + 4)) / 8.0)
                color = blend(far_green, grass, ground_amount)
                extra = 0.6 * math.sin((column * 0.08) + (row * 0.10) + (position_index * 0.2))
                color = tuple(
                    max(0, min(255, round(channel + extra)))
                    for channel in color
                )

            sun_distance = math.hypot(column - sun_x, row - sun_y)
            if sun_distance <= 5:
                sun_mix = 1 - (sun_distance / 5.0)
                color = blend(color, (255, 222, 128), sun_mix * 0.9)
            if any(abs(column - cloud_x) <= 2 and abs(row - cloud_y) <= 1 for cloud_x, cloud_y in cloud_centers):
                color = blend(color, (239, 248, 250), 0.5)
            grid[row][column] = (color, "  ", None)

    for tree_x in randomizer.sample(range(3, WIDTH - 3), 5):
        trunk_top = randomizer.randrange(5, 9)
        trunk_color = randomizer.choice([(125, 87, 58), (131, 96, 67), (111, 79, 55)])
        for row in range(trunk_top, 12):
            grid[row][tree_x] = (trunk_color, "  ", None)
        canopy = randomizer.choice([(82, 150, 104), (102, 170, 110), (120, 182, 120)])
        for row in range(max(1, trunk_top - 4), trunk_top + 1):
            spread = max(1, 4 - abs(row - (trunk_top - 2)))
            for column in range(max(0, tree_x - spread), min(WIDTH, tree_x + spread + 1)):
                distance = abs(column - tree_x)
                canopy_mix = max(0.2, 1 - (distance / (spread + 1)))
                blended = blend(grid[row][column][0], canopy, 0.8 * canopy_mix)
                grid[row][column] = (blended, "  ", None)

    # Keep the background softer and more playful by avoiding dark outline-heavy shapes.

    svg_content = image_path.read_text(encoding="utf-8")
    finder = re.search(r'<g id="finder".*?ellipse cx="([\d.]+)" cy="([\d.]+)"', svg_content, re.DOTALL)
    if finder:
        person_x = round(float(finder.group(1)) / 800 * (WIDTH - 1))
        feet_row = round(float(finder.group(2)) / 500 * (HEIGHT - 1))

        def put_person(row, offset, color, text="  ", foreground=None):
            column = max(0, min(WIDTH - 1, person_x + offset))
            row = max(0, min(HEIGHT - 1, row))
            base_color = grid[row][column][0]
            blended_color = blend(base_color, color, 0.22)
            grid[row][column] = (blended_color, text, foreground)

        # Keep the hidden character subtle and camouflaged against the background.
        put_person(feet_row - 6, -2, (52, 89, 126), "██")
        put_person(feet_row - 6, -1, (78, 113, 153), "██")
        put_person(feet_row - 6, 0, (98, 131, 169), "██")
        put_person(feet_row - 6, 1, (78, 113, 153), "██")
        put_person(feet_row - 6, 2, (52, 89, 126), "██")
        put_person(feet_row - 5, -1, (223, 176, 142), "██")
        put_person(feet_row - 5, 0, (235, 196, 165), "██")
        put_person(feet_row - 5, 1, (223, 176, 142), "██")
        put_person(feet_row - 4, -2, (164, 54, 49), "██")
        put_person(feet_row - 4, -1, (245, 234, 206), "██")
        put_person(feet_row - 4, 0, (208, 86, 74), "██")
        put_person(feet_row - 4, 1, (245, 234, 206), "██")
        put_person(feet_row - 4, 2, (164, 54, 49), "██")
        put_person(feet_row - 3, -2, (49, 84, 126), "██")
        put_person(feet_row - 3, -1, (241, 226, 200), "██")
        put_person(feet_row - 3, 0, (206, 80, 70), "██")
        put_person(feet_row - 3, 1, (241, 226, 200), "██")
        put_person(feet_row - 3, 2, (49, 84, 126), "██")
        put_person(feet_row - 2, -2, (82, 105, 91), "██")
        put_person(feet_row - 2, -1, (235, 223, 190), "██")
        put_person(feet_row - 2, 0, (191, 166, 106), "██")
        put_person(feet_row - 2, 1, (235, 223, 190), "██")
        put_person(feet_row - 2, 2, (82, 105, 91), "██")
        put_person(feet_row - 1, -1, (67, 51, 46), "██")
        put_person(feet_row - 1, 1, (67, 51, 46), "██")
        put_person(feet_row, -1, (38, 38, 38), "██")
        put_person(feet_row, 1, (38, 38, 38), "██")

    print(f"Field position: {position_index / 2:.1f}")
    for row in grid:
        for color, text, foreground in row:
            foreground_code = f"\033[38;2;{foreground[0]};{foreground[1]};{foreground[2]}m" if foreground else ""
            print(f"{rgb_background(color)}{foreground_code}{text}{RESET}", end="")
        print(RESET)


def guess_finder_position(answer, finder_index):
    answer = answer.strip()
    try:
        guessed_position = float(answer)
    except ValueError:
        print("Enter a number such as 4.5.")
        return False

    if not math.isfinite(guessed_position):
        print("Enter a finite field position.")
        return False

    guessed_index = round(guessed_position * 2)
    if not 0 <= guessed_index < FIELD_COUNT or not math.isclose(guessed_position * 2, guessed_index):
        print(f"Choose a field position from 0.0 to {MAX_FIELD_POSITION:.1f} in 0.5 steps.")
        return False

    if guessed_index == finder_index:
        print(f"Correct! He is in field {finder_index / 2:.1f}.")
        return True

    print("Not quite. Keep looking.")
    return False


def open_field_image(position_index):
    field = position_index / 2
    filename_position = f"{field:.1f}".replace(".", "_")
    image_path = Path(__file__).with_name("fields") / f"field_{filename_position}.svg"
    if image_path.exists():
        try:
            import subprocess
            if sys.platform == "darwin":
                subprocess.run(["open", str(image_path)], check=False)
            elif sys.platform.startswith("linux"):
                subprocess.run(["xdg-open", str(image_path)], check=False)
            else:
                print("Open this SVG file in a browser or image viewer:")
                print(image_path)
        except Exception:
            print("Could not open the image automatically.")
            print(image_path)
    else:
        print(f"Image not found: {image_path}")


def play_round():
    fields_dir = Path(__file__).with_name("fields")
    tmp.main()
    finder_index = int((fields_dir / "finder_position.txt").read_text(encoding="utf-8"))
    start_positions = [index for index in range(FIELD_COUNT) if index != finder_index]
    position_index = random.choice(start_positions)

    view_choice = input("Choose your view: T = terminal, O = open outside terminal, Q = quit: ").strip().lower()
    if view_choice == "q":
        return
    if view_choice not in {"t", "o"}:
        view_choice = "t"

    clear_screen = True
    while True:
        if view_choice == "o":
            open_field_image(position_index)
            view_choice = "t"
            print("Returning to terminal mode. Continue playing:")

        field = position_index / 2
        filename_position = f"{field:.1f}".replace(".", "_")
        image_path = fields_dir / f"field_{filename_position}.svg"
        if sys.stdout.isatty() and clear_screen:
            print("\033[2J\033[H", end="")
        clear_screen = True
        render_field(position_index, image_path)

        move = read_move(f"Move with W/A/S/D, enter a guess from 0 to {MAX_FIELD_POSITION:.1f}, open O for the photo, or Q to quit: ")
        if move == "q":
            break
        if move == "o":
            open_field_image(position_index)
            print("Returning to terminal mode. Continue playing:")
            continue

        if move == "w":
            position_index = move_position(position_index, 2)
        elif move == "d":
            position_index = move_position(position_index, 1)
        elif move == "s":
            position_index = move_position(position_index, -2)
        elif move == "a":
            position_index = move_position(position_index, -1)
        else:
            if guess_finder_position(move, finder_index):
                break
            clear_screen = False
        field = position_index / 2
        filename_position = f"{field:.1f}".replace(".", "_")
        image_path = fields_dir / f"field_{filename_position}.svg"
        if sys.stdout.isatty() and clear_screen:
            print("\033[2J\033[H", end="")
        clear_screen = True
        render_field(position_index, image_path)

        move = read_move(f"Move with W/D/S/A, enter a guess from 0 to {MAX_FIELD_POSITION:.1f}, open O for the photo, or Q to quit: ")
        if move == "q":
            break
        if move == "o":
            open_field_image(position_index)
            print("Returning to terminal mode. Continue playing:")
            continue

        if move == "w":
            position_index = move_position(position_index, 2)
        elif move == "d":
            position_index = move_position(position_index, -1)
        elif move == "s":
            position_index = move_position(position_index, 2)
        elif move == "a":
            position_index = move_position(position_index, -1)
        else:
            if guess_finder_position(move, finder_index):
                break
            clear_screen = False


def game():
    while True:
        play_round()
        play_again = input("Play again? (Y/N): ").strip().lower()
        if play_again not in {"y", "yes"}:
            break


if __name__ == "__main__":
    game()