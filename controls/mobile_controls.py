from controls.touch import TouchController
from football.gameplay.mobile_input import MobileInput


class MobileControls:
    """
    Gestionnaire global des contrôles Android.

    Architecture :

        Android Touch
              ↓
        TouchController
              ↓
        MobileInput
              ↓
        Gameplay
    """

    def __init__(
        self,
        match,
        width=900,
        height=600
    ):

        self.match = match

        self.touch = TouchController(
            width,
            height
        )

        self.input = MobileInput(
            match,
            self.touch
        )

        self.enabled = True

    # =========================================================
    # EVENEMENTS
    # =========================================================

    def handle_event(self, event):

        if not self.enabled:
            return False

        return self.touch.handle_event(
            event
        )

    # =========================================================
    # UPDATE
    # =========================================================

    def update(self):

        if not self.enabled:
            return

    # =========================================================
    # AFFICHAGE
    # =========================================================

    def draw(self, screen):

        if not self.enabled:
            return

        self.touch.draw(
            screen
        )

    # =========================================================
    # ACCES GAMEPLAY
    # =========================================================

    def get_input(self):

        return self.input

    # =========================================================
    # CONTROLE
    # =========================================================

    def enable(self):

        self.enabled = True
        self.touch.enable()
        self.input.enable()

    def disable(self):

        self.enabled = False
        self.touch.disable()
        self.input.disable()

    def reset(self):

        self.touch.reset()
        self.input.reset()
