import math


class DribbleSystem:
    """
    Système central de conduite et de dribble.

    Gère :
    - conduite de balle
    - changement de direction
    - accélération avec ballon
    - protection de balle
    - contrôle à vitesse élevée
    - perte de balle lors d'un mauvais contrôle
    """

    def __init__(self, match):

        self.match = match
        self.enabled = True

        self.base_control_distance = 20.0
        self.max_control_distance = 42.0

        self.follow_strength = 0.38

        self.normal_speed_factor = 1.0
        self.sprint_speed_factor = 0.82

        self.protection_distance = 32.0
        self.protection_strength = 0.55

        self.direction_change_limit = 0.72

        self.last_direction_x = 1.0
        self.last_direction_y = 0.0

    # =========================================================
    # OUTILS
    # =========================================================

    def distance(self, a, b):

        dx = a.x - b.x
        dy = a.y - b.y

        return math.sqrt(
            dx * dx +
            dy * dy
        )

    def normalize(self, x, y):

        length = math.sqrt(
            x * x +
            y * y
        )

        if length <= 0:
            return 0.0, 0.0

        return (
            x / length,
            y / length
        )

    # =========================================================
    # JOUEUR POSSEDANT LA BALLE
    # =========================================================

    def get_owner(self):

        return getattr(
            self.match,
            "ball_owner",
            None
        )

    # =========================================================
    # DISTANCE DE CONDUITE
    # =========================================================

    def get_control_distance(
        self,
        player,
        sprint=False
    ):

        speed = player.get_current_speed()

        distance = (
            self.base_control_distance +
            min(speed * 2.0, 20.0)
        )

        if sprint:
            distance += 4.0

        return min(
            distance,
            self.max_control_distance
        )

    # =========================================================
    # POSITION CIBLE DE LA BALLE
    # =========================================================

    def get_ball_target(
        self,
        player,
        sprint=False
    ):

        direction_x = player.direction_x
        direction_y = player.direction_y

        direction_x, direction_y = self.normalize(
            direction_x,
            direction_y
        )

        distance = self.get_control_distance(
            player,
            sprint
        )

        return (
            player.x + direction_x * distance,
            player.y + direction_y * distance
        )

    # =========================================================
    # CONDUITE DE BALLE
    # =========================================================

    def carry_ball(
        self,
        player,
        sprint=False
    ):

        if not self.enabled:
            return False

        if player is None:
            return False

        if self.match.ball_owner is not player:
            return False

        target_x, target_y = self.get_ball_target(
            player,
            sprint
        )

        self.match.ball_x += (
            target_x -
            self.match.ball_x
        ) * self.follow_strength

        self.match.ball_y += (
            target_y -
            self.match.ball_y
        ) * self.follow_strength

        self.match.ball_vx = 0.0
        self.match.ball_vy = 0.0

        return True

    # =========================================================
    # CHANGEMENT DE DIRECTION
    # =========================================================

    def direction_change_quality(
        self,
        player
    ):

        current_x = player.direction_x
        current_y = player.direction_y

        current_x, current_y = self.normalize(
            current_x,
            current_y
        )

        dot = (
            current_x * self.last_direction_x +
            current_y * self.last_direction_y
        )

        dot = max(
            -1.0,
            min(1.0, dot)
        )

        return (dot + 1.0) * 0.5

    def update_direction_memory(
        self,
        player
    ):

        dx, dy = self.normalize(
            player.direction_x,
            player.direction_y
        )

        if dx == 0 and dy == 0:
            return

        self.last_direction_x = dx
        self.last_direction_y = dy

    # =========================================================
    # PROTECTION DE BALLE
    # =========================================================

    def find_nearest_opponent(
        self,
        player
    ):

        opponents = (
            self.match.away_players
            if player.team == "blue"
            else self.match.home_players
        )

        closest = None
        best_distance = float("inf")

        for opponent in opponents:

            if not getattr(
                opponent,
                "on_pitch",
                True
            ):
                continue

            distance = self.distance(
                player,
                opponent
            )

            if distance < best_distance:

                best_distance = distance
                closest = opponent

        return closest, best_distance

    def protect_ball(
        self,
        player
    ):

        if not self.enabled:
            return False

        if self.match.ball_owner is not player:
            return False

        opponent, distance = (
            self.find_nearest_opponent(
                player
            )
        )

        if opponent is None:
            return False

        if distance > self.protection_distance:
            return False

        # Oriente le joueur entre l'adversaire
        # et la direction opposée à la balle.
        dx = opponent.x - player.x
        dy = opponent.y - player.y

        dx, dy = self.normalize(
            dx,
            dy
        )

        player.x -= (
            dx *
            self.protection_strength
        )

        player.y -= (
            dy *
            self.protection_strength
        )

        return True

    # =========================================================
    # QUALITE DU DRIBBLE
    # =========================================================

    def get_dribble_quality(
        self,
        player
    ):

        rating = getattr(
            player,
            "rating",
            75
        )

        control = getattr(
            player,
            "control_rating",
            rating
        )

        speed = player.get_current_speed()

        quality = (
            rating * 0.35 +
            control * 0.50 +
            max(0.0, 100.0 - speed * 8.0) * 0.15
        )

        return max(
            0.0,
            min(100.0, quality)
        )

    # =========================================================
    # RISQUE DE PERTE
    # =========================================================

    def should_lose_ball(
        self,
        player,
        sprint=False
    ):

        quality = self.get_dribble_quality(
            player
        )

        direction_quality = (
            self.direction_change_quality(
                player
            )
        )

        risk = 0.02

        if sprint:
            risk += 0.025

        if direction_quality < self.direction_change_limit:
            risk += 0.06

        if quality < 60:
            risk += 0.06

        elif quality < 75:
            risk += 0.025

        # Plus le risque est élevé, plus une
        # petite valeur aléatoire peut provoquer
        # un mauvais contrôle.
        import random

        return random.random() < risk

    # =========================================================
    # UPDATE
    # =========================================================

    def update(
        self,
        delta_time=0.016,
        sprint=False
    ):

        if not self.enabled:
            return

        player = self.get_owner()

        if player is None:
            return

        if not getattr(
            player,
            "on_pitch",
            True
        ):
            return

        self.carry_ball(
            player,
            sprint
        )

        self.protect_ball(
            player
        )

        if self.should_lose_ball(
            player,
            sprint
        ):

            self.match.ball_owner = None

            # Petite poussée naturelle de la balle.
            dx = player.direction_x
            dy = player.direction_y

            self.match.ball_vx = dx * 2.0
            self.match.ball_vy = dy * 2.0

        self.update_direction_memory(
            player
        )

    # =========================================================
    # CONTROLE
    # =========================================================

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def reset(self):

        self.enabled = True

        self.last_direction_x = 1.0
        self.last_direction_y = 0.0
