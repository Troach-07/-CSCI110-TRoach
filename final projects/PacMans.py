
import pygame
import random
from collections import deque

pygame.init()

# Game settings
TILE = 28
FPS = 60
PLAYER_DELAY = 110
GHOST_DELAY = 230

# The map uses # for walls, . for dots, o for power pellets, and P for the start.
LEVEL = [
    "##########.##########",
    "#...................#",
    "#.###.###.#.###.###.#",
    "#o###.###.#.###.###o#",
    "#...................#",
    "#.###.#.#####.#.###.#",
    "#.....#...#...#.....#",
    "#####.###.#.###.#####",
    "#...#.#.......#.#...#",
    "#.#.#.#.## ##.#.#.#.#",
    "..#.....#   #.....#..",
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
    "##########.##########"
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

# Positions are stored as [column, row] so they can index the maze directly.
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
lives = 5
power_until = 0
last_player_move = 0
last_ghost_move = 0
game_over = False
won = False

# Remove player marker
maze[player[1]][player[0]] = " "

def can_move(x, y):
    # Allow Pac-Man and ghosts to pass between opposite maze edges.
    x %= len(maze[0])
    y %= len(maze)
    return (
        maze[y][x] != "#"
    )

def move_character(pos, dx, dy):
    nx = pos[0] + dx
    if nx < 0:
        nx = len(maze[0]) - 1
    elif nx >= len(maze[0]):
        nx = 0

    ny = pos[1] + dy
    if ny < 0:
        ny = len(maze) - 1
    elif ny >= len(maze):
        ny = 0

    if can_move(nx, ny):
        pos[0] = nx
        pos[1] = ny
        return True

    return False

def reset_positions():
    global direction, next_direction

    # Restore the player and ghosts after Pac-Man loses a life.
    player[:] = start
    for ghost, original in zip(ghosts, ghost_starts):
        ghost[:] = original

    direction = (0, 0)
    next_direction = (0, 0)

def restart_game():
    global maze, score, lives, power_until
    global last_player_move, last_ghost_move, game_over, won

    maze = [list(row) for row in LEVEL]
    maze[start[1]][start[0]] = " "
    reset_positions()

    score = 0
    lives = 5
    power_until = 0
    last_player_move = pygame.time.get_ticks()
    last_ghost_move = last_player_move
    game_over = False
    won = False

def check_collision():
    global lives, game_over, score

    for ghost, original in zip(ghosts, ghost_starts):
        if player == ghost:
            if pygame.time.get_ticks() < power_until:
                # Powered-up Pac-Man sends the ghost back to its starting tile.
                score += 200
                ghost[:] = original.copy()
            else:
                # Losing a life resets positions but keeps the current score.
                lives -= 1
                reset_positions()

                if lives <= 0:
                    game_over = True
            return

def ghost_move(ghost):
    # Breadth-first search finds a shortest route through the walkable maze.
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

        # Randomize equally short routes so ghosts do not all move identically.
        random.shuffle(directions)

        for dx, dy in directions:
            nx = (x + dx) % len(maze[0])
            ny = y + dy

            if can_move(nx, ny) and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), path + [(dx, dy)]))

def draw_game():
    screen.fill(BLACK)

    # Draw walls and uneaten dots from the current maze state.
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

    # Draw Pac-Man over the maze tile at the current player position.
    px = player[0]*TILE + TILE//2
    py = player[1]*TILE + TILE//2

    pygame.draw.circle(screen, YELLOW, (px, py), TILE//2-2)

    # Draw each ghost, changing its color while the power pellet is active.
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

    # Keep the score and remaining lives visible below the maze.
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
            text.get_rect(center=(WIDTH//2, HEIGHT//2 - 24))
        )

        final_score = font.render(f"Final score: {score}", True, WHITE)
        screen.blit(
            final_score,
            final_score.get_rect(center=(WIDTH//2, HEIGHT//2))
        )

        if game_over:
            restart_message = font.render("Press R to restart", True, YELLOW)
            screen.blit(
                restart_message,
                restart_message.get_rect(center=(WIDTH//2, HEIGHT//2 + 24))
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

        # Read input events and remember the next direction the player requests.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif game_over and event.key == pygame.K_r:
                    restart_game()
                elif event.key == pygame.K_UP:
                    next_direction = (0, -1)
                elif event.key == pygame.K_DOWN:
                    next_direction = (0, 1)
                elif event.key == pygame.K_LEFT:
                    next_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    next_direction = (1, 0)
                elif event.key == pygame.K_w:
                    next_direction = (0,-1)
                elif event.key == pygame.K_s:
                    next_direction = (0,1)
                elif event.key == pygame.K_d:
                    next_direction = (1,0)
                elif event.key == pygame.K_a:
                    next_direction = (-1,0)
                elif event.key == pygame.K_TAB:
                    won=True
                elif event.key == pygame.K_LSHIFT:
                    score=score+100
                elif event.key == pygame.K_RSHIFT:
                     score=score-100
          

        if not game_over and not won:

            # Move Pac-Man on a timer so movement speed is independent of frame rate.
            if now - last_player_move >= PLAYER_DELAY:
                last_player_move = now

                dx, dy = next_direction
                nx = (player[0] + dx) % len(maze[0])
                ny = player[1] + dy
                

                if can_move(nx, ny):
                    direction = next_direction

                # Continue in the last valid direction when a turn is blocked.
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

            # Move ghosts at their own slower interval.
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

            # The level is complete when no regular or power-pellet dots remain.
            if not any(
                cell in (".", "o")
                for row in maze
                for cell in row
            ):
                won = True
            

        draw_game()
        # Cap rendering speed without tying movement timing to the frame rate.
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()

##remember to install pygame 