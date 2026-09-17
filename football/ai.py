import math
import random


class FootballAI:

    DIFFICULTIES = {
        "beginner": {
            "reaction": 0.75,
            "decision": 0.55,
            "pass_accuracy": 0.55,
            "shot_accuracy": 0.50,
            "marking": 0.45,
            "positioning": 0.45,
            "interception": 0.35,
            "pressing": 0.40,
            "error_rate": 0.35,
            "chase_speed": 0.85,
        },

        "normal": {
            "reaction": 0.60,
            "decision": 0.70,
            "pass_accuracy": 0.68,
            "shot_accuracy": 0.63,
            "marking": 0.58,
            "positioning": 0.60,
            "interception": 0.52,
            "pressing": 0.55,
            "error_rate": 0.22,
            "chase_speed": 0.95,
        },

        "high": {
            "reaction": 0.48,
            "decision": 0.80,
            "pass_accuracy": 0.78,
            "shot_accuracy": 0.74,
            "marking": 0.70,
            "positioning": 0.72,
            "interception": 0.64,
            "pressing": 0.68,
            "error_rate": 0.15,
            "chase_speed": 1.00,
        },

        "pro": {
            "reaction": 0.38,
            "decision": 0.88,
            "pass_accuracy": 0.85,
            "shot_accuracy": 0.82,
            "marking": 0.80,
            "positioning": 0.82,
            "interception": 0.74,
            "pressing": 0.78,
            "error_rate": 0.10,
            "chase_speed": 1.05,
        },

        "superstar": {
            "reaction": 0.28,
            "decision": 0.94,
            "pass_accuracy": 0.91,
            "shot_accuracy": 0.89,
            "marking": 0.88,
            "positioning": 0.90,
            "interception": 0.84,
            "pressing": 0.87,
            "error_rate": 0.06,
            "chase_speed": 1.10,
        },

        "legend": {
            "reaction": 0.18,
            "decision": 0.98,
            "pass_accuracy": 0.96,
            "shot_accuracy": 0.94,
            "marking": 0.94,
            "positioning": 0.96,
            "interception": 0.92,
            "pressing": 0.94,
            "error_rate": 0.025,
            "chase_speed": 1.15,
        },
    }

    def __init__(
        self,
        match,
        difficulty="normal"
    ):

        self.match = match

        self.difficulty_name = (
            difficulty
            if difficulty in self.DIFFICULTIES
            else "normal"
        )

        self.profile = self.DIFFICULTIES[
            self.difficulty_name
        ]

        self.reaction_timer = 0.0

        self.decision_timer = 0.0

    # ==================================================
    # DIFFICULTÉ
    # ==================================================

    def set_difficulty(self, difficulty):

        if difficulty not in self.DIFFICULTIES:
            difficulty = "normal"

        self.difficulty_name = difficulty

        self.profile = self.DIFFICULTIES[
            difficulty
        ]

    def get_difficulty(self):

        return self.difficulty_name

    def get_profile(self):

        return self.profile.copy()

    # ==================================================
    # HASARD CONTRÔLÉ
    # ==================================================

    def succeeds(self, probability):

        probability = max(
            0.0,
            min(1.0, probability)
        )

        return random.random() <= probability

    def makes_mistake(self):

        return self.succeeds(
            self.profile["error_rate"]
        )

    # ==================================================
    # DISTANCE
    # ==================================================

    def distance(
        self,
        player,
        x,
        y
    ):

        return math.sqrt(
            (player.x - x) ** 2 +
            (player.y - y) ** 2
        )

    def player_distance(self, a, b):

        return math.sqrt(
            (a.x - b.x) ** 2 +
            (a.y - b.y) ** 2
        )

    # ==================================================
    # JOUEUR LE PLUS PROCHE
    # ==================================================

    def nearest_player(
        self,
        players,
        x,
        y
    ):

        if not players:
            return None

        closest = None
        best_distance = float("inf")

        for player in players:

            d = self.distance(
                player,
                x,
                y
            )

            if d < best_distance:

                best_distance = d
                closest = player

        return closest

    # ==================================================
    # RÉACTION
    # ==================================================

    def can_react(self, delta_time):

        self.reaction_timer -= delta_time

        if self.reaction_timer > 0:

            return False

        reaction = self.profile["reaction"]

        self.reaction_timer = (
            reaction +
            random.uniform(
                0.02,
                0.12
            )
        )

        return True

    # ==================================================
    # DÉCISION
    # ==================================================

    def should_make_decision(
        self,
        delta_time
    ):

        self.decision_timer -= delta_time

        if self.decision_timer > 0:

            return False

        decision = self.profile["decision"]

        self.decision_timer = (
            0.20 +
            (1.0 - decision) *
            0.55
        )

        return True

    # ==================================================
    # VITESSE DE POURSUITE
    # ==================================================

    def get_chase_speed(self):

        return self.profile[
            "chase_speed"
        ]

    # ==================================================
    # PASSE
    # ==================================================

    def should_pass(self, player):

        if player is None:
            return False

        if self.makes_mistake():
            return False

        return self.succeeds(
            self.profile[
                "pass_accuracy"
            ]
        )

    def choose_pass_target(
        self,
        player,
        teammates
    ):

        if not teammates:
            return None

        best = None
        best_score = -999999

        for teammate in teammates:

            if teammate is player:
                continue

            dx = teammate.x - player.x
            dy = teammate.y - player.y

            distance = math.sqrt(
                dx * dx +
                dy * dy
            )

            if distance < 30:
                continue

            if distance > 400:
                continue

            score = 0.0

            # Distance raisonnable.
            score -= abs(
                distance - 130
            ) * 0.5

            # Progression vers le but.
            if player.team == "blue":

                if teammate.x > player.x:
                    score += 65

            else:

                if teammate.x < player.x:
                    score += 65

            # Joueur démarqué.
            opponents = (
                self.match.away_players
                if player.team == "blue"
                else self.match.home_players
            )

            nearest_opponent = 9999

            for opponent in opponents:

                d = self.player_distance(
                    teammate,
                    opponent
                )

                nearest_opponent = min(
                    nearest_opponent,
                    d
                )

            score += min(
                nearest_opponent,
                100
            )

            # Les hauts niveaux évaluent mieux
            # les solutions disponibles.
            score *= (
                0.70 +
                self.profile["decision"] *
                0.30
            )

            if score > best_score:

                best_score = score
                best = teammate

        return best

    # ==================================================
    # TIR
    # ==================================================

    def should_shoot(
        self,
        player,
        distance_to_goal
    ):

        if player is None:
            return False

        # Trop loin.
        if distance_to_goal > 500:
            return False

        base_chance = (
            self.profile[
                "shot_accuracy"
            ]
        )

        # Plus proche = décision plus probable.
        if distance_to_goal < 220:

            base_chance += 0.18

        elif distance_to_goal < 320:

            base_chance += 0.08

        if self.makes_mistake():

            base_chance -= 0.25

        return self.succeeds(
            max(
                0.05,
                min(0.95, base_chance)
            )
        )

    # ==================================================
    # PRESSING
    # ==================================================

    def should_press(self):

        return self.succeeds(
            self.profile[
                "pressing"
            ]
        )

    # ==================================================
    # MARQUAGE
    # ==================================================

    def should_mark(self):

        return self.succeeds(
            self.profile[
                "marking"
            ]
        )

    # ==================================================
    # POSITIONNEMENT
    # ==================================================

    def positioning_quality(self):

        return self.profile[
            "positioning"
        ]

    # ==================================================
    # INTERCEPTION
    # ==================================================

    def should_intercept(
        self,
        distance
    ):

        if distance > 45:
            return False

        chance = (
            self.profile[
                "interception"
            ]
        )

        if distance < 25:

            chance += 0.10

        return self.succeeds(
            min(0.95, chance)
        )

    # ==================================================
    # POURSUITE DU BALLON
    # ==================================================

    def chase_ball(
        self,
        player
    ):

        if player is None:
            return False

        distance = self.distance(
            player,
            self.match.ball_x,
            self.match.ball_y
        )

        if distance <= 25:
            return False

        speed = (
            2.8 *
            self.get_chase_speed()
        )

        dx = (
            self.match.ball_x -
            player.x
        )

        dy = (
            self.match.ball_y -
            player.y
        )

        length = math.sqrt(
            dx * dx +
            dy * dy
        )

        if length <= 0:
            return False

        dx /= length
        dy /= length

        player.x += dx * speed
        player.y += dy * speed

        player.direction_x = dx
        player.direction_y = dy

        return True

    # ==================================================
    # MISE À JOUR
    # ==================================================

    def update(self, delta_time):

        if not self.can_react(
            delta_time
        ):
            return

        # Le comportement collectif reste
        # géré par TeamAI.
        # Ce module fournit les décisions
        # individuelles.
        return

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        self.reaction_timer = 0.0
        self.decision_timer = 0.0
