import math


class MarkingSystem:

    def __init__(self, match):

        self.match = match

        self.enabled = True

        self.marking_distance = 85.0
        self.defensive_gap = 45.0

        self.assignments = {
            "blue": {},
            "red": {}
        }

    # ==================================================
    # OUTILS
    # ==================================================

    def distance(self, a, b):

        return math.sqrt(
            (a.x - b.x) ** 2 +
            (a.y - b.y) ** 2
        )

    def get_players(self, team):

        if team == "blue":
            return self.match.home_players

        return self.match.away_players

    def get_opponents(self, team):

        if team == "blue":
            return self.match.away_players

        return self.match.home_players

    # ==================================================
    # PRIORITÉ OFFENSIVE
    # ==================================================

    def opponent_priority(
        self,
        player
    ):

        role = getattr(
            player,
            "role",
            getattr(
                player,
                "position",
                "CM"
            )
        )

        priority = 1.0

        if role in (
            "ST",
            "CF"
        ):
            priority += 1.00

        elif role in (
            "LW",
            "RW"
        ):
            priority += 0.80

        elif role == "AM":
            priority += 0.75

        elif role == "CM":
            priority += 0.45

        elif role == "DM":
            priority += 0.35

        return priority

    # ==================================================
    # ASSIGNATIONS
    # ==================================================

    def assign_markers(self, team):

        defenders = [
            player
            for player in self.get_players(team)
            if getattr(
                player,
                "on_pitch",
                True
            )
            and getattr(
                player,
                "role",
                getattr(
                    player,
                    "position",
                    "CM"
                )
            ) != "GK"
        ]

        opponents = [
            player
            for player in self.get_opponents(team)
            if getattr(
                player,
                "on_pitch",
                True
            )
            and getattr(
                player,
                "role",
                getattr(
                    player,
                    "position",
                    "CM"
                )
            ) != "GK"
        ]

        opponents.sort(
            key=self.opponent_priority,
            reverse=True
        )

        assignments = {}

        used_defenders = set()

        for opponent in opponents:

            best_defender = None
            best_score = float("-inf")

            for defender in defenders:

                if id(defender) in used_defenders:
                    continue

                distance = self.distance(
                    defender,
                    opponent
                )

                score = (
                    self.opponent_priority(
                        opponent
                    ) * 100
                    -
                    distance
                )

                defender_role = getattr(
                    defender,
                    "role",
                    "CM"
                )

                if defender_role in (
                    "CB",
                    "DM"
                ):
                    score += 25

                if score > best_score:

                    best_score = score
                    best_defender = defender

            if best_defender is not None:

                assignments[
                    id(best_defender)
                ] = opponent

                used_defenders.add(
                    id(best_defender)
                )

        self.assignments[team] = assignments

        return assignments

    # ==================================================
    # POSITION DE MARQUAGE
    # ==================================================

    def calculate_marking_position(
        self,
        defender,
        attacker
    ):

        if attacker is None:
            return defender.x, defender.y

        # Le défenseur se place entre
        # l'attaquant et son propre but.
        field = self.match.field

        if defender.team == "blue":
            goal_x = field.left
        else:
            goal_x = field.right

        dx = goal_x - attacker.x
        dy = field.centery - attacker.y

        length = math.sqrt(
            dx * dx +
            dy * dy
        )

        if length <= 0:
            return attacker.x, attacker.y

        dx /= length
        dy /= length

        target_x = (
            attacker.x +
            dx *
            self.defensive_gap
        )

        target_y = (
            attacker.y +
            dy *
            self.defensive_gap
        )

        return target_x, target_y

    # ==================================================
    # DÉPLACEMENT
    # ==================================================

    def update_marker(
        self,
        defender,
        attacker
    ):

        if attacker is None:
            return

        target_x, target_y = (
            self.calculate_marking_position(
                defender,
                attacker
            )
        )

        dx = target_x - defender.x
        dy = target_y - defender.y

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        if distance <= 2:
            return

        speed = min(
            2.8,
            distance * 0.08
        )

        defender.x += (
            dx / distance
        ) * speed

        defender.y += (
            dy / distance
        ) * speed

        defender.direction_x = (
            dx / distance
        )

        defender.direction_y = (
            dy / distance
        )

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        if not self.enabled:
            return

        for team in (
            "blue",
            "red"
        ):

            assignments = (
                self.assign_markers(
                    team
                )
            )

            for defender_id, attacker in (
                assignments.items()
            ):

                defender = None

                for player in self.get_players(
                    team
                ):

                    if id(player) == defender_id:
                        defender = player
                        break

                if defender is not None:

                    self.update_marker(
                        defender,
                        attacker
                    )

    # ==================================================
    # ÉTAT
    # ==================================================

    def get_assignment(
        self,
        defender
    ):

        team = defender.team

        return self.assignments.get(
            team,
            {}
        ).get(
            id(defender)
        )

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        self.assignments = {
            "blue": {},
            "red": {}
        }
