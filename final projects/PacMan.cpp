#include <algorithm>
#include <chrono>
#include <cstdlib>
#include <fcntl.h>
#include <iostream>
#include <random>
#include <string>
#include <termios.h>
#include <thread>
#include <unistd.h>
#include <vector>

using Grid = std::vector<std::string>;

struct Position {
    int x;
    int y;
};

struct Ghost {
    Position position;
    Position start;
};

Grid makeLevelOne() {
    return {
        "####################",
        "#.......##.......#",
        "#.###.#.##.#.###.#",
        "#o###.#.##.#.###o#",
        "#................#",
        "#.###.####.###.#",
        "#.....##  ##.....#",
        "#####.#    #.#####",
        "    #.# ## #.#    ",
        "#####.#    #.#####",
        "#................#",
        "#.###.####.###.#",
        "#o..#......#..o#",
        "###.#.####.#.###",
        "#.....#  #.....#",
        "#.###.## ##.###.#",
        "#o..#......#..o#",
        "###.#.####.#.###",
        "#.....#  #.....#",
        "#.##########.#",
        "#................#",
        "####################"
    };
}

Grid makeLevelTwo() {
    return {
        "####################",
        "#o................#",
        "#.###.######.###.#",
        "#.#..........#.o#",
        "#.#.##.##.##.#.#",
        "#...#......#...#",
        "###.###.##.###.###",
        "#.....#....#.....#",
        "#.###.#.##.#.###.#",
        "#.#...#    #...#.#",
        "#.#.########.#.#",
        "#..............#",
        "#.##.###  ###.##.#",
        "#o.#.#      #.#.o#",
        "#..#.########.#..#",
        "#................#",
        "#.###.####.###.#",
        "#.....#    #.....#",
        "###.##.####.##.###",
        "#o..............o#",
        "#.####.####.####.#",
        "####################"
    };
}

bool isWall(const Grid& grid, int x, int y) {
    if (y < 0 || y >= static_cast<int>(grid.size())) {
        return true;
    }
    if (x < 0) {
        x = static_cast<int>(grid[y].size()) - 1;
    } else if (x >= static_cast<int>(grid[y].size())) {
        x = 0;
    }

    char cell = grid[y][x];
    return cell == '#' || cell == '-';
}

void rawMode(termios& original) {
    tcgetattr(STDIN_FILENO, &original);
    termios raw = original;
    raw.c_lflag &= static_cast<tcflag_t>(~(ICANON | ECHO));
    tcsetattr(STDIN_FILENO, TCSANOW, &raw);

    int flags = fcntl(STDIN_FILENO, F_GETFL, 0);
    fcntl(STDIN_FILENO, F_SETFL, flags | O_NONBLOCK);
}

char readKey() {
    char key = '\0';
    if (read(STDIN_FILENO, &key, 1) == 1) {
        return key;
    }
    return '\0';
}

int main() {
    std::vector<Grid> levels = {makeLevelOne(), makeLevelTwo()};
    int level = 0;
    Grid grid = levels[level];

    Position player = {9, 11};
    Position playerStart = player;

    for (int y = 0; y < static_cast<int>(grid.size()); ++y) {
        for (int x = 0; x < static_cast<int>(grid[y].size()); ++x) {
            if (grid[y][x] == 'P') {
                player = {x, y};
                playerStart = player;
                grid[y][x] = ' ';
            }
        }
    }

    std::vector<Ghost> ghosts = {
        {{8, 9}, {8, 9}},
        {{9, 9}, {9, 9}},
        {{10, 9}, {10, 9}},
        {{11, 9}, {11, 9}}
    };

    int score = 0;
    int lives = 3;
    int powerTicks = 0;
    int playerDx = 0;
    int playerDy = 0;
    int requestedDx = 0;
    int requestedDy = 0;
    bool running = true;
    bool won = false;
    std::random_device randomDevice;
    std::mt19937 randomEngine(randomDevice());
    std::uniform_int_distribution<int> directionDistribution(0, 3);

    termios original;
    rawMode(original);

    auto cleanup = [&]() {
        tcsetattr(STDIN_FILENO, TCSANOW, &original);
        std::cout << "\033[2J\033[H\033[?25h";
    };

    std::cout << "\033[?25l";

    while (running) {
        char key = readKey();
        if (key == 'w' || key == 'W') {
            requestedDx = 0;
            requestedDy = -1;
        } else if (key == 's' || key == 'S') {
            requestedDx = 0;
            requestedDy = 1;
        } else if (key == 'a' || key == 'A') {
            requestedDx = -1;
            requestedDy = 0;
        } else if (key == 'd' || key == 'D') {
            requestedDx = 1;
            requestedDy = 0;
        } else if (key == 'q' || key == 'Q') {
            running = false;
        }

        int nextX = (player.x + requestedDx + static_cast<int>(grid[0].size()))
                    % static_cast<int>(grid[0].size());
        int nextY = player.y + requestedDy;
        if (!isWall(grid, nextX, nextY)) {
            playerDx = requestedDx;
            playerDy = requestedDy;
        }

        nextX = (player.x + playerDx + static_cast<int>(grid[0].size()))
                % static_cast<int>(grid[0].size());
        nextY = player.y + playerDy;
        if (!isWall(grid, nextX, nextY)) {
            player.x = nextX;
            player.y = nextY;

            if (grid[player.y][player.x] == '.') {
                grid[player.y][player.x] = ' ';
                score += 10;
            } else if (grid[player.y][player.x] == 'o') {
                grid[player.y][player.x] = ' ';
                score += 50;
                powerTicks = 50;
            }
        }

        if (powerTicks > 0) {
            --powerTicks;
        }

        for (size_t i = 0; i < ghosts.size(); ++i) {
            int dx = 0;
            int dy = 0;
            bool moved = false;

            if (powerTicks == 0 && i % 2 == 0) {
                dx = (player.x > ghosts[i].position.x) ? 1 : (player.x < ghosts[i].position.x) ? -1 : 0;
                dy = (player.y > ghosts[i].position.y) ? 1 : (player.y < ghosts[i].position.y) ? -1 : 0;

                if (dx != 0) {
                    int tryX = (ghosts[i].position.x + dx + static_cast<int>(grid[0].size()))
                               % static_cast<int>(grid[0].size());
                    if (!isWall(grid, tryX, ghosts[i].position.y)) {
                        ghosts[i].position.x = tryX;
                        moved = true;
                    }
                }
                if (!moved && dy != 0) {
                    int tryY = ghosts[i].position.y + dy;
                    if (!isWall(grid, ghosts[i].position.x, tryY)) {
                        ghosts[i].position.y = tryY;
                        moved = true;
                    }
                }
            }

            if (!moved) {
                const int directions[4][2] = {{0, -1}, {0, 1}, {-1, 0}, {1, 0}};
                for (int attempt = 0; attempt < 4 && !moved; ++attempt) {
                    int choice = directionDistribution(randomEngine);
                    dx = directions[choice][0];
                    dy = directions[choice][1];
                    int tryX = (ghosts[i].position.x + dx + static_cast<int>(grid[0].size()))
                               % static_cast<int>(grid[0].size());
                    int tryY = ghosts[i].position.y + dy;
                    if (!isWall(grid, tryX, tryY)) {
                        ghosts[i].position.x = tryX;
                        ghosts[i].position.y = tryY;
                        moved = true;
                    }
                }
            }

            if (ghosts[i].position.x == player.x && ghosts[i].position.y == player.y) {
                if (powerTicks > 0) {
                    score += 200;
                    ghosts[i].position = ghosts[i].start;
                } else {
                    --lives;
                    if (lives <= 0) {
                        running = false;
                    } else {
                        player = playerStart;
                        playerDx = 0;
                        playerDy = 0;
                        requestedDx = 0;
                        requestedDy = 0;
                    }
                }
            }
        }

        bool dotsLeft = false;
        for (const std::string& row : grid) {
            if (row.find('.') != std::string::npos || row.find('o') != std::string::npos) {
                dotsLeft = true;
                break;
            }
        }

        if (!dotsLeft) {
            ++level;
            if (level >= static_cast<int>(levels.size())) {
                running = false;
                won = true;
            } else {
                grid = levels[level];
                player = {9, 11};
                playerStart = player;
                powerTicks = 0;
            }
        }

        std::cout << "\033[2J\033[H";
        std::cout << "C++ PAC-MAN  |  Score: " << score << "  Lives: " << lives
                  << "  Level: " << level + 1 << "\n";
        for (int y = 0; y < static_cast<int>(grid.size()); ++y) {
            for (int x = 0; x < static_cast<int>(grid[y].size()); ++x) {
                bool printedGhost = false;
                for (size_t i = 0; i < ghosts.size(); ++i) {
                    if (ghosts[i].position.x == x && ghosts[i].position.y == y) {
                        std::cout << (powerTicks > 0 ? 'G' : 'M');
                        printedGhost = true;
                        break;
                    }
                }
                if (printedGhost) {
                    continue;
                }
                if (player.x == x && player.y == y) {
                    std::cout << 'C';
                } else if (grid[y][x] == '#') {
                    std::cout << '#';
                } else if (grid[y][x] == '.') {
                    std::cout << '.';
                } else if (grid[y][x] == 'o') {
                    std::cout << 'O';
                } else if (grid[y][x] == '-') {
                    std::cout << '-';
                } else {
                    std::cout << ' ';
                }
            }
            std::cout << '\n';
        }
        std::cout << "Move: WASD  Quit: Q\n";
        std::cout.flush();

        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }

    cleanup();
    if (won) {
        std::cout << "You cleared both levels! Final score: " << score << "\n";
    } else if (lives <= 0) {
        std::cout << "Game over! Final score: " << score << "\n";
    } else {
        std::cout << "Thanks for playing! Final score: " << score << "\n";
    }

    return 0;
}
