from gleba.core import *


class Node2D(Node):  # Base node for all 2D Objects
    def __init__(self, initial_position: Point):
        super().__init__()
        self.position = initial_position
        self.offset = Point(0, 0)

    def get_position(self):
        return Point(self.position.x + self.offset.x, self.position.y + self.offset.y)

    def update(self):
        if isinstance(self.parent, Node2D):
            self.offset = self.parent.position
        super().update()


class Rect(Node2D):
    def __init__(self, position: Point, size: Point, color):
        super().__init__(position)
        self.size = size
        self.color = color

    def update(self):
        super().update()
        pos = self.get_position()

        rect = pygame.Rect(pos.x, pos.y, self.size.x, self.size.y)
        pygame.draw.rect(self.window.screen, self.color, rect)


class BackgroundColor(Node):
    def __init__(self, color):
        super().__init__()
        self.color = color

    def update(self):
        super().update()  # Not really needed because why would a Background Color have children?
        self.window.screen.fill(self.color)


class Image(Node2D):
    def __init__(self, path: str, position: Point, size: Point, color=(255, 255, 255, 255)):
        super().__init__(position)

          # The image itself

        self.img = None
        self.path = path
        self.size = size

        self.rotation = 0
        self.color = color

    def update(self):
        super().update()

        self.img = pygame.image.load(self.path)

        self.img = self.img.copy()

        self.img = pygame.transform.scale(self.img, self.size.to_tuple())

        if self.rotation != 0:
            self.img = pygame.transform.rotate(self.img, self.rotation)

        # This is so the image is rotated around it's center and not around the top left
        rect = self.img.get_rect(center=self.get_position().to_tuple())

        if self.color != (255, 255, 255, 255):
            self.img.fill(self.color, self.img.get_rect(), pygame.BLEND_RGBA_MULT)

        self.window.screen.blit(self.img, rect)

    def center_offset(self):
        # The image is centered so offset the position
        self.position.x += self.size.x // 2
        self.position.y += self.size.y // 2
