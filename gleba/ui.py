from gleba.graphics import *


class Font:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def get_font(self):
        return pygame.font.SysFont(self.name, self.size)


class Text(Node2D):
    def __init__(self, text, position, font: Font, font_color):
        super().__init__(position)
        self.text = text
        self.font = font
        self.font_color = font_color

        self.surface = None

    def ready(self):
        self.update_text()

    def update_text(self):
        self.surface = self.font.get_font().render(self.text, False, self.font_color.to_tuple())

    def update(self):
        if self.surface:
            self.render(self.surface)


class ProgressBar(Node2D):
    def __init__(self, position, foreground: Node2D, background: Node2D, timer: Timer):
        super().__init__(position)

        self.background = background
        self.foreground = foreground

        self.foreground.clip = Point(self.foreground.size.x, self.foreground.size.y)

        self.max_x = foreground.size.x
        self.timer = timer

    def ready(self):
        self.add_child(self.background)
        self.add_child(self.foreground)
        self.add_child(self.timer)

    def update(self):
        super().update()
        self.foreground.clip.x = self.max_x * self.timer.get_percent()
