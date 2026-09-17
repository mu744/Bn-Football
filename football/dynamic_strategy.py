class DynamicStrategy:

    # ==================================================
    # ÉTATS DU MATCH
    # ==================================================

    STATES = (
        "losing",
        "drawing",
        "winning",
        "late_losing",
        "late_winning"
    )

    def __init__(self, tactics):

        self.tactics = tactics

        self.enabled = True

        self.current_state = "drawing"

        self.original_mentality = (
            tactics.mentality
        )

        self.original_pressing = (
            tactics.pressing
        )

        self.original_tempo = (
            tactics.tempo
        )

        self.original_depth = (
            tactics.depth
        )

        self.original_width = (
            tactics.width
        )

    # ==================================================
    # CALCUL DE LA SITUATION
    # ==================================================

    def get_match_state(
        self,
        own_score,
        opponent_score,
        minute,
        match_duration=90
    ):

        difference = (
            own_score -
            opponent_score
        )

        remaining = (
            match_duration -
            minute
        )

        # Fin de match en étant mené.
        if (
            difference < 0
            and remaining <= 15
        ):
            return "late_losing"

        # Fin de match en gagnant.
        if (
            difference > 0
            and remaining <= 10
        ):
            return "late_winning"

        if difference < 0:
            return "losing"

        if difference > 0:
            return "winning"

        return "drawing"

    # ==================================================
    # STRATÉGIE QUAND ON PERD
    # ==================================================

    def apply_losing(self):

        self.tactics.set_mentality(
            "offensive"
        )

        self.tactics.set_pressing(
            "high"
        )

        self.tactics.set_tempo(
            1.20
        )

        self.tactics.set_depth(
            1.20
        )

        self.tactics.set_width(
            1.15
        )

        self.tactics.enable_counter_attack()

    # ==================================================
    # STRATÉGIE FIN DE MATCH EN PERDANT
    # ==================================================

    def apply_late_losing(self):

        self.tactics.set_mentality(
            "all_out_attack"
        )

        self.tactics.set_pressing(
            "extreme"
        )

        self.tactics.set_tempo(
            1.40
        )

        self.tactics.set_depth(
            1.40
        )

        self.tactics.set_width(
            1.30
        )

        self.tactics.enable_counter_attack()

    # ==================================================
    # MATCH NUL
    # ==================================================

    def apply_drawing(self):

        self.tactics.set_mentality(
            "balanced"
        )

        self.tactics.set_pressing(
            "medium"
        )

        self.tactics.set_tempo(
            1.00
        )

        self.tactics.set_depth(
            1.00
        )

        self.tactics.set_width(
            1.00
        )

        self.tactics.enable_counter_attack()

    # ==================================================
    # STRATÉGIE QUAND ON GAGNE
    # ==================================================

    def apply_winning(self):

        self.tactics.set_mentality(
            "balanced"
        )

        self.tactics.set_pressing(
            "medium"
        )

        self.tactics.set_tempo(
            0.90
        )

        self.tactics.set_depth(
            0.90
        )

        self.tactics.set_width(
            0.95
        )

        self.tactics.enable_possession()

    # ==================================================
    # FIN DE MATCH EN GAGNANT
    # ==================================================

    def apply_late_winning(self):

        self.tactics.set_mentality(
            "defensive"
        )

        self.tactics.set_pressing(
            "low"
        )

        self.tactics.set_tempo(
            0.70
        )

        self.tactics.set_depth(
            0.75
        )

        self.tactics.set_width(
            0.85
        )

        self.tactics.disable_counter_attack()

        self.tactics.enable_possession()

    # ==================================================
    # APPLICATION
    # ==================================================

    def apply_state(self, state):

        if not self.enabled:
            return

        if state not in self.STATES:
            state = "drawing"

        self.current_state = state

        if state == "losing":
            self.apply_losing()

        elif state == "late_losing":
            self.apply_late_losing()

        elif state == "winning":
            self.apply_winning()

        elif state == "late_winning":
            self.apply_late_winning()

        else:
            self.apply_drawing()

    # ==================================================
    # MISE À JOUR
    # ==================================================

    def update(
        self,
        own_score,
        opponent_score,
        minute,
        match_duration=90
    ):

        if not self.enabled:
            return self.current_state

        state = self.get_match_state(
            own_score,
            opponent_score,
            minute,
            match_duration
        )

        if state != self.current_state:

            self.apply_state(state)

        return self.current_state

    # ==================================================
    # ACTIVATION
    # ==================================================

    def enable(self):

        self.enabled = True

    def disable(self):

        self.enabled = False

    # ==================================================
    # ÉTAT
    # ==================================================

    def get_state(self):

        return self.current_state

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        self.current_state = "drawing"

        self.tactics.set_mentality(
            self.original_mentality
        )

        self.tactics.set_pressing(
            self.original_pressing
        )

        self.tactics.set_tempo(
            self.original_tempo
        )

        self.tactics.set_depth(
            self.original_depth
        )

        self.tactics.set_width(
            self.original_width
        )
