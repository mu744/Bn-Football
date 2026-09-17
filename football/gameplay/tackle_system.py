import math
import random


class TackleSystem:

    def __init__(self, match):

        self.match = match

        # Distances
        self.tackle_distance = 42.0
        self.interception_distance = 32.0

        # Temps entre deux tacles
        self.cooldown = 0.0
        self.tackle_cooldown = 0.55

        # Puissance du dégagement après tacle
        self.clearance_speed = 7.0

    # ==================================================
    # OUTILS
    # ==================================================

    def distance(self, player, target):

        return math.sqrt(
            (player.x - target.x) ** 2 +
            (player.y - target.y) ** 2
        )

    def update(self, delta_time):

        if self.cooldown > 0:

            self.cooldown -= delta_time

            if self.cooldown < 0:
                self.cooldown = 0

    # ==================================================
    # TACLE
    # ==================================================

    def tackle(self, defender):

        if defender is None:
            return False

        if self.cooldown > 0:
            return False

        owner = self.match.ball_owner

        if owner is None:
            return False

        # Impossible de tacler un coéquipier
        if owner.team == defender.team:
            return False

        distance = self.distance(
            defender,
            owner
        )

        if distance > self.tackle_distance:
            return False

        # --------------------------------------------------
        # CHANCE DE RÉUSSITE
        # --------------------------------------------------

        chance = 0.72

        speed = defender.get_current_speed()

        if speed > 4.0:
            chance += 0.05

        # Plus on est loin, plus le tacle est difficile.
        chance -= max(
            0.0,
            (distance - 25.0) / 100.0
        )

        chance = max(
            0.20,
            min(0.90, chance)
        )

        self.cooldown = (
            self.tackle_cooldown
        )

        # --------------------------------------------------
        # RÉSULTAT
        # --------------------------------------------------

        if random.random() <= chance:

            self.match.ball_owner = defender

            self.match.ball_vx = 0.0
            self.match.ball_vy = 0.0

            (
                self.match.ball_x,
                self.match.ball_y
            ) = defender.ball_control.update_ball_position(
                self.match.ball_x,
                self.match.ball_y
            )

            return True

        # Tacle manqué
        return False

    # ==================================================
    # INTERCEPTION
    # ==================================================

    def intercept(self, defender):

        if defender is None:
            return False

        if self.match.ball_owner is not None:
            return False

        distance = math.sqrt(
            (defender.x - self.match.ball_x) ** 2 +
            (defender.y - self.match.ball_y) ** 2
        )

        if distance > self.interception_distance:
            return False

        chance = 0.68

        if random.random() > chance:
            return False

        self.match.ball_owner = defender

        self.match.ball_vx = 0.0
        self.match.ball_vy = 0.0

        (
            self.match.ball_x,
            self.match.ball_y
        ) = defender.ball_control.update_ball_position(
            self.match.ball_x,
            self.match.ball_y
        )

        return True

    # ==================================================
    # DÉGAGEMENT
    # ==================================================

    def clear_ball(self, player):

        if player is None:
            return False

        if self.match.ball_owner is not player:
            return False

        direction_x = player.direction_x
        direction_y = player.direction_y

        length = math.sqrt(
            direction_x ** 2 +
            direction_y ** 2
        )

        if length <= 0:
            direction_x = 1.0
            direction_y = 0.0
            length = 1.0

        direction_x /= length
        direction_y /= length

        self.match.ball_vx = (
            direction_x *
            self.clearance_speed
        )

        self.match.ball_vy = (
            direction_y *
            self.clearance_speed
        )

        self.match.ball_owner = None

        return True
