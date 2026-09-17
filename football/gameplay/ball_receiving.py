import math


class BallReceiving:
    def __init__(self, match):
        self.match = match
        self.enabled = True
        self.control_radius = 38.0
        self.follow_strength = 0.42

    def distance(self, player):
        return math.sqrt(
            (player.x - self.match.ball_x) ** 2 +
            (player.y - self.match.ball_y) ** 2
        )

    def can_receive(self, player):
        if player is None:
            return False

        return self.distance(player) <= self.control_radius

    def receive(self, player):
        if not self.enabled or not self.can_receive(player):
            return False

        self.match.ball_owner = player
        self.match.ball_vx = 0.0
        self.match.ball_vy = 0.0

        return True

    def update(self):
        owner = getattr(self.match, "ball_owner", None)

        if owner is None:
            return

        target = owner.ball_control.get_target_position()

        self.match.ball_x += (
            target[0] - self.match.ball_x
        ) * self.follow_strength

        self.match.ball_y += (
            target[1] - self.match.ball_y
        ) * self.follow_strength

    def reset(self):
        pass
