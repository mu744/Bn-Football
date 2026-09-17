import math
import random


class DecisionSystem:

    def __init__(self, match):

        self.match = match
        self.enabled = True

        self.decision_interval = 0.35
        self.timers = {}

    # ==================================================
    # OUTILS
    # ==================================================

    def distance(self, a, b):

        return math.sqrt(
            (a.x - b.x) ** 2 +
            (a.y - b.y) ** 2
        )

    def get_teammates(self, player):

        players = (
            self.match.home_players
            if player.team == "blue"
            else self.match.away_players
        )

        return [
            p for p in players
            if p is not player
            and getattr(p, "on_pitch", True)
        ]

    def get_opponents(self, player):

        players = (
            self.match.away_players
            if player.team == "blue"
            else self.match.home_players
        )

        return [
            p for p in players
            if getattr(p, "on_pitch", True)
        ]

    # ==================================================
    # TEMPS DE DÉCISION
    # ==================================================

    def ready(self, player, delta_time):

        key = id(player)

        timer = self.timers.get(key, 0.0)
        timer -= delta_time

        if timer > 0:

            self.timers[key] = timer
            return False

        self.timers[key] = (
            self.decision_interval
            + random.uniform(0.0, 0.20)
        )

        return True

    # ==================================================
    # JOUEUR LE PLUS PROCHE
    # ==================================================

    def nearest_opponent(self, player):

        opponents = self.get_opponents(player)

        if not opponents:
            return None

        return min(
            opponents,
            key=lambda p: self.distance(
                player,
                p
            )
        )

    # ==================================================
    # ÉVALUATION DE LA SITUATION
    # ==================================================

    def evaluate(self, player):

        owner = self.match.ball_owner

        if owner is None:

            return "loose_ball"

        if owner.team == player.team:

            if owner is player:
                return "possession"

            return "support"

        return "defend"

    # ==================================================
    # CHOIX D'ACTION
    # ==================================================

    def choose_action(self, player):

        situation = self.evaluate(player)

        if situation == "possession":

            return self.choose_ball_action(
                player
            )

        if situation == "support":

            return self.choose_support_action(
                player
            )

        if situation == "defend":

            return self.choose_defensive_action(
                player
            )

        return "recover"

    def choose_ball_action(self, player):

        field = self.match.field

        if player.team == "blue":

            goal_x = field.right

        else:

            goal_x = field.left

        distance_to_goal = abs(
            goal_x - player.x
        )

        # Tir si le joueur est avancé.
        if distance_to_goal < 230:

            if random.random() < 0.35:

                return "shoot"

        # Passe la plupart du temps.
        if random.random() < 0.55:

            return "pass"

        return "dribble"

    def choose_support_action(self, player):

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

            return "run"

        if role in (
            "DM",
            "CB"
        ):

            return "cover"

        return "support"

    def choose_defensive_action(self, player):

        opponent = self.nearest_opponent(
            player
        )

        if opponent is None:
            return "reposition"

        distance = self.distance(
            player,
            opponent
        )

        if distance < 35:

            return "tackle"

        if distance < 100:

            return "press"

        return "mark"

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self, delta_time):

        if not self.enabled:
            return

        players = (
            self.match.home_players
            +
            self.match.away_players
        )

        for player in players:

            if not getattr(
                player,
                "on_pitch",
                True
            ):
                continue

            if not self.ready(
                player,
                delta_time
            ):
                continue

            player.ai_action = (
                self.choose_action(
                    player
                )
            )

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        self.timers.clear()
