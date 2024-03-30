from gleba.core import *


class Node2D(Node):  # Base node for all 2D Objects
    def __init__(self, position: Point):
        super().__init__()
        self.position = position
        self.offset = Point(0, 0)
        self.color = Color(255, 255, 255)
        self.rotation = 0

        self.clip = None

    def get_position(self):
        return Point(self.position.x + self.offset.x, self.position.y + self.offset.y)

    def update(self):
        if isinstance(self.parent, Node2D):
            self.offset = self.parent.position
        super().update()

    def render(self, surface: pygame.Surface, centered=False):
        if self.color.a != 255:  # Alpha
            surface.set_alpha(self.color.a)
        if self.color.to_rgb() != (255, 255, 255):  # Modulate
            surface.fill(self.color.to_rgb(), surface.get_rect(), pygame.BLEND_RGBA_MULT)

        if self.rotation != 0:
            surface = pygame.transform.rotate(surface, self.rotation)

        # If clip is defined, clip the surface
        if self.clip:
            surface = surface.subsurface((0, 0, self.clip.x, self.clip.y))

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
    def __init__(self, color=Color(0, 0, 0)):
        super().__init__()
        self.color = color

    def update(self):
        super().update()  # Not really needed because why would a Background Color have children?
        self.window.screen.fill(self.color.to_tuple())


class Image(Node2D):
    def __init__(self, path: str, position: Point, size: Point, centered=False):
        super().__init__(position)

        self.path = path
        self.size = size
        self.centered = centered

    def update(self):
        super().update()
        surface = pygame.image.load(self.path)
        surface = pygame.transform.scale(surface, self.size.to_tuple())

        self.render(surface, self.centered)
