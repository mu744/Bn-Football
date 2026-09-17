import math


class PressingSystem:

    def __init__(self, match):

        self.match = match

        self.enabled = True

        self.press_distance = 145.0
        self.press_speed = 3.5

        self.max_pressers = 3

        self.pressers = {
            "blue": [],
            "red": []
        }

    # ==================================================
    # DISTANCE
    # ==================================================

    def distance(self, a, b):

        return math.sqrt(
            (a.x - b.x) ** 2 +
            (a.y - b.y) ** 2
        )

    # ==================================================
    # JOUEURS
    # ==================================================

    def get_players(self, team):

        if team == "blue":
            return self.match.home_players

        return self.match.away_players

    def get_opponents(self, team):

        if team == "blue":
            return self.match.away_players

        return self.match.home_players

    # ==================================================
    # PORTEUR
    # ==================================================

    def get_ball_owner(self):

        return self.match.ball_owner

    # ==================================================
    # CHOIX DES PRESSEURS
    # ==================================================

    def choose_pressers(self, team):

        owner = self.get_ball_owner()

        if owner is None:
            self.pressers[team] = []
            return []

        if owner.team == team:
            self.pressers[team] = []
            return []

        players = self.get_players(team)

        candidates = []

        for player in players:

            if not getattr(
                player,
                "on_pitch",
                True
            ):
                continue

            distance = self.distance(
                player,
                owner
            )

            if distance > self.press_distance:
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

            priority = (
                self.press_priority(
                    player,
                    role
                )
            )

            candidates.append(
                (
                    priority,
                    distance,
                    player
                )
            )

        candidates.sort(
            key=lambda item: (
                -item[0],
                item[1]
            )
        )

        selected = [
            item[2]
            for item in candidates[
                :self.max_pressers
            ]
        ]

        self.pressers[team] = selected

        return selected

    # ==================================================
    # PRIORITÉ
    # ==================================================

    def press_priority(
        self,
        player,
        role
    ):

        priority = 1.0

        if role in (
            "ST",
            "CF",
            "LW",
            "RW"
        ):
            priority += 0.35

        elif role in (
            "AM",
            "CM"
        ):
            priority += 0.25

        elif role in (
            "DM",
        ):
            priority += 0.40

        elif role in (
            "CB",
        ):
            priority -= 0.20

        return priority

    # ==================================================
    # DÉPLACEMENT
    # ==================================================

    def move_to_ball_carrier(
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

        if distance <= 1:
            return

        dx /= distance
        dy /= distance

        player.x += (
            dx *
            self.press_speed
        )

        player.y += (
            dy *
            self.press_speed
        )

        player.direction_x = dx
        player.direction_y = dy

    # ==================================================
    # COUVERTURE
    # ==================================================

    def cover_pressing_lane(
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

        if distance <= 0:
            return

        # Le joueur se place légèrement
        # derrière le premier presseur.
        dx /= distance
        dy /= distance

        target_x = (
            owner.x -
            dx * 70
        )

        target_y = (
            owner.y -
            dy * 70
        )

        player.x += (
            target_x -
            player.x
        ) * 0.025

        player.y += (
            target_y -
            player.y
        ) * 0.025

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        if not self.enabled:
            return

        owner = self.get_ball_owner()

        if owner is None:
            return

        defending_team = (
            "red"
            if owner.team == "blue"
            else "blue"
        )

        pressers = self.choose_pressers(
            defending_team
        )

        for index, player in enumerate(
            pressers
        ):

            if index == 0:

                self.move_to_ball_carrier(
                    player,
                    owner
                )

            else:

                self.cover_pressing_lane(
                    player,
                    owner
                )

    # ==================================================
    # ÉTAT
    # ==================================================

    def get_pressers(self, team):

        return list(
            self.pressers.get(
                team,
                []
            )
        )

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        self.pressers = {
            "blue": [],
            "red": []
        }
