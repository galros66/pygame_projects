from enum import Enum
import pygame
import os
DIR = R"C:\ws\pygame_projects\utils\sounds"
class Sound(Enum):
    pygame.mixer.init()
    HIT = pygame.mixer.Sound(os.path.join(DIR, "tap.wav"))
    WIN = pygame.mixer.Sound(os.path.join(DIR, "treasure.wav"))