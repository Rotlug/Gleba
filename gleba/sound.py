from gleba.core import *

pygame.mixer.init()

def play(path, loop=False):
    sound = pygame.mixer.Sound(path)
    loops = 0

    if loop:
        loops = -1

    sound.play(loops=loops)

