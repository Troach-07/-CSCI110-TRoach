
import pygame
import random
import heapq
from collections import deque

pygame.init()

# Game settings
TILE = 28
FPS = 60
PLAYER_DELAY = 110
GHOST_DELAY = 230
GHOST_IDLE_LIMIT = 5000
BONUS_ROUND_DURATION = 60_000

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

LEVEL_TWO = [
    "##########.##########",
    "#...................#",
    "#.###.#...#...#.###.#",
    "#o..#.#.#.#.#.#.#..o#",
    "#...#...........#...#",
    "#.#.#.###.###.#.#.#.#",
    "#...#.....#.....#...#",
    "###.###.#.#.###.###.#",
    "#...#...#...#...#...#",
    "#.#.#.#.## ##.#.#.#.#",
    "..#.....#   #.....#..",
    "#.#.#.#.#####.#.#.#.#",
    "#...#.#.......#.#...#",
    "#.###.#.#####.#.###.#",
    "#.........#.........#",
    "#.###.###.#.###.###.#",
    "#o..#.....P.....#..o#",
    "###.#.#.#####.#.#.###",
    "#.....#...#...#.....#",
    "#.#######.#.#######.#",
    "#...................#",
    "##########.##########"
]
LEVELS = [LEVEL, LEVEL_TWO]

WIDTH = len(LEVEL[0]) * TILE
HEIGHT = len(LEVEL) * TILE + 50

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Pac-Man")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24, bold=True)
title_font = pygame.font.SysFont("Arial", 40, bold=True)
status_font = pygame.font.SysFont("Arial", 18, bold=True)

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
GHOST_SCORE_MULTIPLIERS = [0.5, 1.0, 1.0, 1.0]
INITIAL_DOT_COUNT = sum(cell in ".o" for row in LEVEL for cell in row)

current_level = 0
level_dot_count = INITIAL_DOT_COUNT
maze = [list(row) for row in LEVELS[current_level]]

# Positions are stored as [column, row] so they can index the maze directly.
player = [10, 16]
start = player.copy()

ghost_starts = [
    [9, 10],
    [10, 10],
    [11, 10],
    [10, 9]
]
GHOST_AREA = {(9, 10), (10, 10), (11, 10), (10, 9)}
GHOST_DOOR = (10, 9)

ghosts = [pos.copy() for pos in ghost_starts]
ghost_facing = [(0, -1) for _ in ghosts]

direction = (0, 0)
next_direction = (0, 0)
ghost_direction = (0, 0)

score = 0
lives = 5
power_until = 0
last_player_move = 0
last_ghost_moves = [0 for _ in ghosts]
last_controlled_ghost_move = 0
game_over = False
won = False
pacman_won = False
ghosts_won = False
game_mode = None
controlled_ghost = 0
bonus_round = False
bonus_until = 0
eaten_ghosts = [False for _ in ghosts]

# Remove player marker
maze[player[1]][player[0]] = " "

def can_move(x, y, allow_ghost_area=False):
    # Allow Pac-Man and ghosts to pass between opposite maze edges.
    x %= len(maze[0])
    y %= len(maze)
    return (
        maze[y][x] != "#"
        and (allow_ghost_area or (x, y) not in GHOST_AREA)
    )

def move_character(pos, dx, dy, allow_ghost_area=False):
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

    if can_move(nx, ny, allow_ghost_area):
        pos[0] = nx
        pos[1] = ny
        return True

    return False

def move_pacman_toward_dot():
    global direction

    powered_up = bonus_round or pygame.time.get_ticks() < power_until
    distance_from_ghosts = {}
    queue = deque()
    for ghost in ghosts:
        position = tuple(ghost)
        if position not in distance_from_ghosts:
            distance_from_ghosts[position] = 0
            queue.append(position)

    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    while queue:
        x, y = queue.popleft()
        for dx, dy in directions:
            nx = (x + dx) % len(maze[0])
            ny = (y + dy) % len(maze)
            position = (nx, ny)
            if can_move(nx, ny) and position not in distance_from_ghosts:
                distance_from_ghosts[position] = distance_from_ghosts[(x, y)] + 1
                queue.append(position)

    start_position = tuple(player)
    route_costs = {start_position: 0}
    first_steps = {start_position: None}
    queue = [(0, player[1], player[0])]

    while queue:
        cost, y, x = heapq.heappop(queue)
        position = (x, y)
        if cost != route_costs[position]:
            continue
        for dx, dy in directions:
            nx = (x + dx) % len(maze[0])
            ny = (y + dy) % len(maze)
            next_position = (nx, ny)

            if not can_move(nx, ny):
                continue

            risk = 0
            if not powered_up:
                ghost_distance = distance_from_ghosts.get(next_position, 99)
                if ghost_distance == 0:
                    risk = 40
                elif ghost_distance == 1:
                    risk = 10
                elif ghost_distance == 2:
                    risk = 3

            new_cost = cost + 1 + risk
            if new_cost < route_costs.get(next_position, float("inf")):
                route_costs[next_position] = new_cost
                first_steps[next_position] = (
                    first_steps[position] if position != start_position else (dx, dy)
                )
                heapq.heappush(queue, (new_cost, ny, nx))

    if powered_up:
        reachable_ghosts = [
            (route_costs[tuple(ghost)], tuple(ghost))
            for ghost_index, ghost in enumerate(ghosts)
            if not eaten_ghosts[ghost_index]
            and tuple(ghost) in route_costs
            and first_steps[tuple(ghost)] is not None
        ]
        if reachable_ghosts:
            _, target_ghost = min(reachable_ghosts)
            step = first_steps[target_ghost]
            moved = move_character(player, *step)
            if moved:
                direction = step
            return moved

    best_target = None
    best_score = float("inf")
    for (x, y), cost in route_costs.items():
        cell = maze[y][x]
        if cell not in (".", "o") or first_steps[(x, y)] is None:
            continue

        target_score = cost
        if cell == "o" and not powered_up:
            if distance_from_ghosts.get((x, y), 99) <= 4:
                target_score -= 12

        if target_score < best_score:
            best_score = target_score
            best_target = (x, y)

    if best_target is None:
        return False
    step = first_steps[best_target]
    moved = move_character(player, *step)
    if moved:
        direction = step
    return moved

def reset_positions():
    global direction, next_direction, ghost_direction

    # Restore the player and ghosts after Pac-Man loses a life.
    player[:] = start
    for ghost, original in zip(ghosts, ghost_starts):
        ghost[:] = original
    ghost_facing[:] = [(0, -1) for _ in ghosts]

    direction = (0, 0)
    next_direction = (0, 0)
    ghost_direction = (0, 0)

def restart_game():
    global maze, score, lives, power_until, current_level, level_dot_count
    global last_player_move, last_ghost_moves, last_controlled_ghost_move
    global game_over, won, pacman_won, ghosts_won
    global controlled_ghost
    global bonus_round, bonus_until, eaten_ghosts

    current_level = 0
    maze = [list(row) for row in LEVELS[current_level]]
    level_dot_count = sum(cell in ".o" for row in maze for cell in row)
    maze[start[1]][start[0]] = " "
    reset_positions()
    controlled_ghost = 0

    score = 0
    lives = 5
    power_until = 0
    last_player_move = pygame.time.get_ticks()
    last_ghost_moves = [last_player_move for _ in ghosts]
    last_controlled_ghost_move = last_player_move
    game_over = False
    won = False
    pacman_won = False
    ghosts_won = False
    bonus_round = False
    bonus_until = 0
    eaten_ghosts = [False for _ in ghosts]

def advance_level():
    global current_level, level_dot_count, maze, power_until
    global last_player_move, last_ghost_moves, last_controlled_ghost_move
    global controlled_ghost, bonus_round, bonus_until, eaten_ghosts
    global won, pacman_won, ghosts_won

    if current_level + 1 >= len(LEVELS):
        won = True
        return

    current_level += 1
    maze = [list(row) for row in LEVELS[current_level]]
    level_dot_count = sum(cell in ".o" for row in maze for cell in row)
    maze[start[1]][start[0]] = " "
    reset_positions()
    controlled_ghost = 0
    power_until = 0
    bonus_round = False
    bonus_until = 0
    eaten_ghosts = [False for _ in ghosts]
    pacman_won = False
    ghosts_won = False

    last_player_move = pygame.time.get_ticks()
    last_ghost_moves = [last_player_move for _ in ghosts]
    last_controlled_ghost_move = last_player_move

def check_collision():
    global lives, game_over, score, won

    for ghost_index, (ghost, original) in enumerate(zip(ghosts, ghost_starts)):
        if eaten_ghosts[ghost_index]:
            continue
        if player == ghost:
            if bonus_round or pygame.time.get_ticks() < power_until:
                # Powered-up Pac-Man sends the ghost back to its starting tile.
                score += int(200 * GHOST_SCORE_MULTIPLIERS[ghost_index])
                if bonus_round:
                    eaten_ghosts[ghost_index] = True
                    if all(eaten_ghosts):
                        advance_level()
                else:
                    ghost[:] = original.copy()
            elif game_mode == "ghost":
                won = True
            else:
                # Losing a life resets positions but keeps the current score.
                lives -= 1
                reset_positions()

                if lives <= 0:
                    game_over = True
            return

def ghost_target(ghost_index, distances):
    player_x, player_y = player
    direction_x, direction_y = direction

    if ghost_index == 0:
        return player_x, player_y

    if ghost_index == 1:
        return (
            (player_x + direction_x * 4) % len(maze[0]),
            max(0, min(len(maze) - 1, player_y + direction_y * 4))
        )

    if ghost_index == 2:
        pivot_x = (player_x + direction_x * 2) % len(maze[0])
        pivot_y = max(0, min(len(maze) - 1, player_y + direction_y * 2))
        blinky_x, blinky_y = ghosts[0]
        return (
            max(0, min(len(maze[0]) - 1, pivot_x * 2 - blinky_x)),
            max(0, min(len(maze) - 1, pivot_y * 2 - blinky_y))
        )

    player_distance = distances.get(tuple(player), float("inf"))
    if player_distance <= 8:
        return 1, len(maze) - 2
    return player_x, player_y

def ghost_move(ghost, ghost_index):
    start_position = tuple(ghost)
    distances = {start_position: 0}
    first_steps = {start_position: None}
    queue = deque([start_position])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while queue:
        x, y = queue.popleft()
        for dx, dy in directions:
            nx = (x + dx) % len(maze[0])
            ny = (y + dy) % len(maze)
            position = (nx, ny)
            if can_move(nx, ny, allow_ghost_area=True) and position not in distances:
                distances[position] = distances[(x, y)] + 1
                first_steps[position] = first_steps[(x, y)] or (dx, dy)
                queue.append(position)

    target_x, target_y = ghost_target(ghost_index, distances)
    reachable_targets = [
        position for position in distances
        if first_steps[position] is not None
    ]
    if not reachable_targets:
        return

    target = min(
        reachable_targets,
        key=lambda position: (
            min(
                (position[0] - target_x) % len(maze[0]),
                (target_x - position[0]) % len(maze[0])
            ) + min(
                (position[1] - target_y) % len(maze),
                (target_y - position[1]) % len(maze)
            ),
            distances[position]
        )
    )
    move_character(ghost, *first_steps[target], allow_ghost_area=True)

def pacman_mouth_points(px, py, radius, facing):
    dx, dy = facing
    if dx == 0 and dy == 0:
        dx = 1

    tip = (px + dx * radius, py + dy * radius)
    perpendicular = (-dy, dx)
    half_opening = radius // 2
    return [
        (px, py),
        (
            tip[0] + perpendicular[0] * half_opening,
            tip[1] + perpendicular[1] * half_opening
        ),
        (
            tip[0] - perpendicular[0] * half_opening,
            tip[1] - perpendicular[1] * half_opening
        )
    ]

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

    door_x = GHOST_DOOR[0] * TILE
    door_y = GHOST_DOOR[1] * TILE
    pygame.draw.line(
        screen, (0, 220, 255),
        (door_x + 5, door_y + TILE // 2 - 4),
        (door_x + TILE - 5, door_y + TILE // 2 - 4), 3
    )
    pygame.draw.line(
        screen, (0, 220, 255),
        (door_x + 5, door_y + TILE // 2 + 4),
        (door_x + TILE - 5, door_y + TILE // 2 + 4), 3
    )

    # Draw Pac-Man over the maze tile at the current player position.
    px = player[0]*TILE + TILE//2
    py = player[1]*TILE + TILE//2

    pacman_radius = TILE//2-2
    pygame.draw.circle(screen, YELLOW, (px, py), pacman_radius)
    pygame.draw.polygon(
        screen, BLACK, pacman_mouth_points(px, py, pacman_radius, direction)
    )

    # Draw each ghost, changing its color while the power pellet is active.
    for i, ghost in enumerate(ghosts):
        if eaten_ghosts[i]:
            continue
        gx = ghost[0]*TILE + TILE//2
        gy = ghost[1]*TILE + TILE//2

        color = GHOST_COLORS[i]

        if bonus_round or pygame.time.get_ticks() < power_until:
            color = BLUE

        outlined = game_mode in ("ghost", "two_player") and i == controlled_ghost
        if outlined:
            pygame.draw.circle(screen, WHITE, (gx, gy-3), 13)
            pygame.draw.rect(screen, WHITE, (gx-13, gy-3, 26, 14))
            for offset in (-9, -3, 3, 9):
                pygame.draw.circle(screen, WHITE, (gx + offset, gy + 9), 4)

        pygame.draw.circle(screen, color, (gx, gy-3), 11)
        pygame.draw.rect(screen, color, (gx-11, gy-3, 22, 12))
        for offset in (-8, -3, 3, 8):
            pygame.draw.circle(screen, color, (gx + offset, gy + 8), 3)

        highlight = tuple(min(channel + 55, 255) for channel in color)
        pygame.draw.ellipse(screen, highlight, (gx-7, gy-10, 5, 3))

        # Eye whites and pupils make the ghost's expression easy to read.
        pygame.draw.ellipse(screen, WHITE, (gx-8, gy-7, 6, 9))
        pygame.draw.ellipse(screen, WHITE, (gx+2, gy-7, 6, 9))
        look_x, look_y = ghost_facing[i]
        pupil_x = look_x * 2
        pupil_y = look_y * 2
        pygame.draw.circle(screen, BLACK, (gx-5+pupil_x, gy-3+pupil_y), 2)
        pygame.draw.circle(screen, BLACK, (gx+5+pupil_x, gy-3+pupil_y), 2)
        pygame.draw.circle(screen, WHITE, (gx-5+pupil_x, gy-4+pupil_y), 1)
        pygame.draw.circle(screen, WHITE, (gx+5+pupil_x, gy-4+pupil_y), 1)

    if game_mode in ("ghost", "two_player"):
        dots_left = sum(cell in (".", "o") for row in maze for cell in row)
        if bonus_round:
            seconds_left = max(
                0, (bonus_until - pygame.time.get_ticks() + 999) // 1000
            )
            controls = f"BONUS ROUND: Eat all ghosts! Time: {seconds_left}s"
        elif game_mode == "two_player":
            controls = (
                f"P1: Arrows | P2 Ghost {controlled_ghost + 1}: "
                f"WASD / E switch | Dots: {dots_left}"
            )
        else:
            controls = (
                f"Ghost {controlled_ghost + 1}: WASD move, E switch"
                f" | Dots: {dots_left}"
            )
        controls += f" | Map {current_level + 1}/{len(LEVELS)}"
        info = status_font.render(controls, True, WHITE)
        screen.blit(info, info.get_rect(center=(WIDTH // 2, HEIGHT - 24)))
    else:
        bonus_status = ""
        if bonus_round:
            seconds_left = max(
                0, (bonus_until - pygame.time.get_ticks() + 999) // 1000
            )
            ghosts_left = len(ghosts) - sum(eaten_ghosts)
            bonus_status = f"    Ghosts: {ghosts_left}    Time: {seconds_left}s"
        info = font.render(
            f"Score: {score}    Lives: {lives}    Map: {current_level + 1}/{len(LEVELS)}{bonus_status}",
            True, WHITE
        )
        screen.blit(info, (10, HEIGHT-40))

    if game_over or won:
        if won:
            message = "YOU WIN!"
        elif pacman_won:
            message = "PAC-MAN WINS!"
        elif ghosts_won:
            message = "GHOSTS WIN!"
        elif game_mode == "ghost":
            message = "PAC-MAN ESCAPED!"
        elif game_mode == "two_player":
            message = "GHOST WINS!"
        else:
            message = "GAME OVER"
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

        restart_text = "Press R to play again" if won else "Press R to restart"
        restart_message = font.render(restart_text, True, YELLOW)
        screen.blit(
            restart_message,
            restart_message.get_rect(center=(WIDTH//2, HEIGHT//2 + 24))
        )

    pygame.display.flip()

def draw_menu():
    screen.fill(BLACK)
    title = title_font.render("PAC-MAN", True, YELLOW)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100)))

    instructions = [
        "Choose a game mode",
        "P: Single player as Pac-Man (arrow keys)",
        "G: Single player as a ghost (WASD; E switches ghosts)",
        "T: Two players (P1 arrows; P2 ghost uses WASD)",
        "In Ghost mode, catch Pac-Man before all dots are eaten."
    ]
    for index, line in enumerate(instructions):
        text = status_font.render(line, True, WHITE)
        screen.blit(
            text,
            text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50 + index * 34))
        )

    pygame.display.flip()

def main():
    global direction, next_direction
    global ghost_direction
    global score, power_until
    global last_player_move, last_ghost_moves
    global last_controlled_ghost_move
    global lives, game_over, won, pacman_won
    global ghosts_won
    global game_mode, controlled_ghost
    global bonus_round, bonus_until

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
                elif game_mode is None:
                    if event.key in (pygame.K_p, pygame.K_1):
                        game_mode = "pacman"
                        restart_game()
                    elif event.key in (pygame.K_g, pygame.K_2):
                        game_mode = "ghost"
                        restart_game()
                    elif event.key in (pygame.K_t, pygame.K_3):
                        game_mode = "two_player"
                        restart_game()
                elif event.key == pygame.K_r:
                    if game_over or won:
                        restart_game()
                    else:
                        lives -= 1
                        reset_positions()
                        last_controlled_ghost_move = now
                        if lives <= 0:
                            game_over = True
                elif event.key == pygame.K_UP:
                    next_direction = (0, -1)
                elif event.key == pygame.K_DOWN:
                    next_direction = (0, 1)
                elif event.key == pygame.K_LEFT:
                    next_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    next_direction = (1, 0)
                elif game_mode in ("ghost", "two_player") and event.key == pygame.K_e:
                    controlled_ghost = (controlled_ghost + 1) % len(ghosts)
                    ghost_direction = (0, 0)
                elif game_mode in ("ghost", "two_player") and event.key == pygame.K_w:
                    ghost_direction = (0, -1)
                elif game_mode in ("ghost", "two_player") and event.key == pygame.K_s:
                    ghost_direction = (0, 1)
                elif game_mode in ("ghost", "two_player") and event.key == pygame.K_d:
                    ghost_direction = (1, 0)
                elif game_mode in ("ghost", "two_player") and event.key == pygame.K_a:
                    ghost_direction = (-1, 0)
                elif event.key == pygame.K_TAB:
                    won=True
                elif event.key == pygame.K_LSHIFT:
                    score=score+100
                elif event.key == pygame.K_RSHIFT:
                     score=score-100
          

        if game_mode is not None and not game_over and not won:
            if (
                game_mode in ("ghost", "two_player")
                and now - last_controlled_ghost_move >= GHOST_IDLE_LIMIT
            ):
                game_over = True
                pacman_won = True

        if bonus_round and not game_over and not won and now >= bonus_until:
            game_over = True
            ghosts_won = True

        if game_mode is not None and not game_over and not won:

            # Move Pac-Man on a timer so movement speed is independent of frame rate.
            if now - last_player_move >= PLAYER_DELAY:
                last_player_move = now

                if game_mode == "ghost":
                    move_pacman_toward_dot()
                else:
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

            # Move each ghost on its own timer; Blinky speeds up as dots are eaten.
            if not game_over and not won:
                dots_left = sum(cell in ".o" for row in maze for cell in row)
                dots_eaten = level_dot_count - dots_left
                for ghost_index, ghost in enumerate(ghosts):
                    if eaten_ghosts[ghost_index]:
                        continue
                    ghost_delay = GHOST_DELAY
                    if ghost_index == 0:
                        ghost_delay = max(
                            PLAYER_DELAY, GHOST_DELAY - dots_eaten * 2
                        )
                    if now - last_ghost_moves[ghost_index] < ghost_delay:
                        continue
                    last_ghost_moves[ghost_index] = now

                    previous_position = ghost.copy()
                    if (
                        game_mode in ("ghost", "two_player")
                        and ghost_index == controlled_ghost
                    ):
                        move_character(
                            ghost, *ghost_direction, allow_ghost_area=True
                        )
                        if ghost != previous_position:
                            last_controlled_ghost_move = now
                    elif bonus_round or now < power_until:
                        options = [
                            (0, 1), (0, -1),
                            (1, 0), (-1, 0)
                        ]
                        random.shuffle(options)

                        for dx, dy in options:
                            if move_character(
                                ghost, dx, dy, allow_ghost_area=True
                            ):
                                break
                    else:
                        ghost_move(ghost, ghost_index)

                    if ghost != previous_position:
                        ghost_facing[ghost_index] = (
                            ghost[0] - previous_position[0],
                            ghost[1] - previous_position[1]
                        )
                        if ghost_facing[ghost_index][0] > 1:
                            ghost_facing[ghost_index] = (-1, 0)
                        elif ghost_facing[ghost_index][0] < -1:
                            ghost_facing[ghost_index] = (1, 0)
                        elif ghost_facing[ghost_index][1] > 1:
                            ghost_facing[ghost_index] = (0, -1)
                        elif ghost_facing[ghost_index][1] < -1:
                            ghost_facing[ghost_index] = (0, 1)

                    check_collision()

            # Clearing the maze starts a timed round to eat every ghost.
            if not any(
                cell in (".", "o")
                for row in maze
                for cell in row
            ):
                if not bonus_round:
                    bonus_round = True
                    bonus_until = now + BONUS_ROUND_DURATION

        if game_mode is None:
            draw_menu()
            clock.tick(FPS)
            continue

        draw_game()
        # Cap rendering speed without tying movement timing to the frame rate.
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()

##remember to install pygame 