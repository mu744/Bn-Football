import math


class ClearanceSystem:
    def __init__(self, match):
        self.match = match
        self.enabled = True
        self.clearance_power = 12.0
        self.clearance_distance = 55.0

    def clearance(self, player):
        if not self.enabled or player is None:
            return False

        if self.match.ball_owner is not player:
            return False

        direction = 1 if player.team == "blue" else -1

        self.match.ball_owner = None
        self.match.ball_x = player.x
        self.match.ball_y = player.y
        self.match.ball_vx = direction * self.clearance_power
        self.match.ball_vy = 0.0

        return True

    def update(self):
        pass

    def reset(self):
        pass
