import math


class CrossSystem:
    def __init__(self, match):
        self.match = match
        self.enabled = True
        self.cross_power = 9.0
        self.cross_height = 2.0

    def is_wide_position(self, player):
        field = self.match.field

        return (
            player.y < field.top + 105
            or
            player.y > field.bottom - 105
        )

    def cross(self, player, target_x, target_y):
        if not self.enabled:
            return False

        if player is None:
            return False

        if getattr(self.match, "ball_owner", None) is not player:
            return False

        if not self.is_wide_position(player):
            return False

        dx = target_x - player.x
        dy = target_y - player.y

        distance = math.sqrt(dx * dx + dy * dy)

        if distance <= 0:
            return False

        dx /= distance
        dy /= distance

        self.match.ball_owner = None
        self.match.ball_x = player.x
        self.match.ball_y = player.y

        self.match.ball_vx = dx * self.cross_power
        self.match.ball_vy = dy * self.cross_power

        return True

    def update(self):
        pass

    def reset(self):
        pass
