from gleba.core import *

pygame.mixer.init()


def play(path, volume=1, loop=False):
    sound = pygame.mixer.Sound(path)
    loops = 0

    sound.set_volume(volume)

    if loop:
        loops = -1

    sound.play(loops=loops)
