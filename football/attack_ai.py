import math


class AttackAI:

    def __init__(self, match):

        self.match = match
        self.enabled = True

        self.run_speed = 2.8
        self.support_distance = 150.0
        self.attack_distance = 250.0

    # ==================================================
    # OUTILS
    # ==================================================

    def distance(self, a, b):

        return math.sqrt(
            (a.x - b.x) ** 2 +
            (a.y - b.y) ** 2
        )

    def get_players(self, team):

        return (
            self.match.home_players
            if team == "blue"
            else self.match.away_players
        )

    # ==================================================
    # DIRECTION
    # ==================================================

    def direction(self, team):

        return 1 if team == "blue" else -1

    # ==================================================
    # APPEL
    # ==================================================

    def make_run(self, player):

        direction = self.direction(
            player.team
        )

        player.x += (
            direction *
            self.run_speed
        )

    # ==================================================
    # SOUTIEN
    # ==================================================

    def support_ball_carrier(
        self,
        player,
        owner
    ):

        if owner is None:
            return

        dx = owner.x - player.x
        dy = owner.y - player.y

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        if distance <= self.support_distance:
            return

        if distance <= 0:
            return

        dx /= distance
        dy /= distance

        player.x += dx * 1.8
        player.y += dy * 1.8

    # ==================================================
    # LARGEUR
    # ==================================================

    def create_width(self, player):

        role = getattr(
            player,
            "role",
            getattr(
                player,
                "position",
                "CM"
            )
        )

        if role not in (
            "LW",
            "RW",
            "LWB",
            "RWB"
        ):
            return

        field = self.match.field

        if role in ("LW", "LWB"):

            target_y = field.top + 70

        else:

            target_y = field.bottom - 70

        player.y += (
            target_y -
            player.y
        ) * 0.025

    # ==================================================
    # ATTACK PROFONDEUR
    # ==================================================

    def attack_depth(self, player):

        role = getattr(
            player,
            "role",
            "CM"
        )

        if role not in (
            "ST",
            "CF",
            "LW",
            "RW"
        ):
            return

        direction = self.direction(
            player.team
        )

        player.x += (
            direction *
            1.2
        )

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        if not self.enabled:
            return

        owner = self.match.ball_owner

        if owner is None:
            return

        team = owner.team

        for player in self.get_players(
            team
        ):

            if player is owner:
                continue

            if not getattr(
                player,
                "on_pitch",
                True
            ):
                continue

            self.support_ball_carrier(
                player,
                owner
            )

            self.create_width(
                player
            )

            self.attack_depth(
                player
            )

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):
        pass
