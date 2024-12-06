import pygame
import sys
import random
import math


# Initialize Pygame
pygame.init()

# Screen settings
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("ChewPacabra")

# Colors
BACKGROUND_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
PACMAN_COLOR = (255, 255, 0)
GHOST_COLOR = (255, 0, 0)
DOT_COLOR = (255, 255, 255)
WALL_COLOR = (0, 0, 128)
POWERUP_COLOR = (255, 223, 0)
EXIT_COLOR = (0, 255, 0)
IMMUNITY_COLOR = (0, 255, 255)


# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Sounds
pygame.mixer.music.load("assets/Juhani Junkala [Chiptune Adventures] 1. Stage 1.ogg")
pygame.mixer.music.set_volume(0.5)
dot_sound = pygame.mixer.Sound("assets/apple_bite.ogg")
level_complete_sound = pygame.mixer.Sound("assets/Juhani Junkala [Chiptune Adventures] 2. Stage 2.ogg")
game_over_sound = pygame.mixer.Sound("assets/ThisGameIsOver.wav")
powerup_sound = pygame.mixer.Sound("assets/invincible.wav")

# Game variables
tile_size = 50
pacman = {"x": 50, "y": 50, "radius": 15, "speed": 5, "chomp_open": True}
ghosts = [{"x": 400, "y": 300, "speed": 3, "dx": random.choice([-1, 1]), "dy": random.choice([-1, 1])} for _ in range(5)]  # Added an extra ghost
score = 0
lives = 3
game_over = False
level_complete = False
immunity_time = 0
current_level = 1

# Maze layout (0 = path, 1 = wall, 2 = dot, 3 = power-up, 4 = exit)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 2, 0, 1, 0, 0, 0, 1, 0, 2, 0, 3, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 2, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 1, 0, 2, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1],
    [1, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 4, 1],  # Exit here (bottom left)
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 2, 1, 0, 2, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1],
    [1, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


# Helper functions
def draw_maze():
    """Draw the maze with walls, dots, power-ups, and the exit."""
    for row_index, row in enumerate(maze):
        for col_index, tile in enumerate(row):
            x, y = col_index * tile_size, row_index * tile_size
            if tile == 1:  # Wall
                pygame.draw.rect(screen, WALL_COLOR, (x, y, tile_size, tile_size))
            elif tile == 2:  # Dot
                pygame.draw.circle(screen, DOT_COLOR, (x + tile_size // 2, y + tile_size // 2), 5)
            elif tile == 3:  # Power-up
                pygame.draw.circle(screen, POWERUP_COLOR, (x + tile_size // 2, y + tile_size // 2), 10)
            elif tile == 4:  # Exit
                pygame.draw.rect(screen, EXIT_COLOR, (x, y, tile_size, tile_size))


def can_move(x, y):
    """Check if a position is within the maze and not a wall."""
    tile_x, tile_y = int(x // tile_size), int(y // tile_size)
    if 0 <= tile_x < len(maze[0]) and 0 <= tile_y < len(maze):
        return maze[tile_y][tile_x] != 1
    return False


def move_ghosts():
    """Move ghosts and make them bounce off walls."""
    for ghost in ghosts:
        next_x = ghost["x"] + ghost["speed"] * ghost["dx"]
        next_y = ghost["y"] + ghost["speed"] * ghost["dy"]

        # Check for wall collisions
        if not can_move(next_x, ghost["y"]):
            ghost["dx"] *= -1
        if not can_move(ghost["x"], next_y):
            ghost["dy"] *= -1

        ghost["x"] += ghost["speed"] * ghost["dx"]
        ghost["y"] += ghost["speed"] * ghost["dy"]


def eat_dot():
    """Check if Pac-Man eats a dot or a power-up and update the score."""
    global score, immunity_time
    tile_x, tile_y = int(pacman["x"] // tile_size), int(pacman["y"] // tile_size)
    if maze[tile_y][tile_x] == 2:
        maze[tile_y][tile_x] = 0
        score += 10
        dot_sound.play()
    elif maze[tile_y][tile_x] == 3:
        maze[tile_y][tile_x] = 0
        immunity_time = pygame.time.get_ticks() + 7000
        powerup_sound.play()


def check_collisions():
    """Check if Pac-Man collides with a ghost."""
    global lives, game_over
    if immunity_time > pygame.time.get_ticks():
        return
    for ghost in ghosts:
        distance = math.sqrt((pacman["x"] - ghost["x"]) ** 2 + (pacman["y"] - ghost["y"]) ** 2)
        if distance < pacman["radius"] * 2:
            lives -= 1
            if lives <= 0:
                game_over = True
            return


def draw_pacman():
    """Draw Pac-Man with chomping animation."""
    mouth_angle = 30 if pacman["chomp_open"] else 0
    pacman["chomp_open"] = not pacman["chomp_open"]
    pygame.draw.arc(screen, PACMAN_COLOR,
                    (pacman["x"] - pacman["radius"], pacman["y"] - pacman["radius"],
                     pacman["radius"] * 2, pacman["radius"] * 2),
                    math.radians(mouth_angle),
                    math.radians(360 - mouth_angle),
                    pacman["radius"])


def draw_immunity_timer():
    """Draw the immunity timer (if Pac-Man has a power-up)."""
    if immunity_time > pygame.time.get_ticks():
        pygame.draw.circle(screen, IMMUNITY_COLOR,
                           (pacman["x"], pacman["y"]), pacman["radius"] + 5, 5)


def check_win_condition():
    """Check if Pac-Man has reached the exit."""
    tile_x, tile_y = int(pacman["x"] // tile_size), int(pacman["y"] // tile_size)
    return maze[tile_y][tile_x] == 4


# Game loop
pygame.mixer.music.play(-1)  # Loop background music
while True:
    screen.fill(BACKGROUND_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if game_over:
        game_over_text = large_font.render("GAME OVER", True, TEXT_COLOR)
        screen.blit(game_over_text, (width // 2 - 150, height // 2 - 36))
        pygame.display.flip()
        continue

    if level_complete:
        level_complete_text = large_font.render("LEVEL COMPLETE!", True, TEXT_COLOR)
        screen.blit(level_complete_text, (width // 2 - 230, height // 2 - 36))
        pygame.display.flip()
        pygame.time.delay(2000)
        level_complete = False
        current_level += 1  # Proceed to the next level

    if check_win_condition():
        level_complete = True
        pygame.mixer.music.stop()
        level_complete_sound.play()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and can_move(pacman["x"] - pacman["speed"], pacman["y"]):
        pacman["x"] -= pacman["speed"]
    if keys[pygame.K_RIGHT] and can_move(pacman["x"] + pacman["speed"], pacman["y"]):
        pacman["x"] += pacman["speed"]
    if keys[pygame.K_UP] and can_move(pacman["x"], pacman["y"] - pacman["speed"]):
        pacman["y"] -= pacman["speed"]
    if keys[pygame.K_DOWN] and can_move(pacman["x"], pacman["y"] + pacman["speed"]):
        pacman["y"] += pacman["speed"]

    move_ghosts()
    eat_dot()
    check_collisions()
    draw_maze()
    draw_pacman()
    draw_immunity_timer()

    # Draw the score and lives
    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_text, (10, 10))
    lives_text = font.render(f"Lives: {lives}", True, TEXT_COLOR)
    screen.blit(lives_text, (10, 40))

    # Draw ghosts
    for ghost in ghosts:
        pygame.draw.circle(screen, GHOST_COLOR, (int(ghost["x"]), int(ghost["y"])), 15)

    pygame.display.flip()
    pygame.time.Clock().tick(15)
