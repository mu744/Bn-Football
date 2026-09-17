import math
import random


class FirstTouchSystem:
    def __init__(self, match):
        self.match = match
        self.enabled = True
        self.max_control_distance = 48.0
        self.soft_touch = 0.72
        self.hard_touch = 1.35

    def distance_to_ball(self, player):
        return math.sqrt(
            (player.x - self.match.ball_x) ** 2 +
            (player.y - self.match.ball_y) ** 2
        )

    def control_quality(self, player):
        rating = getattr(player, "control_rating", 75)
        return max(0.35, min(1.0, rating / 100.0))

    def receive(self, player):
        if not self.enabled or player is None:
            return False

        distance = self.distance_to_ball(player)

        if distance > self.max_control_distance:
            return False

        quality = self.control_quality(player)

        if random.random() > quality:
            self.match.ball_owner = None
            return False

        self.match.ball_owner = player

        speed = math.sqrt(
            self.match.ball_vx ** 2 +
            self.match.ball_vy ** 2
        )

        damping = self.soft_touch

        if speed > 10:
            damping = self.hard_touch

        self.match.ball_vx *= max(0.05, 1.0 - damping)
        self.match.ball_vy *= max(0.05, 1.0 - damping)

        return True

    def update(self):
        if not self.enabled:
            return

        owner = getattr(self.match, "ball_owner", None)

        if owner is not None:
            return

        players = (
            self.match.home_players +
            self.match.away_players
        )

        closest = None
        closest_distance = self.max_control_distance

        for player in players:
            if not getattr(player, "on_pitch", True):
                continue

            distance = self.distance_to_ball(player)

            if distance < closest_distance:
                closest = player
                closest_distance = distance

        if closest is not None:
            self.receive(closest)

    def reset(self):
        pass
