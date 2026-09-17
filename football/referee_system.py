import math
import random


class RefereeSystem:

    FOUL_NONE = "none"
    FOUL_NORMAL = "foul"
    FOUL_ADVANTAGE = "advantage"
    FOUL_PENALTY = "penalty"

    def __init__(self, match):

        self.match = match

        self.enabled = True

        self.foul_probability = 0.018
        self.offside_enabled = True

        self.yellow_cards = {
            "blue": 0,
            "red": 0
        }

        self.red_cards = {
            "blue": 0,
            "red": 0
        }

        self.fouls = {
            "blue": 0,
            "red": 0
        }

        self.last_event = None

        self.advantage_timer = 0.0

    # ==================================================
    # OUTILS
    # ==================================================

    def distance(self, a, b):

        return math.sqrt(
            (a.x - b.x) ** 2 +
            (a.y - b.y) ** 2
        )

    def get_team(self, player):

        if player is None:
            return None

        return player.team

    # ==================================================
    # FAUTE
    # ==================================================

    def detect_foul(
        self,
        defender,
        attacker,
        intensity=1.0
    ):

        if not self.enabled:
            return False

        if defender is None:
            return False

        if attacker is None:
            return False

        if defender.team == attacker.team:
            return False

        distance = self.distance(
            defender,
            attacker
        )

        if distance > 38:
            return False

        chance = (
            self.foul_probability *
            intensity
        )

        # Contact très proche.
        if distance < 22:
            chance *= 2.0

        # Une vitesse élevée augmente légèrement
        # le risque de faute.
        speed = defender.get_current_speed()

        if speed > 4:
            chance *= 1.35

        chance = min(
            0.20,
            chance
        )

        if random.random() > chance:
            return False

        self.register_foul(
            defender,
            attacker
        )

        return True

    # ==================================================
    # ENREGISTRER LA FAUTE
    # ==================================================

    def register_foul(
        self,
        defender,
        attacker
    ):

        team = defender.team

        self.fouls[team] += 1

        # Faute dans la surface.
        if self.is_penalty_area(
            attacker
        ):

            event_type = self.FOUL_PENALTY

        else:

            event_type = self.FOUL_NORMAL

        # Carton occasionnel.
        if self.should_yellow_card(
            defender
        ):

            self.give_yellow_card(
                defender
            )

        self.last_event = {
            "type": event_type,
            "defender": defender,
            "attacker": attacker,
            "team": team
        }

    # ==================================================
    # SURFACE DE RÉPARATION
    # ==================================================

    def is_penalty_area(self, player):

        field = self.match.field

        if player.team == "blue":

            # Pour le défenseur bleu, sa surface
            # est du côté gauche.
            return player.x <= (
                field.left + 95
            )

        # Surface de l'équipe rouge.
        return player.x >= (
            field.right - 95
        )

    # ==================================================
    # CARTON JAUNE
    # ==================================================

    def should_yellow_card(self, player):

        if player is None:
            return False

        # Environ une faute sur quatre peut
        # entraîner un avertissement.
        return random.random() < 0.25

    def give_yellow_card(self, player):

        team = player.team

        self.yellow_cards[team] += 1

        # Deux jaunes = rouge.
        if self.yellow_cards[team] % 2 == 0:

            self.give_red_card(
                player
            )

    # ==================================================
    # CARTON ROUGE
    # ==================================================

    def give_red_card(self, player):

        if player is None:
            return False

        team = player.team

        self.red_cards[team] += 1

        player.on_pitch = False

        # Un joueur expulsé ne doit plus
        # contrôler le ballon.
        if self.match.ball_owner is player:

            self.match.ball_owner = None

        self.last_event = {
            "type": "red_card",
            "player": player,
            "team": team
        }

        return True

    # ==================================================
    # HORS-JEU
    # ==================================================

    def check_offside(
        self,
        player,
        ball_x=None
    ):

        if not self.enabled:
            return False

        if not self.offside_enabled:
            return False

        if player is None:
            return False

        # Le gardien n'est pas traité comme
        # une cible offensive de hors-jeu.
        if getattr(
            player,
            "position",
            ""
        ) == "GK":

            return False

        if ball_x is None:
            ball_x = self.match.ball_x

        opponents = (
            self.match.away_players
            if player.team == "blue"
            else self.match.home_players
        )

        active_opponents = [
            p for p in opponents
            if getattr(
                p,
                "on_pitch",
                True
            )
        ]

        if len(active_opponents) < 2:
            return False

        positions = sorted(
            [p.x for p in active_opponents]
        )

        if player.team == "blue":

            second_last = positions[-2]

            beyond_defense = (
                player.x > second_last
            )

            beyond_ball = (
                player.x > ball_x
            )

        else:

            second_last = positions[1]

            beyond_defense = (
                player.x < second_last
            )

            beyond_ball = (
                player.x < ball_x
            )

        if beyond_defense and beyond_ball:

            self.last_event = {
                "type": "offside",
                "player": player,
                "team": player.team
            }

            return True

        return False

    # ==================================================
    # AVANTAGE
    # ==================================================

    def apply_advantage(self):

        self.advantage_timer = 2.5

        self.last_event = {
            "type": self.FOUL_ADVANTAGE
        }

    def update_advantage(self, delta_time):

        if self.advantage_timer <= 0:
            return

        self.advantage_timer -= delta_time

        if self.advantage_timer < 0:
            self.advantage_timer = 0

    # ==================================================
    # MISE À JOUR
    # ==================================================

    def update(self, delta_time):

        if not self.enabled:
            return

        self.update_advantage(
            delta_time
        )

    # ==================================================
    # STATISTIQUES
    # ==================================================

    def get_statistics(self):

        return {
            "blue_fouls": self.fouls["blue"],
            "red_fouls": self.fouls["red"],
            "blue_yellow": (
                self.yellow_cards["blue"]
            ),
            "red_yellow": (
                self.yellow_cards["red"]
            ),
            "blue_red": (
                self.red_cards["blue"]
            ),
            "red_red": (
                self.red_cards["red"]
            )
        }

    # ==================================================
    # DERNIER ÉVÉNEMENT
    # ==================================================

    def get_last_event(self):

        return self.last_event

    def clear_last_event(self):

        self.last_event = None

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

        self.yellow_cards = {
            "blue": 0,
            "red": 0
        }

        self.red_cards = {
            "blue": 0,
            "red": 0
        }

        self.fouls = {
            "blue": 0,
            "red": 0
        }

        self.last_event = None
        self.advantage_timer = 0.0
