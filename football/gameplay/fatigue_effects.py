class FatigueEffects:
    """
    Transforme le niveau de fatigue en conséquences
    sur les performances du joueur.

    Le système ne modifie pas directement la stamina.
    Il fournit uniquement les multiplicateurs.
    """

    def __init__(self, match):

        self.match = match
        self.enabled = True

    # =========================================================
    # MULTIPLICATEUR GENERAL
    # =========================================================

    def performance_multiplier(
        self,
        player
    ):

        stamina = getattr(
            player,
            "stamina",
            100.0
        )

        if stamina >= 75:
            return 1.0

        if stamina >= 50:
            return 0.96

        if stamina >= 30:
            return 0.90

        if stamina >= 15:
            return 0.80

        return 0.68

    # =========================================================
    # VITESSE
    # =========================================================

    def speed_multiplier(
        self,
        player
    ):

        stamina = getattr(
            player,
            "stamina",
            100.0
        )

        if stamina >= 75:
            return 1.0

        if stamina >= 50:
            return 0.97

        if stamina >= 30:
            return 0.92

        if stamina >= 15:
            return 0.82

        return 0.70

    # =========================================================
    # PASSE
    # =========================================================

    def passing_multiplier(
        self,
        player
    ):

        stamina = getattr(
            player,
            "stamina",
            100.0
        )

        if stamina >= 60:
            return 1.0

        if stamina >= 35:
            return 0.94

        if stamina >= 15:
            return 0.85

        return 0.72

    # =========================================================
    # TIR
    # =========================================================

    def shooting_multiplier(
        self,
        player
    ):

        stamina = getattr(
            player,
            "stamina",
            100.0
        )

        if stamina >= 60:
            return 1.0

        if stamina >= 35:
            return 0.95

        if stamina >= 15:
            return 0.86

        return 0.74

    # =========================================================
    # CONTROLE DE BALLE
    # =========================================================

    def control_multiplier(
        self,
        player
    ):

        stamina = getattr(
            player,
            "stamina",
            100.0
        )

        if stamina >= 60:
            return 1.0

        if stamina >= 35:
            return 0.94

        if stamina >= 15:
            return 0.84

        return 0.72

    # =========================================================
    # ETAT
    # =========================================================

    def get_state(
        self,
        player
    ):

        stamina = getattr(
            player,
            "stamina",
            100.0
        )

        if stamina >= 75:
            return "fresh"

        if stamina >= 50:
            return "normal"

        if stamina >= 30:
            return "tired"

        if stamina >= 15:
            return "very_tired"

        return "exhausted"

    # =========================================================
    # UPDATE
    # =========================================================

    def update(
        self,
        delta_time=0.016
    ):

        if not self.enabled:
            return

        # Les effets sont calculés à la demande.
        # Aucun traitement lourd nécessaire ici.
        return

    # =========================================================
    # CONTROLE
    # =========================================================

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def reset(self):
        self.enabled = True
