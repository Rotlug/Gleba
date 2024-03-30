from gleba.core import *


class Node2D(Node):  # Base node for all 2D Objects
    def __init__(self, position: Point):
        super().__init__()
        self.position = position
        self.offset = Point(0, 0)
        self.color = Color(255, 255, 255)
        self.rotation = 0

    def get_position(self):
        return Point(self.position.x + self.offset.x, self.position.y + self.offset.y)

    def update(self):
        if isinstance(self.parent, Node2D):
            self.offset = self.parent.position

        super().update()

    def render(self, surface: pygame.Surface, centered=True):
        if self.color.a != 255:  # Alpha
            surface.set_alpha(self.color.a)
        if self.color.to_rgb() != (255, 255, 255):  # Modulate
            surface.fill(self.color.to_rgb(), surface.get_rect(), pygame.BLEND_RGBA_MULT)

        if self.rotation != 0:
            surface = pygame.transform.rotate(surface, self.rotation)

        # If the rect variable is defined, render using that, if not, just render using the position.
        if centered:
            rect = surface.get_rect(center=self.get_position().to_tuple())
            self.window.screen.blit(surface, rect)
        else:
            self.window.screen.blit(surface, self.get_position().to_tuple())


class Rect(Node2D):
    def __init__(self, position: Point, size: Point, color):
        super().__init__(position)
        self.size = size
        self.color = color

    def update(self):
        super().update()
        surface = pygame.Surface(self.size.to_tuple()).convert_alpha()
        surface.fill(self.color.to_rgb())
        self.render(surface)


class BackgroundColor(Node):
    def __init__(self, color):
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

    def update(self):
        super().update()
        surface = pygame.image.load(self.path)
        surface = pygame.transform.scale(surface, self.size.to_tuple())

        self.render(surface, True)

    def center_offset(self):
        # The image is centered so offset the position
        self.position.x += self.size.x // 2
        self.position.y += self.size.y // 2

