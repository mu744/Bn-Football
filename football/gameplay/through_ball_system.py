import math


class ThroughBallSystem:
    def __init__(self, match):
        self.match = match
        self.enabled = True
        self.power = 10.5
        self.max_distance = 420.0

    def pass_ball(self, player, target):
        if not self.enabled:
            return False

        if player is None or target is None:
            return False

        if getattr(self.match, "ball_owner", None) is not player:
            return False

        dx = target.x - player.x
        dy = target.y - player.y

        distance = math.sqrt(dx * dx + dy * dy)

        if distance <= 0:
            return False

        distance = min(distance, self.max_distance)

        dx /= math.sqrt(dx * dx + dy * dy)
        dy /= math.sqrt(dx * dx + dy * dy)

        self.match.ball_owner = None
        self.match.ball_vx = dx * self.power
        self.match.ball_vy = dy * self.power

        self.match.ball_x = player.x
        self.match.ball_y = player.y

        return True

    def find_target(self, player):
        teammates = (
            self.match.home_players
            if player.team == "blue"
            else self.match.away_players
        )

        best = None
        best_score = -999999

        direction = 1 if player.team == "blue" else -1

        for teammate in teammates:
            if teammate is player:
                continue

            if not getattr(teammate, "on_pitch", True):
                continue

            dx = teammate.x - player.x
            dy = teammate.y - player.y

            distance = math.sqrt(dx * dx + dy * dy)

            if distance < 60 or distance > self.max_distance:
                continue

            forward = dx * direction

            score = forward - abs(dy) * 0.35

            if score > best_score:
                best_score = score
                best = teammate

        return best

    def update(self):
        pass

    def reset(self):
        pass
