import math


class Ball:

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

        self.radius = 11

        self.vx = 0
        self.vy = 0

    def update(self, field):

        self.x += self.vx
        self.y += self.vy

        # ralentissement
        self.vx *= 0.97
        self.vy *= 0.97

        if abs(self.vx) < 0.05:
            self.vx = 0

        if abs(self.vy) < 0.05:
            self.vy = 0

        # murs haut/bas
        if self.y < field.top + self.radius:
            self.y = field.top + self.radius
            self.vy *= -0.55

        if self.y > field.bottom - self.radius:
            self.y = field.bottom - self.radius
            self.vy *= -0.55

    def kick(self, direction_x, direction_y, power=11):

        length = math.sqrt(
            direction_x ** 2 +
            direction_y ** 2
        )

        if length == 0:
            return

        direction_x /= length
        direction_y /= length

        self.vx = direction_x * power
        self.vy = direction_y * power
