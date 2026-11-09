
import pygame
import random
from collections import deque

pygame.init()

# Game settings
TILE = 28
FPS = 60
PLAYER_DELAY = 110
GHOST_DELAY = 230

LEVEL = [
    "#####################",
    "#.........#.........#",
    "#.###.###.#.###.###.#",
    "#o###.###.#.###.###o#",
    "#...................#",
    "#.###.#.#####.#.###.#",
    "#.....#...#...#.....#",
    "#####.###.#.###.#####",
    "#...#.#.......#.#...#",
    "#.#.#.#.##.##.#.#.#.#",
    "#.#.....#...#.....#.#",
    "#.#.#.#.#####.#.#.#.#",
    "#...#.#.......#.#...#",
    "#####.#.#####.#.#####",
    "#.........#.........#",
    "#.###.###.#.###.###.#",
    "#o..#.....P.....#..o#",
    "###.#.#.#####.#.#.###",
    "#.....#...#...#.....#",
    "#.#######.#.#######.#",
    "#...................#",
    "#####################"
]

WIDTH = len(LEVEL[0]) * TILE
HEIGHT = len(LEVEL) * TILE + 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Pac-Man")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24, bold=True)

BLACK = (0, 0, 0)
BLUE = (30, 70, 255)
YELLOW = (255, 230, 0)
WHITE = (255, 255, 255)

GHOST_COLORS = [
    (255, 50, 50),
    (255, 150, 200),
    (0, 220, 255),
    (255, 170, 30)
]

maze = [list(row) for row in LEVEL]

player = [10, 16]
start = player.copy()

ghost_starts = [
    [9, 10],
    [10, 10],
    [11, 10],
    [10, 9]
]

ghosts = [pos.copy() for pos in ghost_starts]

direction = (0, 0)
next_direction = (0, 0)

score = 0
lives = 3
power_until = 0
last_player_move = 0
last_ghost_move = 0
game_over = False
won = False

# Remove player marker
maze[player[1]][player[0]] = " "

def can_move(x, y):
    # Allow horizontal wraparound
    x %= len(maze[0])
    return (
        0 <= y < len(maze)
        and maze[y][x] != "#"
    )

def move_character(pos, dx, dy):
    nx = (pos[0] + dx) % len(maze[0])
    ny = pos[1] + dy

    if can_move(nx, ny):
        pos[0] = nx
        pos[1] = ny
        return True

    return False

def reset_positions():
    global direction, next_direction

    player[:] = start
    for ghost, original in zip(ghosts, ghost_starts):
        ghost[:] = original

    direction = (0, 0)
    next_direction = (0, 0)

def check_collision():
    global lives, game_over, score

    for ghost, original in zip(ghosts, ghost_starts):
        if player == ghost:
            if pygame.time.get_ticks() < power_until:
                score += 200
                ghost[:] = original.copy()
            else:
                lives -= 1
                reset_positions()

                if lives <= 0:
                    game_over = True
            return

def ghost_move(ghost):
    # Find shortest path toward player
    queue = deque([(tuple(ghost), [])])
    visited = {tuple(ghost)}

    directions = [
        (0, 1), (0, -1),
        (1, 0), (-1, 0)
    ]

    while queue:
        (x, y), path = queue.popleft()

        if [x, y] == player:
            if path:
                dx, dy = path[0]
                move_character(ghost, dx, dy)
            return

        random.shuffle(directions)

        for dx, dy in directions:
            nx = (x + dx) % len(maze[0])
            ny = y + dy

            if can_move(nx, ny) and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), path + [(dx, dy)]))

def draw_game():
    screen.fill(BLACK)

    # Draw maze
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            cx = x * TILE + TILE // 2
            cy = y * TILE + TILE // 2

            if cell == "#":
                pygame.draw.rect(
                    screen, BLUE,
                    (x*TILE+2, y*TILE+2, TILE-4, TILE-4),
                    border_radius=7
                )

            elif cell == ".":
                pygame.draw.circle(screen, WHITE, (cx, cy), 3)

            elif cell == "o":
                pygame.draw.circle(screen, WHITE, (cx, cy), 8)

    # Draw Pac-Man
    px = player[0]*TILE + TILE//2
    py = player[1]*TILE + TILE//2

    pygame.draw.circle(screen, YELLOW, (px, py), TILE//2-2)

    # Draw ghosts
    for i, ghost in enumerate(ghosts):
        gx = ghost[0]*TILE + TILE//2
        gy = ghost[1]*TILE + TILE//2

        color = GHOST_COLORS[i]

        if pygame.time.get_ticks() < power_until:
            color = BLUE

        pygame.draw.circle(screen, color, (gx, gy-3), 11)
        pygame.draw.rect(screen, color, (gx-11, gy-3, 22, 13))

        # Eyes
        pygame.draw.circle(screen, WHITE, (gx-5, gy-4), 4)
        pygame.draw.circle(screen, WHITE, (gx+5, gy-4), 4)
        pygame.draw.circle(screen, BLACK, (gx-5, gy-4), 2)
        pygame.draw.circle(screen, BLACK, (gx+5, gy-4), 2)

    # Scoreboard
    info = font.render(
        f"Score: {score}    Lives: {lives}",
        True, WHITE
    )
    screen.blit(info, (10, HEIGHT-40))

    if game_over or won:
        message = "YOU WIN!" if won else "GAME OVER"
        text = font.render(message, True, YELLOW)
        screen.blit(
            text,
            text.get_rect(center=(WIDTH//2, HEIGHT//2))
        )

    pygame.display.flip()

def main():
    global direction, next_direction
    global score, power_until
    global last_player_move, last_ghost_move
    global won

    running = True

    while running:
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    next_direction = (0, -1)
                elif event.key == pygame.K_DOWN:
                    next_direction = (0, 1)
                elif event.key == pygame.K_LEFT:
                    next_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    next_direction = (1, 0)

        if not game_over and not won:

            # Player movement
            if now - last_player_move >= PLAYER_DELAY:
                last_player_move = now

                dx, dy = next_direction
                nx = (player[0] + dx) % len(maze[0])
                ny = player[1] + dy

                if can_move(nx, ny):
                    direction = next_direction

                move_character(player, *direction)

                cell = maze[player[1]][player[0]]

                if cell == ".":
                    score += 10
                    maze[player[1]][player[0]] = " "

                elif cell == "o":
                    score += 50
                    power_until = now + 6000
                    maze[player[1]][player[0]] = " "

                check_collision()

            # Ghost movement
            if now - last_ghost_move >= GHOST_DELAY:
                last_ghost_move = now

                for ghost in ghosts:
                    if now < power_until:
                        options = [
                            (0, 1), (0, -1),
                            (1, 0), (-1, 0)
                        ]
                        random.shuffle(options)

                        for dx, dy in options:
                            if move_character(ghost, dx, dy):
                                break
                    else:
                        ghost_move(ghost)

                    check_collision()

            # Win when all dots are collected
            if not any(
                cell in (".", "o")
                for row in maze
                for cell in row
            ):
                won = True

        draw_game()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()

##remember to install pygame 