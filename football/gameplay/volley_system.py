import math
import random


class VolleySystem:
    def __init__(self, match):
        self.match = match
        self.enabled = True
        self.range = 50.0
        self.power = 11.0

    def can_volley(self, player):
        if player is None:
            return False

        if self.match.ball_owner is not None:
            return False

        distance = math.sqrt(
            (player.x - self.match.ball_x) ** 2 +
            (player.y - self.match.ball_y) ** 2
        )

        return distance <= self.range

    def volley(self, player, target_x, target_y):
        if not self.enabled:
            return False

        if not self.can_volley(player):
            return False

        dx = target_x - player.x
        dy = target_y - player.y

        length = math.sqrt(dx * dx + dy * dy)

        if length <= 0:
            return False

        accuracy = getattr(player, "volley_rating", 70) / 100.0

        if random.random() > accuracy:
            self.match.ball_vx = dx / length * 4.0
            self.match.ball_vy = dy / length * 4.0
            return False

        dx /= length
        dy /= length

        self.match.ball_vx = dx * self.power
        self.match.ball_vy = dy * self.power
        self.match.ball_owner = None

        return True

    def update(self):
        pass

    def reset(self):
        pass
