import pygame
from gleba.util import *


class Node:  # The base class for all nodes
    def __init__(self):
        self.parent = None
        self.children = []
        self.window = None

        self.name = str(type(self))

    def add_child(self, child):
        child.parent = self
        child.window = self.window
        self.children.append(child)

    def remove_self(self):
        self.parent.children.remove(self)

    def update(self):
        for child in self.children:
            child.update()


def get_mouse_position():
    mouse = pygame.mouse.get_pos()
    return Point(mouse[0], mouse[1])


def get_offset_mouse_position(offset):
    mouse = get_mouse_position()
    return Point(mouse.x - offset.x, mouse.y - offset.y)


class Window(Node):
    def __init__(self, size: Point, fps: int, name="Gleba Project", mouse_visible: bool=True):
        super().__init__()

        self.window = self  # Look at me, I am the window now

        self.size = size
        self.fps = fps

        self.screen = pygame.display.set_mode(self.size.to_tuple())

        self.keys_pressed = {}  # pygame.key.get_pressed()

        pygame.display.set_caption(name)
        if not mouse_visible: pygame.mouse.set_visible(False)
    def run(self):
        pygame.init()
        running = True
        clock = pygame.time.Clock()

        # Game loop
        while running:
            self.keys_pressed = pygame.key.get_pressed()

            for event in pygame.event.get():  # Quit on close button
                if event.type == pygame.QUIT:
                    running = False

            super().update()

            pygame.display.flip()
            clock.tick(self.fps)
