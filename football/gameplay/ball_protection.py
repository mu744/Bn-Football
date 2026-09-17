import math


class BallProtection:
    """
    Gestion spécialisée de la protection du ballon.

    Sépare la notion de duel physique du système
    général de dribble.
    """

    def __init__(self, match):

        self.match = match
        self.enabled = True

        self.contact_distance = 38.0
        self.push_strength = 2.2

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

    # =========================================================
    # DUEL
    # =========================================================

    def duel(self, attacker, defender):

        if attacker is None:
            return False

        if defender is None:
            return False

        if self.distance(
            attacker,
            defender
        ) > self.contact_distance:

            return False

        attacker_rating = getattr(
            attacker,
            "physical",
            getattr(attacker, "rating", 70)
        )

        defender_rating = getattr(
            defender,
            "physical",
            getattr(defender, "rating", 70)
        )

        # Certains anciens joueurs ne possèdent
        # pas encore la statistique physique.
        attacker_rating = float(
            attacker_rating
        )

        defender_rating = float(
            defender_rating
        )

        total = (
            attacker_rating +
            defender_rating
        )

        if total <= 0:
            return False

        attacker_chance = (
            attacker_rating / total
        )

        import random

        if random.random() <= attacker_chance:

            # L'attaquant garde la balle.
            return True

        # Le défenseur récupère la balle.
        self.match.ball_owner = defender

        self.match.ball_x = defender.x
        self.match.ball_y = defender.y

        self.match.ball_vx = 0.0
        self.match.ball_vy = 0.0

        return False

    # =========================================================
    # UPDATE
    # =========================================================

    def update(self):

        if not self.enabled:
            return

        owner = getattr(
            self.match,
            "ball_owner",
            None
        )

        if owner is None:
            return

        opponents = (
            self.match.away_players
            if owner.team == "blue"
            else self.match.home_players
        )

        for opponent in opponents:

            if not getattr(
                opponent,
                "on_pitch",
                True
            ):
                continue

            if self.distance(
                owner,
                opponent
            ) <= self.contact_distance:

                self.duel(
                    owner,
                    opponent
                )

                break

    # =========================================================
    # CONTROLE
    # =========================================================

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def reset(self):
        self.enabled = True
