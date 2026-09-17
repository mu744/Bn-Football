import math


class InterceptionSystem:
    def __init__(self, match):
        self.match = match
        self.enabled = True
        self.interception_radius = 42.0

    def distance(self, player):
        return math.sqrt(
            (player.x - self.match.ball_x) ** 2 +
            (player.y - self.match.ball_y) ** 2
        )

    def can_intercept(self, player):
        if player is None:
            return False

        if self.match.ball_owner is not None:
            return False

        return self.distance(player) <= self.interception_radius

    def intercept(self, player):
        if not self.enabled:
            return False

        if not self.can_intercept(player):
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

        closest = None
        best_distance = self.interception_radius

        for player in players:
            if not getattr(player, "on_pitch", True):
                continue

            distance = self.distance(player)

            if distance < best_distance:
                best_distance = distance
                closest = player

        if closest is not None:
            self.intercept(closest)

    def reset(self):
        pass
