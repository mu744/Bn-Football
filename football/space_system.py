import math


class SpaceSystem:

    def __init__(self, match):

        self.match = match

        self.enabled = True

        self.space_radius = 70.0
        self.danger_radius = 45.0

        self.spaces = {
            "blue": [],
            "red": []
        }

    # ==================================================
    # OUTILS
    # ==================================================

    def distance_to_point(
        self,
        player,
        x,
        y
    ):

        return math.sqrt(
            (player.x - x) ** 2 +
            (player.y - y) ** 2
        )

    def get_players(self, team):

        if team == "blue":
            return self.match.home_players

        return self.match.away_players

    # ==================================================
    # CALCUL DES ZONES
    # ==================================================

    def calculate_spaces(self, team):

        field = self.match.field

        points = []

        columns = 6
        rows = 4

        for column in range(
            columns
        ):

            for row in range(
                rows
            ):

                x = (
                    field.left
                    +
                    field.width *
                    (
                        (column + 0.5)
                        / columns
                    )
                )

                y = (
                    field.top
                    +
                    field.height *
                    (
                        (row + 0.5)
                        / rows
                    )
                )

                pressure = (
                    self.calculate_pressure(
                        team,
                        x,
                        y
                    )
                )

                value = (
                    1.0 -
                    min(
                        pressure,
                        1.0
                    )
                )

                points.append({
                    "x": x,
                    "y": y,
                    "pressure": pressure,
                    "value": value
                })

        self.spaces[team] = points

        return points

    # ==================================================
    # PRESSION DANS UNE ZONE
    # ==================================================

    def calculate_pressure(
        self,
        team,
        x,
        y
    ):

        opponents = (
            self.match.away_players
            if team == "blue"
            else self.match.home_players
        )

        pressure = 0.0

        for opponent in opponents:

            if not getattr(
                opponent,
                "on_pitch",
                True
            ):
                continue

            distance = self.distance_to_point(
                opponent,
                x,
                y
            )

            if distance < self.space_radius:

                contribution = (
                    1.0 -
                    distance /
                    self.space_radius
                )

                pressure += contribution

        return min(
            pressure,
            1.0
        )

    # ==================================================
    # MEILLEURE ZONE
    # ==================================================

    def get_best_space(self, team):

        spaces = self.calculate_spaces(
            team
        )

        if not spaces:
            return None

        return max(
            spaces,
            key=lambda space:
                space["value"]
        )

    # ==================================================
    # ESPACE AUTOUR DU BALLON
    # ==================================================

    def get_ball_space(self, team):

        return {
            "x": self.match.ball_x,
            "y": self.match.ball_y,
            "pressure": self.calculate_pressure(
                team,
                self.match.ball_x,
                self.match.ball_y
            )
        }

    # ==================================================
    # JOUEUR LE PLUS PROCHE
    # ==================================================

    def nearest_teammate(
        self,
        player
    ):

        teammates = [
            p
            for p in self.get_players(
                player.team
            )
            if p is not player
            and getattr(
                p,
                "on_pitch",
                True
            )
        ]

        if not teammates:
            return None

        return min(
            teammates,
            key=lambda p:
                self.distance_to_point(
                    p,
                    player.x,
                    player.y
                )
        )

    # ==================================================
    # ESPACE LIBRE POUR UN JOUEUR
    # ==================================================

    def find_space_for_player(
        self,
        player
    ):

        spaces = self.calculate_spaces(
            player.team
        )

        if not spaces:
            return None

        role = getattr(
            player,
            "role",
            getattr(
                player,
                "position",
                "CM"
            )
        )

        best = None
        best_score = float("-inf")

        for space in spaces:

            score = space["value"]

            # Les ailiers recherchent la largeur.
            if role in (
                "LW",
                "RW",
                "LWB",
                "RWB"
            ):

                side_bonus = (
                    abs(
                        space["y"]
                        -
                        self.match.field.centery
                    )
                    /
                    max(
                        1,
                        self.match.field.height
                    )
                )

                score += side_bonus

            # Les attaquants recherchent
            # les zones avancées.
            if role in (
                "ST",
                "CF",
                "AM"
            ):

                if player.team == "blue":

                    score += (
                        space["x"]
                        /
                        self.match.field.right
                    )

                else:

                    score += (
                        1.0 -
                        space["x"]
                        /
                        self.match.field.right
                    )

            if score > best_score:

                best_score = score
                best = space

        return best

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        if not self.enabled:
            return

        self.calculate_spaces(
            "blue"
        )

        self.calculate_spaces(
            "red"
        )

    # ==================================================
    # ACTIVATION
    # ==================================================

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        self.spaces = {
            "blue": [],
            "red": []
        }
