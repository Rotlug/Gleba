# Utility Classes


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_tuple(self): return self.x, self.y


class Color:
    def __init__(self, r, g, b, a=255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def to_tuple(self):
        if self.a == 255:
            return self.r, self.g, self.b
        else:
            return self.r, self.g, self.b, self.a

    def to_rgb(self): return self.r, self.g, self.b