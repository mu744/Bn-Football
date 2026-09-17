import math


class TransitionSystem:

    BUILD_UP = "build_up"
    COUNTER_ATTACK = "counter_attack"
    DEFENSIVE_TRANSITION = "defensive_transition"
    RECOVERY = "recovery"
    STABLE = "stable"

    def __init__(self, match):

        self.match = match

        self.state = self.STABLE
        self.previous_owner = None
        self.previous_team = None

        self.timer = 0.0
        self.transition_duration = 2.5

        self.counter_speed = 1.15
        self.recovery_speed = 1.20

        self.enabled = True

    # ==================================================
    # OUTILS
    # ==================================================

    def distance(self, a, b):

        return math.sqrt(
            (a.x - b.x) ** 2 +
            (a.y - b.y) ** 2
        )

    def get_ball_team(self):

        owner = self.match.ball_owner

        if owner is None:
            return None

        return owner.team

    # ==================================================
    # DÉTECTION DE LA TRANSITION
    # ==================================================

    def detect_transition(self):

        current_owner = self.match.ball_owner

        current_team = self.get_ball_team()

        # Récupération d'un ballon libre.
        if (
            current_owner is not None
            and self.previous_owner is None
        ):

            self.state = self.RECOVERY
            self.timer = self.transition_duration

            return

        # Changement d'équipe.
        if (
            current_team is not None
            and self.previous_team is not None
            and current_team != self.previous_team
        ):

            self.state = self.COUNTER_ATTACK
            self.timer = self.transition_duration

            return

        # Perte du ballon.
        if (
            current_owner is None
            and self.previous_owner is not None
        ):

            self.state = self.DEFENSIVE_TRANSITION
            self.timer = self.transition_duration

            return

        # Possession stable.
        if current_owner is not None:

            if self.state in (
                self.RECOVERY,
                self.COUNTER_ATTACK
            ):
                return

            self.state = self.BUILD_UP

    # ==================================================
    # MOUVEMENT DE CONTRE-ATTAQUE
    # ==================================================

    def counter_attack(self, team):

        players = (
            self.match.home_players
            if team == "blue"
            else self.match.away_players
        )

        for player in players:

            if not getattr(
                player,
                "on_pitch",
                True
            ):
                continue

            position = getattr(
                player,
                "position",
                ""
            )

            # Les attaquants partent immédiatement.
            if position == "AT":

                direction = (
                    1
                    if team == "blue"
                    else -1
                )

                player.x += (
                    direction *
                    2.2 *
                    self.counter_speed
                )

    # ==================================================
    # REPLI DÉFENSIF
    # ==================================================

    def defensive_recovery(self, team):

        players = (
            self.match.home_players
            if team == "blue"
            else self.match.away_players
        )

        field = self.match.field

        if team == "blue":
            target_x = (
                field.left +
                field.width * 0.32
            )
        else:
            target_x = (
                field.right -
                field.width * 0.32
            )

        for player in players:

            if not getattr(
                player,
                "on_pitch",
                True
            ):
                continue

            position = getattr(
                player,
                "position",
                ""
            )

            if position == "GK":
                continue

            dx = target_x - player.x

            player.x += (
                dx *
                0.025 *
                self.recovery_speed
            )

    # ==================================================
    # CONSTRUCTION
    # ==================================================

    def build_up(self, team):

        players = (
            self.match.home_players
            if team == "blue"
            else self.match.away_players
        )

        owner = self.match.ball_owner

        if owner is None:
            return

        for player in players:

            if player is owner:
                continue

            if not getattr(
                player,
                "on_pitch",
                True
            ):
                continue

            position = getattr(
                player,
                "position",
                ""
            )

            if position == "MC":

                dx = owner.x - player.x
                dy = owner.y - player.y

                player.x += dx * 0.01
                player.y += dy * 0.01

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self, delta_time):

        if not self.enabled:
            return

        self.detect_transition()

        if self.timer > 0:

            self.timer -= delta_time

            if self.timer < 0:
                self.timer = 0

        team = self.get_ball_team()

        if self.state == self.COUNTER_ATTACK:

            if team is not None:
                self.counter_attack(team)

        elif self.state == self.DEFENSIVE_TRANSITION:

            if self.previous_team is not None:
                self.defensive_recovery(
                    self.previous_team
                )

        elif self.state == self.BUILD_UP:

            if team is not None:
                self.build_up(team)

        elif self.state == self.RECOVERY:

            if team is not None:
                self.counter_attack(team)

        # Quand la transition est terminée,
        # on revient à une situation normale.
        if self.timer <= 0:

            if team is not None:
                self.state = self.BUILD_UP
            else:
                self.state = self.STABLE

        self.previous_owner = (
            self.match.ball_owner
        )

        if team is not None:

            self.previous_team = team

    # ==================================================
    # ÉTAT
    # ==================================================

    def get_state(self):

        return self.state

    def is_counter_attack(self):

        return (
            self.state ==
            self.COUNTER_ATTACK
        )

    def is_defensive_transition(self):

        return (
            self.state ==
            self.DEFENSIVE_TRANSITION
        )

    def is_building_up(self):

        return (
            self.state ==
            self.BUILD_UP
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

        self.state = self.STABLE
        self.previous_owner = None
        self.previous_team = None
        self.timer = 0.0
