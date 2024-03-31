import pygame
from gleba.util import *


class Node:  # The base class for all nodes
    def __init__(self):
        self.parent = None
        self.children = []

        self.window = None

        self.name = type(self).__name__
        self.active_signals: list[str] = []
        self.signals_to_remove: list[str] = []  # This list is to make sure that signals get emitted only once

        self.is_ready = False

    def add_child(self, child):
        child.parent = self
        child.window = self.window

        self.children.append(child)
        if self.is_ready:
            child.is_ready = True
            child.ready()

    def remove_self(self):
        self.parent.children.remove(self)

    def update(self):
        for child in self.children:
            if child.is_ready:
                child.update()

        for signal in self.signals_to_remove:
            self.signals_to_remove.remove(signal)
            self.active_signals.remove(signal)

        for signal in self.active_signals:
            self.signals_to_remove.append(signal)

    def ready(self):
        pass

    def emit(self, signal):
        self.active_signals.append(signal)

    def is_active(self, signal):
        return signal in self.active_signals


def get_mouse_position():
    mouse = pygame.mouse.get_pos()
    return Point(mouse[0], mouse[1])


def get_offset_mouse_position(offset):
    mouse = get_mouse_position()
    return Point(mouse.x - offset.x, mouse.y - offset.y)


class Window(Node):
    def __init__(self, size: Point, fps: int, name="Gleba Project", mouse_visible: bool = True):
        super().__init__()
        self.window = self  # Look at me, I am the window now

        self.is_ready = True
        self.size = size
        self.fps = fps

        self.screen = pygame.display.set_mode(self.size.to_tuple())

        self.keys_pressed = None  # pygame.key.get_pressed()
        self.events = None  # pygame.event.get()

        pygame.display.set_caption(name)
        pygame.init()

        self.running = True

        if not mouse_visible:
            pygame.mouse.set_visible(False)

    def run(self):
        clock = pygame.time.Clock()
        for c in self.children:
            c.ready()

        # Game loop
        while self.running:
            self.keys_pressed = pygame.key.get_pressed()
            self.events = pygame.event.get()

            for event in self.events:  # Quit on close button
                if event.type == pygame.QUIT:
                    quit()

            super().update()

            pygame.display.flip()
            clock.tick(self.fps)

    def stop(self):
        self.running = False
        self.children = []


class Timer(Node):
    def __init__(self, secs, self_destruct=False):
        super().__init__()
        self.secs = secs*2  # Why is x2?

        self.self_destruct = self_destruct
        self.time_left = -1
        self.max_value = -1

    def update(self):
        if self.is_active("timeout"):
            if self.self_destruct:
                self.remove_self()
            else:
                self.ready()

        if self.time_left <= 0:
            self.emit("timeout")

        self.time_left -= 1
        super().update()

    def ready(self):
        self.max_value = self.secs * self.window.fps
        self.time_left = self.max_value

    def get_percent(self):  # From 0 to 1
        if self.time_left <= 0:
            return 0
        return self.time_left / self.max_value
