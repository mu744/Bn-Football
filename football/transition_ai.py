import math


class TransitionAI:

    def __init__(self, match):

        self.match = match
        self.enabled = True

        self.counter_speed = 3.4
        self.recovery_speed = 3.0

        self.active_team = None
        self.timer = 0.0
        self.duration = 2.0

    # ==================================================
    # DIRECTION
    # ==================================================

    def direction(self, team):

        return 1 if team == "blue" else -1

    # ==================================================
    # JOUEURS
    # ==================================================

    def get_players(self, team):

        return (
            self.match.home_players
            if team == "blue"
            else self.match.away_players
        )

    # ==================================================
    # CONTRE-ATTAQUE
    # ==================================================

    def counter_attack(self, team):

        direction = self.direction(
            team
        )

        for player in self.get_players(
            team
        ):

            if not getattr(
                player,
                "on_pitch",
                True
            ):
                continue

            role = getattr(
                player,
                "role",
                getattr(
                    player,
                    "position",
                    "CM"
                )
            )

            if role in (
                "ST",
                "CF",
                "LW",
                "RW"
            ):

                player.x += (
                    direction *
                    self.counter_speed
                )

    # ==================================================
    # REPLI
    # ==================================================

    def recover_team(self, team):

        field = self.match.field

        if team == "blue":

            target_x = (
                field.left +
                field.width * 0.30
            )

        else:

            target_x = (
                field.right -
                field.width * 0.30
            )

        for player in self.get_players(
            team
        ):

            if not getattr(
                player,
                "on_pitch",
                True
            ):
                continue

            if getattr(
                player,
                "role",
                getattr(
                    player,
                    "position",
                    "CM"
                )
            ) == "GK":
                continue

            dx = target_x - player.x

            player.x += (
                dx * 0.025
            )

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self, delta_time):

        if not self.enabled:
            return

        owner = self.match.ball_owner

        if owner is None:
            return

        current_team = owner.team

        if (
            self.active_team is not None
            and current_team != self.active_team
        ):

            self.timer = self.duration

        self.active_team = current_team

        if self.timer > 0:

            self.counter_attack(
                current_team
            )

            defending_team = (
                "red"
                if current_team == "blue"
                else "blue"
            )

            self.recover_team(
                defending_team
            )

            self.timer -= delta_time

            if self.timer < 0:
                self.timer = 0

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        self.active_team = None
        self.timer = 0.0
