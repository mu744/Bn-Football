import math
import random


class ShootSystem:

    def __init__(self, match):

        self.match = match

        self.min_power = 8.0
        self.normal_power = 12.0
        self.max_power = 17.0

        self.min_distance = 35.0

        self.goal_half_width = 70.0

    # ==================================================
    # DISTANCE BUT
    # ==================================================

    def distance_to_goal(self, player):

        goal_x = self.match.field.right
        goal_y = self.match.field.centery

        return math.sqrt(
            (goal_x - player.x) ** 2 +
            (goal_y - player.y) ** 2
        )

    # ==================================================
    # DIRECTION
    # ==================================================

    def get_direction(
        self,
        player,
        target_y=None
    ):

        goal_x = self.match.field.right

        if target_y is None:
            target_y = self.match.field.centery

        dx = goal_x - player.x
        dy = target_y - player.y

        length = math.sqrt(
            dx * dx +
            dy * dy
        )

        if length <= 0:
            return 0.0, 0.0

        return (
            dx / length,
            dy / length
        )

    # ==================================================
    # PRÉCISION
    # ==================================================

    def calculate_accuracy(self, player):

        rating = getattr(
            player,
            "rating",
            75
        )

        accuracy = (
            0.70 +
            rating / 1000
        )

        return max(
            0.70,
            min(0.95, accuracy)
        )

    # ==================================================
    # TIR
    # ==================================================

    def shoot(
        self,
        player,
        power="normal",
        target_y=None,
        charge_power=None
    ):

        if player is None:
            return False

        if self.match.ball_owner is not player:
            return False

        distance = self.distance_to_goal(
            player
        )

        if distance < self.min_distance:
            return False

        # ------------------------------------------
        # PUISSANCE
        # ------------------------------------------

        if charge_power is not None:

            speed = self.match.power_system.shot_speed(
                charge_power
            )

        else:

            if power == "low":

                speed = self.min_power

            elif power == "strong":

                speed = self.max_power

            else:

                speed = self.normal_power

        # ------------------------------------------
        # DIRECTION
        # ------------------------------------------

        direction_x, direction_y = (
            self.get_direction(
                player,
                target_y
            )
        )

        if (
            direction_x == 0
            and direction_y == 0
        ):
            return False

        # ------------------------------------------
        # PRÉCISION
        # ------------------------------------------

        accuracy = self.calculate_accuracy(
            player
        )

        error = (
            1.0 - accuracy
        ) * 0.35

        direction_y += random.uniform(
            -error,
            error
        )

        length = math.sqrt(
            direction_x ** 2 +
            direction_y ** 2
        )

        if length > 0:

            direction_x /= length
            direction_y /= length

        # ------------------------------------------
        # TIR
        # ------------------------------------------

        self.match.ball_vx = (
            direction_x * speed
        )

        self.match.ball_vy = (
            direction_y * speed
        )

        self.match.ball_owner = None

        return True

    # ==================================================
    # TIR FAIBLE
    # ==================================================

    def low_shot(
        self,
        player,
        power=None
    ):

        return self.shoot(
            player,
            power="low",
            charge_power=power
        )

    # ==================================================
    # TIR NORMAL
    # ==================================================

    def normal_shot(
        self,
        player,
        power=None
    ):

        return self.shoot(
            player,
            power="normal",
            charge_power=power
        )

    # ==================================================
    # TIR PUISSANT
    # ==================================================

    def strong_shot(
        self,
        player,
        power=None
    ):

        return self.shoot(
            player,
            power="strong",
            charge_power=power
        )

    # ==================================================
    # TIR CIBLÉ
    # ==================================================

    def targeted_shot(
        self,
        player,
        target_y,
        power=None
    ):

        return self.shoot(
            player,
            target_y=target_y,
            charge_power=power
        )
