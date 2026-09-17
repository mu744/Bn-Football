import math


class PossessionSystem:

    NONE = None
    BLUE = "blue"
    RED = "red"

    ATTACKING = "attacking"
    DEFENDING = "defending"
    TRANSITION = "transition"

    def __init__(self, match):

        self.match = match

        self.owner = None
        self.team = None

        self.previous_team = None

        self.phase = self.TRANSITION

        self.possession_count = {
            "blue": 0,
            "red": 0
        }

        self.transitions = {
            "blue_to_red": 0,
            "red_to_blue": 0
        }

        self.last_owner = None
        self.last_loser = None

        self.transition_timer = 0.0
        self.transition_duration = 1.0

        self.enabled = True

    # ==================================================
    # OUTILS
    # ==================================================

    def distance(self, player):

        if player is None:
            return float("inf")

        return math.sqrt(
            (player.x - self.match.ball_x) ** 2 +
            (player.y - self.match.ball_y) ** 2
        )

    # ==================================================
    # ÉQUIPE DU PORTEUR
    # ==================================================

    def get_owner_team(self):

        owner = self.match.ball_owner

        if owner is None:
            return None

        return owner.team

    # ==================================================
    # CHANGER DE POSSESSION
    # ==================================================

    def set_possession(self, player):

        if player is None:
            self.clear_possession()
            return False

        new_team = player.team
        old_team = self.team

        # Même joueur : rien à changer.
        if (
            self.owner is player
            and self.match.ball_owner is player
        ):
            return True

        # Transition entre équipes.
        if (
            old_team is not None
            and old_team != new_team
        ):

            key = (
                old_team +
                "_to_" +
                new_team
            )

            if key in self.transitions:

                self.transitions[key] += 1

        self.previous_team = old_team

        self.owner = player
        self.team = new_team

        self.last_owner = player

        self.possession_count[
            new_team
        ] += 1

        self.phase = self.ATTACKING

        self.transition_timer = (
            self.transition_duration
        )

        self.match.ball_owner = player

        self.match.ball_vx = 0.0
        self.match.ball_vy = 0.0

        return True

    # ==================================================
    # PERDRE LA POSSESSION
    # ==================================================

    def clear_possession(self):

        if self.owner is not None:

            self.last_loser = self.owner

        self.owner = None
        self.team = None

        self.previous_team = (
            self.previous_team
            if self.previous_team is not None
            else self.get_owner_team()
        )

        self.phase = self.TRANSITION

        self.transition_timer = (
            self.transition_duration
        )

        self.match.ball_owner = None

    # ==================================================
    # DÉTECTER LA POSSESSION EXISTANTE
    # ==================================================

    def synchronize(self):

        match_owner = self.match.ball_owner

        if match_owner is not self.owner:

            if match_owner is None:

                self.clear_possession()

            else:

                self.set_possession(
                    match_owner
                )

    # ==================================================
    # TROUVER LE JOUEUR LE PLUS PROCHE
    # ==================================================

    def nearest_player(self):

        players = (
            self.match.home_players +
            self.match.away_players
        )

        closest = None
        closest_distance = float("inf")

        for player in players:

            if not getattr(
                player,
                "on_pitch",
                True
            ):
                continue

            distance = self.distance(
                player
            )

            if distance < closest_distance:

                closest_distance = distance
                closest = player

        return closest

    # ==================================================
    # RÉCUPÉRATION AUTOMATIQUE
    # ==================================================

    def try_recover_ball(
        self,
        max_distance=30.0
    ):

        if self.match.ball_owner is not None:
            return False

        player = self.nearest_player()

        if player is None:
            return False

        if self.distance(player) > max_distance:
            return False

        return self.set_possession(
            player
        )

    # ==================================================
    # TRANSITION
    # ==================================================

    def update_transition(
        self,
        delta_time
    ):

        if self.transition_timer <= 0:
            return

        self.transition_timer -= delta_time

        if self.transition_timer < 0:

            self.transition_timer = 0

        if self.transition_timer == 0:

            if self.team is not None:

                self.phase = (
                    self.ATTACKING
                )

            else:

                self.phase = (
                    self.TRANSITION
                )

    # ==================================================
    # MISE À JOUR
    # ==================================================

    def update(self, delta_time):

        if not self.enabled:
            return

        self.synchronize()

        self.update_transition(
            delta_time
        )

    # ==================================================
    # ÉTAT
    # ==================================================

    def get_team(self):

        return self.team

    def get_owner(self):

        return self.owner

    def get_phase(self):

        return self.phase

    def is_blue_attacking(self):

        return (
            self.team == self.BLUE
            and self.phase == self.ATTACKING
        )

    def is_red_attacking(self):

        return (
            self.team == self.RED
            and self.phase == self.ATTACKING
        )

    def is_transitioning(self):

        return (
            self.phase == self.TRANSITION
        )

    # ==================================================
    # STATISTIQUES
    # ==================================================

    def get_possession_count(self, team):

        return self.possession_count.get(
            team,
            0
        )

    def get_transitions(self):

        return dict(
            self.transitions
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

        self.owner = None
        self.team = None
        self.previous_team = None

        self.phase = self.TRANSITION

        self.possession_count = {
            "blue": 0,
            "red": 0
        }

        self.transitions = {
            "blue_to_red": 0,
            "red_to_blue": 0
        }

        self.last_owner = None
        self.last_loser = None

        self.transition_timer = 0.0
