from gleba import *

collision_objects = []


class CollisionRect(Node2D):
    def __init__(self):
        super().__init__(position=Point(0, 0))
        self.currently_colliding = []

    def ready(self):
        collision_objects.append(self)

    def remove_self(self):
        collision_objects.remove(self)
        super().remove_self()

    def update(self):
        super().update()

    def get_colliding(self):
        if self.parent.surface is None:
            return []

        current_cols = []

        global collision_objects
        for col in collision_objects:
            if (col is self) or (col.parent.surface is None):
                continue

            my_rect: pygame.Rect = self.parent.get_rect()
            collider_rect: pygame.Rect = col.parent.get_rect()

            if my_rect.colliderect(collider_rect):
                current_cols.append(col)

        return current_cols
