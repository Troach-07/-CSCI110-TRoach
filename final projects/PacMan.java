import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.Scanner;

public class PacMan {
    private static final String[][] LEVELS = {
        {
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
        },
        {
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
        }
    };

    private static final int[][] DIRECTIONS = {{0, -1}, {0, 1}, {-1, 0}, {1, 0}};
    private static final Random RANDOM = new Random();
    private static char[][] maze;
    private static int level;
    private static int score;
    private static int lives = 3;
    private static int powerTurns;
    private static Position player;
    private static Position playerStart;
    private static final List<Position> ghosts = new ArrayList<>();
    private static final List<Position> ghostStarts = new ArrayList<>();

    private static final class Position {
        int x;
        int y;

        Position(int x, int y) {
            this.x = x;
            this.y = y;
        }
    }

    private static void loadLevel(int number) {
        level = number;
        maze = new char[LEVELS[level].length][];
        for (int y = 0; y < maze.length; y++) {
            maze[y] = LEVELS[level][y].toCharArray();
            for (int x = 0; x < maze[y].length; x++) {
                if (maze[y][x] == 'P') {
                    player = new Position(x, y);
                    playerStart = new Position(x, y);
                    maze[y][x] = ' ';
                }
            }
        }
        ghosts.clear();
        ghostStarts.clear();
        int[][] starts = {{9, 10}, {10, 10}, {11, 10}, {10, 9}};
        for (int[] start : starts) {
            ghosts.add(new Position(start[0], start[1]));
            ghostStarts.add(new Position(start[0], start[1]));
        }
        powerTurns = 0;
    }

    private static boolean canMove(int x, int y) {
        return y >= 0 && y < maze.length
            && x >= 0 && x < maze[y].length
            && maze[y][x] != '#';
    }

    private static void draw() {
        System.out.println("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n");
        System.out.printf("PAC-MAN  Score: %d  Lives: %d  Level: %d/%d%n",
            score, lives, level + 1, LEVELS.length);
        for (int y = 0; y < maze.length; y++) {
            for (int x = 0; x < maze[y].length; x++) {
                char cell = maze[y][x];
                if (player.x == x && player.y == y) {
                    System.out.print('C');
                } else {
                    boolean ghostHere = false;
                    for (int i = 0; i < ghosts.size(); i++) {
                        if (ghosts.get(i).x == x && ghosts.get(i).y == y) {
                            System.out.print(powerTurns > 0 ? 'g' : 'M');
                            ghostHere = true;
                            break;
                        }
                    }
                    if (!ghostHere) {
                        System.out.print(cell == '#' ? '#' : cell == '.' ? '.' : cell == 'o' ? 'O' : ' ');
                    }
                }
            }
            System.out.println();
        }
        System.out.println("Move with W/A/S/D, then press Enter. Q quits.");
        if (powerTurns > 0) {
            System.out.println("Power pellet active!");
        }
    }

    private static void moveGhosts() {
        for (int i = 0; i < ghosts.size(); i++) {
            Position ghost = ghosts.get(i);
            int[] direction = DIRECTIONS[RANDOM.nextInt(DIRECTIONS.length)];
            int nextX = ghost.x + direction[0];
            int nextY = ghost.y + direction[1];
            if (canMove(nextX, nextY)) {
                ghost.x = nextX;
                ghost.y = nextY;
            }

            if (ghost.x == player.x && ghost.y == player.y) {
                if (powerTurns > 0) {
                    score += 200;
                    ghost.x = ghostStarts.get(i).x;
                    ghost.y = ghostStarts.get(i).y;
                } else {
                    lives--;
                    if (lives > 0) {
                        player = new Position(playerStart.x, playerStart.y);
                        return;
                    }
                }
            }
        }
    }

    private static boolean dotsRemain() {
        for (char[] row : maze) {
            for (char cell : row) {
                if (cell == '.' || cell == 'o') {
                    return true;
                }
            }
        }
        return false;
    }

    public static void main(String[] args) {
        loadLevel(0);
        boolean quit = false;
        try (Scanner input = new Scanner(System.in)) {
            while (lives > 0 && !quit) {
                draw();
                if (!input.hasNextLine()) {
                    break;
                }
                String line = input.nextLine().trim().toLowerCase();
                if (line.isEmpty()) {
                    continue;
                }
                char key = line.charAt(0);
                if (key == 'q') {
                    quit = true;
                    break;
                }

                int dx = 0;
                int dy = 0;
                if (key == 'w') dy = -1;
                else if (key == 's') dy = 1;
                else if (key == 'a') dx = -1;
                else if (key == 'd') dx = 1;
                else continue;

                int nextX = player.x + dx;
                int nextY = player.y + dy;
                if (canMove(nextX, nextY)) {
                    player.x = nextX;
                    player.y = nextY;
                    if (maze[nextY][nextX] == '.') {
                        score += 10;
                        maze[nextY][nextX] = ' ';
                    } else if (maze[nextY][nextX] == 'o') {
                        score += 50;
                        powerTurns = 10;
                        maze[nextY][nextX] = ' ';
                    }
                }

                moveGhosts();
                if (powerTurns > 0) powerTurns--;
                if (lives > 0 && !dotsRemain()) {
                    if (level + 1 == LEVELS.length) {
                        break;
                    }
                    loadLevel(level + 1);
                }
            }
        }

        if (lives <= 0) {
            System.out.println("Game over! Final score: " + score);
        } else if (level == LEVELS.length - 1 && !dotsRemain()) {
            System.out.println("You cleared both levels! Final score: " + score);
        } else {
            System.out.println("Thanks for playing! Final score: " + score);
        }
    }
}
