import math


class BallRecovery:
    def __init__(self, match):
        self.match = match
        self.enabled = True
        self.recovery_radius = 35.0

    def recover(self, player):
        if not self.enabled or player is None:
            return False

        if self.match.ball_owner is not None:
            return False

        distance = math.sqrt(
            (player.x - self.match.ball_x) ** 2 +
            (player.y - self.match.ball_y) ** 2
        )

        if distance > self.recovery_radius:
            return False

        self.match.ball_owner = player
        self.match.ball_vx = 0.0
        self.match.ball_vy = 0.0

        return True

    def update(self):
        if not self.enabled:
            return

        if self.match.ball_owner is not None:
            return

        players = (
            self.match.home_players +
            self.match.away_players
        )

        for player in players:
            if not getattr(player, "on_pitch", True):
                continue

            if self.recover(player):
                break

    def reset(self):
        pass
