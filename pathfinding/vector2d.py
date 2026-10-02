import math


class Vector2D:
    def __init__(self, x=0, y=0):
        self.x = float(x)
        self.y = float(y)

    def add(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def subtract(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def scale(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

    def abs(self):
        return math.hypot(self.x, self.y)

    def distance(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f"({self.x:g}, {self.y:g})"