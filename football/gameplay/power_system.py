import time


class PowerSystem:
    """
    Système central de puissance pour les actions du joueur.

    Prévu pour :
    - passes
    - tirs
    - futures commandes tactiles
    - clavier
    """

    MIN_POWER = 0.0
    MAX_POWER = 1.0

    def __init__(self):
        self.charging = False
        self.action = None
        self.start_time = 0.0
        self.power = 0.0

        # Temps nécessaire pour atteindre 100 %
        self.max_charge_time = 1.20

        # Puissance minimale utilisable
        self.minimum_release_power = 0.08

    # ==================================================
    # DÉBUT DE CHARGE
    # ==================================================

    def start(self, action):
        """
        Commence à charger une action.

        action :
        - "pass"
        - "shoot"
        """

        if action not in ("pass", "shoot"):
            return False

        if self.charging:
            return False

        self.charging = True
        self.action = action
        self.start_time = time.monotonic()
        self.power = 0.0

        return True

    # ==================================================
    # MISE À JOUR
    # ==================================================

    def update(self):
        """
        Met à jour la puissance pendant l'appui.
        """

        if not self.charging:
            return self.power

        elapsed = time.monotonic() - self.start_time

        self.power = min(
            elapsed / self.max_charge_time,
            self.MAX_POWER
        )

        return self.power

    # ==================================================
    # LIBÉRATION
    # ==================================================

    def release(self):
        """
        Termine la charge et retourne :

        (action, puissance)
        """

        if not self.charging:
            return None, 0.0

        self.update()

        action = self.action
        power = self.power

        self.charging = False
        self.action = None
        self.start_time = 0.0
        self.power = 0.0

        if power < self.minimum_release_power:
            power = self.minimum_release_power

        return action, power

    # ==================================================
    # ANNULATION
    # ==================================================

    def cancel(self):
        self.charging = False
        self.action = None
        self.start_time = 0.0
        self.power = 0.0

    # ==================================================
    # PUISSANCE ACTUELLE
    # ==================================================

    def get_power(self):
        if self.charging:
            self.update()

        return max(
            self.MIN_POWER,
            min(self.MAX_POWER, self.power)
        )

    # ==================================================
    # POURCENTAGE
    # ==================================================

    def get_percentage(self):
        return round(self.get_power() * 100)

    # ==================================================
    # ÉTAT
    # ==================================================

    def is_charging(self):
        return self.charging

    def get_action(self):
        return self.action

    # ==================================================
    # NIVEAU DE PUISSANCE
    # ==================================================

    def get_level(self):
        power = self.get_power()

        if power < 0.25:
            return "faible"

        if power < 0.55:
            return "normale"

        if power < 0.80:
            return "forte"

        return "maximale"

    # ==================================================
    # CONVERSION POUR UNE PASSE
    # ==================================================

    def pass_speed(self, power):
        """
        Convertit une puissance 0..1
        en vitesse de ballon.
        """

        minimum = 5.5
        maximum = 14.5

        power = max(
            0.0,
            min(1.0, power)
        )

        return minimum + (
            maximum - minimum
        ) * power

    # ==================================================
    # CONVERSION POUR UN TIR
    # ==================================================

    def shot_speed(self, power):
        """
        Convertit une puissance 0..1
        en vitesse de tir.
        """

        minimum = 8.0
        maximum = 19.0

        power = max(
            0.0,
            min(1.0, power)
        )

        return minimum + (
            maximum - minimum
        ) * power

    # ==================================================
    # RÉINITIALISATION
    # ==================================================

    def reset(self):
        self.cancel()
