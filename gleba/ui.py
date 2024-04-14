import pygame

from gleba.graphics import *
from copy import copy


class Font:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def get_font(self):
        return pygame.font.SysFont(self.name, self.size)


class Text(Node2D):
    def __init__(self, text, position, font: Font, font_color=Color(255, 255, 255)):
        super().__init__(position)
        self.text = text
        self.font = font
        self.font_color = font_color

    def ready(self):
        self.update_text(self.text)

    def update_text(self, text):
        self.text = text
        self.surface = self.font.get_font().render(self.text, False, self.font_color.to_tuple())


class ProgressBar(Node2D):
    def __init__(self, position, sprite: Node2D):
        super().__init__(position)

        self.sprite = sprite

        self.sprite.clip = copy(self.sprite.size)
        self.max_x = sprite.size.x

    def ready(self):
        self.add_child(self.sprite)

    def set_value(self, val):
        self.sprite.clip.x = (1-val) * self.max_x


class Button(Node2D):
    def __init__(self, position: Point, foreground: Node2D):
        super().__init__(position)
        self.foreground = foreground
        self.hovered = False

    def ready(self):
        self.add_child(self.foreground)

    def update(self):
        if self.foreground.surface:  # If the foreground has a surface
            mouse_pos = get_offset_mouse_position(self.foreground.get_position()).to_tuple()
            is_hovered = self.foreground.surface.get_rect().collidepoint(mouse_pos)

            if is_hovered and not self.hovered:  # Emit mouse_hovered and mouse_exited
                self.emit("mouse_entered")
                self.hovered = True
            elif not is_hovered and self.hovered:
                self.emit("mouse_exited")
                self.hovered = False

            # Emit signal on pressed
            for e in self.window.events:
                if e.type == pygame.MOUSEBUTTONDOWN and self.hovered:
                    self.emit("pressed")

        super().update()
