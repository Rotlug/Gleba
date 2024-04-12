import pygame.pixelcopy

from gleba.core import *


class Node2D(Node):  # Base node for all 2D Objects
    def __init__(self, position: Point):
        super().__init__()
        self.position = position
        self.color = Color(255, 255, 255)
        self.rotation = 0

        self.surface = None
        self.centered = False

        self.clip = None

    def get_position(self):  # Find the global position of the node on-screen
        pos = Point(0, 0)
        node = self

        while isinstance(node, Node2D):
            pos.x += node.position.x
            pos.y += node.position.y
            node = node.parent

        return pos

    def update(self):
        if self.surface:
            self.render()

        super().update()

    def render(self):
        if self.color.a != 255:  # Alpha
            self.surface.set_alpha(self.color.a)
        if self.color.to_rgb() != (255, 255, 255):  # Modulate
            self.surface.fill(self.color.to_rgb(), self.surface.get_rect(), pygame.BLEND_RGBA_MULT)

        if self.rotation != 0:
            self.surface = pygame.transform.rotate(self.surface, self.rotation)

        # If clip is defined, clip the surface
        if self.clip:
            self.surface = self.surface.subsurface((0, 0, self.clip.x, self.clip.y))

        # If the rect variable is defined, render using that, if not, just render using the position.
        if self.centered:
            rect = self.surface.get_rect(center=self.get_position().to_tuple())
            self.window.screen.blit(self.surface, rect)
        else:
            self.window.screen.blit(self.surface, self.get_position().to_tuple())


class Rect(Node2D):
    def __init__(self, position: Point, size: Point, color):
        super().__init__(position)
        self.size = size
        self.color = color

    def update(self):
        self.surface = pygame.Surface(self.size.to_tuple()).convert_alpha()
        self.surface.fill(self.color.to_rgb())
        super().update()


class BackgroundColor(Node):
    def __init__(self, color=Color(0, 0, 0)):
        super().__init__()
        self.color = color

    def update(self):
        super().update()  # Not really needed because why would a Background Color have children?
        self.window.screen.fill(self.color.to_tuple())


class Image(Node2D):
    def __init__(self, path: str, position: Point, size: Point):
        super().__init__(position)

        self.path = path
        self.size = size
        self.img = pygame.image.load(self.path)

    def update(self):
        self.surface = self.img
        self.surface = pygame.transform.scale(self.surface, self.size.to_tuple())
        super().update()

    def set_image(self, path):
        self.img = pygame.image.load(path)
