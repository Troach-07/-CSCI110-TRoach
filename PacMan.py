
import time
import random
import keyboard

# Game settings
map_width = 21
map_height = 21

player_x = 1
player_y = 1
game_running = True
score = 0

# Generate a random maze
def Generate_Maze():
    maze = [["#" for x in range(map_width)]
            for y in range(map_height)]

    def carve(x, y):
        maze[y][x] = "."

        directions = [
            (0, 2), (0, -2),
            (2, 0), (-2, 0)
        ]
        random.shuffle(directions)

        for dx, dy in directions:
            nx = x + dx
            ny = y + dy

            if (1 <= nx < map_width - 1 and
                1 <= ny < map_height - 1 and
                maze[ny][nx] == "#"):

                maze[y + dy // 2][x + dx // 2] = "."
                carve(nx, ny)

    carve(1, 1)

    # Add extra paths for a Pac-Man-like maze
    for y in range(1, map_height - 1):
        for x in range(1, map_width - 1):
            if maze[y][x] == "#" and random.random() < 0.12:
                maze[y][x] = "."

    # Place exit in bottom-right area
    for y in range(map_height - 2, 0, -1):
        for x in range(map_width - 2, 0, -1):
            if maze[y][x] == ".":
                maze[y][x] = "E"
                return maze

    return maze


maze = Generate_Maze()


def Controls():
    global player_x, player_y, game_running

    new_x = player_x
    new_y = player_y

    if keyboard.is_pressed("down"):
        new_y = (player_y + 1) % map_height

    elif keyboard.is_pressed("up"):
        new_y = (player_y - 1) % map_height

    elif keyboard.is_pressed("left"):
        new_x = (player_x - 1) % map_width

    elif keyboard.is_pressed("right"):
        new_x = (player_x + 1) % map_width

    elif keyboard.is_pressed("esc"):
        game_running = False

    if maze[new_y][new_x] != "#":
        player_x = new_x
        player_y = new_y


def Map_Size_Elements():
    for y in range(map_height):
        for x in range(map_width):
            if x == player_x and y == player_y:
                print("P", end=" ")
            else:
                print(maze[y][x], end=" ")
        print()


def Player():
    global score

    if maze[player_y][player_x] == ".":
        score += 10
        maze[player_y][player_x] = " "

    print(f"Score: {score}")
    print(f"Position: ({player_x}, {player_y})")


def Game_Menu():
    print("=== RANDOM PAC-MAN MAZE ===")
    print("P = Player")
    print("# = Wall")
    print(". = Dot (+10 points)")
    print("E = Exit")
    print("Arrow Keys = Move")
    print("ESC = Quit")
    print("===========================")


def main():
    global game_running

    Game_Menu()
    time.sleep(2)

    while game_running:
        Controls()

        print("\n" * 30)
        Map_Size_Elements()
        Player()

        if maze[player_y][player_x] == "E":
            print("YOU WIN!")
            game_running = False

        time.sleep(0.15)

    print("Game Over!")


if __name__ == "__main__":
    main()
