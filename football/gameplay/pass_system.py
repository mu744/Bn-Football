
import math


class PassSystem:

    def __init__(self, match):

        self.match = match

        self.short_pass_speed = 6.0
        self.normal_pass_speed = 9.0
        self.long_pass_speed = 13.0

        self.min_distance = 25.0
        self.max_distance = 420.0

    # ==================================================
    # DISTANCE
    # ==================================================

    def distance(self, player_a, player_b):

        return math.sqrt(
            (player_a.x - player_b.x) ** 2 +
            (player_a.y - player_b.y) ** 2
        )

    # ==================================================
    # COÉQUIPIERS
    # ==================================================

    def get_teammates(self, player):

        if player.team == "blue":
            players = self.match.home_players
        else:
            players = self.match.away_players

        return [
            p for p in players
            if p is not player
        ]

    # ==================================================
    # RECHERCHE DE CIBLE
    # ==================================================

    def find_target(
        self,
        player,
        direction_x=None,
        direction_y=None,
        pass_type="normal"
    ):

        teammates = self.get_teammates(player)

        if not teammates:
            return None

        best_player = None
        best_score = -999999

        if direction_x is not None and direction_y is not None:

            length = math.sqrt(
                direction_x ** 2 +
                direction_y ** 2
            )

            if length > 0:
                direction_x /= length
                direction_y /= length

        for teammate in teammates:

            dx = teammate.x - player.x
            dy = teammate.y - player.y

            distance = math.sqrt(
                dx * dx +
                dy * dy
            )

            if distance < self.min_distance:
                continue

            if distance > self.max_distance:
                continue

            score = 0.0

            # Distance idéale
            if pass_type == "short":

                score -= abs(
                    distance - 90
                )

            elif pass_type == "long":

                score -= abs(
                    distance - 240
                ) * 0.45

            else:

                score -= abs(
                    distance - 150
                ) * 0.65

            # Direction
            if (
                direction_x is not None
                and direction_y is not None
            ):

                target_length = math.sqrt(
                    dx * dx +
                    dy * dy
                )

                if target_length > 0:

                    target_dx = dx / target_length
                    target_dy = dy / target_length

                    dot = (
                        target_dx * direction_x +
                        target_dy * direction_y
                    )

                    if dot < -0.25:
                        continue

                    score += dot * 220

            # Progression vers le but
            if player.team == "blue":

                if teammate.x > player.x:
                    score += 55

            else:

                if teammate.x < player.x:
                    score += 55

            # Espace autour du coéquipier
            opponents = (
                self.match.away_players
                if player.team == "blue"
                else self.match.home_players
            )

            nearest_opponent = 9999

            for opponent in opponents:

                opponent_distance = math.sqrt(
                    (teammate.x - opponent.x) ** 2 +
                    (teammate.y - opponent.y) ** 2
                )

                if opponent_distance < nearest_opponent:
                    nearest_opponent = opponent_distance

            score += min(
                nearest_opponent,
                100
            ) * 0.8

            if score > best_score:

                best_score = score
                best_player = teammate

        return best_player

    # ==================================================
    # PASSE AVEC PUISSANCE
    # ==================================================

    def execute_pass(
        self,
        player,
        direction_x=None,
        direction_y=None,
        pass_type="normal",
        power=None
    ):

        if player is None:
            return False

        if self.match.ball_owner is not player:
            return False

        target = self.find_target(
            player,
            direction_x,
            direction_y,
            pass_type
        )

        if target is None:
            return False

        dx = target.x - player.x
        dy = target.y - player.y

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        if distance <= 0:
            return False

        # ------------------------------------------
        # PUISSANCE
        # ------------------------------------------

        if power is not None:

            speed = self.match.power_system.pass_speed(
                power
            )

        else:

            if pass_type == "short":
                speed = self.short_pass_speed

            elif pass_type == "long":
                speed = self.long_pass_speed

            else:
                speed = self.normal_pass_speed

        # ------------------------------------------
        # LANCEMENT
        # ------------------------------------------

        self.match.ball_vx = (
            dx / distance
        ) * speed

        self.match.ball_vy = (
            dy / distance
        ) * speed

        self.match.ball_owner = None

        return True

    # ==================================================
    # PASSE COURTE
    # ==================================================

    def short_pass(
        self,
        player,
        power=None
    ):

        return self.execute_pass(
            player,
            pass_type="short",
            power=power
        )

    # ==================================================
    # PASSE NORMALE
    # ==================================================

    def normal_pass(
        self,
        player,
        power=None
    ):

        return self.execute_pass(
            player,
            pass_type="normal",
            power=power
        )

    # ==================================================
    # PASSE LONGUE
    # ==================================================

    def long_pass(
        self,
        player,
        power=None
    ):

        return self.execute_pass(
            player,
            pass_type="long",
            power=power
        )

    # ==================================================
    # PASSE DIRECTIONNELLE
    # ==================================================

    def directional_pass(
        self,
        player,
        direction_x,
        direction_y,
        power=None
    ):

        return self.execute_pass(
            player,
            direction_x,
            direction_y,
            "normal",
            power
        )
