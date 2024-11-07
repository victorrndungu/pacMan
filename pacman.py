import pygame
import sys
import math
import random

# Initialize pygame modules
pygame.init()

# Screen settings
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pac-Man Game")

# Colors
background_color = (0, 0, 0)
pacman_color = (255, 255, 0)
ghost_color = (255, 0, 0)
wall_color = (0, 0, 255)
dot_color = (0, 255, 255)
confetti_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]

# Game settings
pacman = {"x": 80, "y": 100, "radius": 20, "speed": 10, "mouth_angle": 0}
ghosts = [{"x": random.randint(200, width - 100), "y": random.randint(100, height - 100),
           "speed_x": random.choice([-3, 3]), "speed_y": random.choice([-3, 3])} for _ in range(3)]
walls = [pygame.Rect(100, 100, 250, 10), pygame.Rect(450, 100, 250, 10),
         pygame.Rect(100, 490, 600, 10), pygame.Rect(100, 100, 10, 400), pygame.Rect(690, 100, 10, 400)]
dots = [(200 + i * 50, 300) for i in range(10)]
score, game_over, win = 0, False, False
font = pygame.font.Font(None, 36)

