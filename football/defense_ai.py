import math


class DefenseAI:

    def __init__(self, match):

        self.match = match
        self.enabled = True

        self.mark_distance = 75.0
        self.press_distance = 120.0
        self.press_speed = 2.8
        self.recovery_speed = 2.4

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

    def get_opponents(self, team):

        return (
            self.match.away_players
            if team == "blue"
            else self.match.home_players
        )

    # ==================================================
    # PORTEUR
    # ==================================================

    def press_ball_carrier(
        self,
        defender,
        owner
    ):

        if owner is None:
            return

        dx = owner.x - defender.x
        dy = owner.y - defender.y

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        if distance <= 0:
            return

        dx /= distance
        dy /= distance

        defender.x += (
            dx *
            self.press_speed
        )

        defender.y += (
            dy *
            self.press_speed
        )

        defender.direction_x = dx
        defender.direction_y = dy

    # ==================================================
    # MARQUAGE
    # ==================================================

    def mark_player(
        self,
        defender,
        attacker
    ):

        if attacker is None:
            return

        dx = attacker.x - defender.x
        dy = attacker.y - defender.y

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        if distance <= self.mark_distance:
            return

        if distance <= 0:
            return

        dx /= distance
        dy /= distance

        defender.x += (
            dx *
            self.recovery_speed
        )

        defender.y += (
            dy *
            self.recovery_speed
        )

    # ==================================================
    # REPLI
    # ==================================================

    def recover(self, player):

        field = self.match.field

        if player.team == "blue":

            target_x = (
                field.left +
                field.width * 0.30
            )

        else:

            target_x = (
                field.right -
                field.width * 0.30
            )

        dx = target_x - player.x

        player.x += (
            dx * 0.025
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

        defending_team = (
            "red"
            if owner.team == "blue"
            else "blue"
        )

        defenders = self.get_players(
            defending_team
        )

        opponents = self.get_opponents(
            defending_team
        )

        for defender in defenders:

            if not getattr(
                defender,
                "on_pitch",
                True
            ):
                continue

            role = getattr(
                defender,
                "role",
                getattr(
                    defender,
                    "position",
                    "CM"
                )
            )

            if role == "GK":
                continue

            distance = self.distance(
                defender,
                owner
            )

            if distance < self.press_distance:

                self.press_ball_carrier(
                    defender,
                    owner
                )

            else:

                target = self.find_target(
                    defender,
                    opponents
                )

                self.mark_player(
                    defender,
                    target
                )

    # ==================================================
    # CIBLE DE MARQUAGE
    # ==================================================

    def find_target(
        self,
        defender,
        opponents
    ):

        if not opponents:
            return None

        return min(
            opponents,
            key=lambda p:
                self.distance(
                    defender,
                    p
                )
        )

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):
        pass
