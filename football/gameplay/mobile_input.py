class MobileInput:
    """
    Pont entre le contrôleur tactile et le gameplay.

    Ce module ne décide pas comment fonctionne une passe,
    un tir ou un tacle.

    Il transmet simplement les intentions du joueur
    au moteur de gameplay.
    """

    def __init__(self, match, touch_controller):

        self.match = match
        self.touch = touch_controller

        self.enabled = True

    # =========================================================
    # DEPLACEMENT
    # =========================================================

    def get_movement(self):

        if not self.enabled:
            return 0.0, 0.0

        return self.touch.get_movement()

    def is_sprinting(self):

        if not self.enabled:
            return False

        return self.touch.is_down(
            "sprint"
        )

    # =========================================================
    # ACTIONS
    # =========================================================

    def wants_pass(self):

        if not self.enabled:
            return False

        return self.touch.consume_pressed(
            "pass"
        )

    def wants_shoot(self):

        if not self.enabled:
            return False

        return self.touch.consume_pressed(
            "shoot"
        )

    def wants_tackle(self):

        if not self.enabled:
            return False

        return self.touch.consume_pressed(
            "tackle"
        )

    def wants_switch_player(self):

        if not self.enabled:
            return False

        return self.touch.consume_pressed(
            "switch"
        )

    # =========================================================
    # ETAT
    # =========================================================

    def enable(self):

        self.enabled = True

    def disable(self):

        self.enabled = False

    def reset(self):

        self.enabled = True
