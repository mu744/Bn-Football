import math


class StaminaSystem:
    """
    Système complet d'endurance.

    Gère :
    - consommation pendant le sprint
    - consommation pendant les déplacements
    - récupération
    - fatigue
    - état physique du joueur
    """

    def __init__(self, match):

        self.match = match
        self.enabled = True

        # Consommation.
        self.sprint_drain = 8.0
        self.running_drain = 1.2
        self.idle_recovery = 3.5

        # Seuils.
        self.high_energy = 75.0
        self.medium_energy = 50.0
        self.low_energy = 30.0
        self.critical_energy = 15.0

    # =========================================================
    # JOUEURS
    # =========================================================

    def get_players(self):

        return (
            self.match.home_players +
            self.match.away_players
        )

    # =========================================================
    # VITESSE
    # =========================================================

    def get_speed_ratio(self, player):

        stamina = max(
            0.0,
            min(
                100.0,
                getattr(
                    player,
                    "stamina",
                    100.0
                )
            )
        )

        if stamina >= self.high_energy:
            return 1.0

        if stamina >= self.medium_energy:
            return 0.96

        if stamina >= self.low_energy:
            return 0.90

        if stamina >= self.critical_energy:
            return 0.80

        return 0.68

    # =========================================================
    # CONSOMMATION
    # =========================================================

    def consume(
        self,
        player,
        amount
    ):

        if player is None:
            return

        player.stamina = max(
            0.0,
            getattr(
                player,
                "stamina",
                100.0
            ) - amount
        )

    # =========================================================
    # RECUPERATION
    # =========================================================

    def recover(
        self,
        player,
        amount
    ):

        if player is None:
            return

        player.stamina = min(
            100.0,
            getattr(
                player,
                "stamina",
                100.0
            ) + amount
        )

    # =========================================================
    # ETAT
    # =========================================================

    def get_state(self, player):

        stamina = getattr(
            player,
            "stamina",
            100.0
        )

        if stamina >= self.high_energy:
            return "fresh"

        if stamina >= self.medium_energy:
            return "normal"

        if stamina >= self.low_energy:
            return "tired"

        if stamina >= self.critical_energy:
            return "very_tired"

        return "exhausted"

    # =========================================================
    # UPDATE JOUEUR
    # =========================================================

    def update_player(
        self,
        player,
        delta_time
    ):

        if not getattr(
            player,
            "on_pitch",
            True
        ):
            return

        speed = player.get_current_speed()

        # Déplacement actif.
        if speed > 0.25:

            sprinting = getattr(
                player,
                "is_sprinting",
                False
            )

            if sprinting:

                self.consume(
                    player,
                    self.sprint_drain *
                    delta_time
                )

            else:

                self.consume(
                    player,
                    self.running_drain *
                    delta_time
                )

        else:

            # Récupération lorsque le joueur ne court pas.
            self.recover(
                player,
                self.idle_recovery *
                delta_time
            )

    # =========================================================
    # UPDATE GLOBAL
    # =========================================================

    def update(
        self,
        delta_time=0.016
    ):

        if not self.enabled:
            return

        for player in self.get_players():

            self.update_player(
                player,
                delta_time
            )

    # =========================================================
    # RESET
    # =========================================================

    def reset(self):

        for player in self.get_players():

            player.stamina = 100.0

        self.enabled = True

    # =========================================================
    # CONTROLE
    # =========================================================

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
