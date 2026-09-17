import math


class MovementController:
    """
    Système de déplacement physique du joueur.

    Gère :
    - accélération
    - décélération
    - sprint
    - vitesse maximale
    - influence de la fatigue
    - changement de direction
    - contrôle du joueur sur le terrain
    """

    def __init__(self, player):
        self.player = player

        # ---------------------------------------------------------
        # PHYSIQUE
        # ---------------------------------------------------------
        self.velocity_x = 0.0
        self.velocity_y = 0.0

        self.acceleration = 0.55
        self.deceleration = 0.72

        self.max_speed = player.speed

        self.sprint_multiplier = 1.35

        # Contrôle des changements de direction
        self.turn_control = 0.22

        # ---------------------------------------------------------
        # ÉTAT
        # ---------------------------------------------------------
        self.current_sprint = False

    # =============================================================
    # UTILITAIRES
    # =============================================================

    def get_direction(self, dx, dy):
        length = math.sqrt(dx * dx + dy * dy)

        if length <= 0.001:
            return 0.0, 0.0

        return dx / length, dy / length

    def get_stamina_multiplier(self):
        """
        Influence de l'endurance sur la vitesse.

        Plus le joueur est fatigué, plus sa vitesse maximale diminue.
        """

        stamina = getattr(
            self.player,
            "stamina",
            100.0
        )

        stamina = max(
            0.0,
            min(100.0, float(stamina))
        )

        if stamina >= 75.0:
            return 1.00

        if stamina >= 50.0:
            return 0.97

        if stamina >= 30.0:
            return 0.92

        if stamina >= 15.0:
            return 0.82

        return 0.70

    def get_sprint_multiplier(self):
        """
        Retourne le multiplicateur de sprint adapté
        à l'endurance actuelle.
        """

        stamina = getattr(
            self.player,
            "stamina",
            100.0
        )

        if stamina <= 15.0:
            return 1.0

        if stamina <= 30.0:
            return 1.10

        if stamina <= 50.0:
            return 1.20

        return self.sprint_multiplier

    # =============================================================
    # ACCÉLÉRATION
    # =============================================================

    def accelerate(self, dx, dy, sprint=False):
        """
        Accélère le joueur dans une direction.
        """

        direction_x, direction_y = self.get_direction(dx, dy)

        if direction_x == 0.0 and direction_y == 0.0:
            self.brake()
            return

        stamina = getattr(
            self.player,
            "stamina",
            100.0
        )

        # Un joueur complètement épuisé ne peut plus sprinter.
        if stamina <= 15.0:
            sprint = False

        self.current_sprint = bool(sprint)

        # ---------------------------------------------------------
        # VITESSE DE BASE
        # ---------------------------------------------------------
        stamina_multiplier = self.get_stamina_multiplier()

        max_speed = self.max_speed * stamina_multiplier

        # ---------------------------------------------------------
        # SPRINT
        # ---------------------------------------------------------
        if sprint:
            max_speed *= self.get_sprint_multiplier()

        # Sécurité
        max_speed = max(0.5, max_speed)

        target_x = direction_x * max_speed
        target_y = direction_y * max_speed

        # ---------------------------------------------------------
        # CHANGEMENT DE DIRECTION
        # ---------------------------------------------------------
        current_speed = self.get_speed()

        if current_speed > 0.1:
            current_x = self.velocity_x / current_speed
            current_y = self.velocity_y / current_speed

            dot = (
                current_x * direction_x +
                current_y * direction_y
            )

            dot = max(-1.0, min(1.0, dot))

            # Virage brusque = accélération légèrement réduite
            turn_factor = (
                0.55 +
                (dot + 1.0) * 0.225
            )

            acceleration = (
                self.acceleration *
                turn_factor
            )
        else:
            acceleration = self.acceleration

        # ---------------------------------------------------------
        # ACCÉLÉRATION PROGRESSIVE
        # ---------------------------------------------------------
        self.velocity_x += (
            target_x - self.velocity_x
        ) * acceleration

        self.velocity_y += (
            target_y - self.velocity_y
        ) * acceleration

        # ---------------------------------------------------------
        # LIMITE DE VITESSE
        # ---------------------------------------------------------
        speed = self.get_speed()

        if speed > max_speed:
            factor = max_speed / speed

            self.velocity_x *= factor
            self.velocity_y *= factor

        # ---------------------------------------------------------
        # DIRECTION DU JOUEUR
        # ---------------------------------------------------------
        self.player.direction_x = direction_x
        self.player.direction_y = direction_y

    # =============================================================
    # FREINAGE
    # =============================================================

    def brake(self):
        """
        Ralentissement progressif.
        """

        self.current_sprint = False

        self.velocity_x *= self.deceleration
        self.velocity_y *= self.deceleration

        if abs(self.velocity_x) < 0.05:
            self.velocity_x = 0.0

        if abs(self.velocity_y) < 0.05:
            self.velocity_y = 0.0

    def stop(self):
        """
        Arrêt immédiat.
        """

        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.current_sprint = False

    # =============================================================
    # MISE À JOUR
    # =============================================================

    def update(self, field):
        """
        Applique la vitesse au joueur et le maintient
        dans les limites du terrain.
        """

        self.player.x += self.velocity_x
        self.player.y += self.velocity_y

        radius = getattr(
            self.player,
            "radius",
            18
        )

        self.player.x = max(
            field.left + radius,
            min(
                field.right - radius,
                self.player.x
            )
        )

        self.player.y = max(
            field.top + radius,
            min(
                field.bottom - radius,
                self.player.y
            )
        )

    # =============================================================
    # VITESSE
    # =============================================================

    def get_speed(self):
        return math.sqrt(
            self.velocity_x * self.velocity_x +
            self.velocity_y * self.velocity_y
        )

    def get_speed_ratio(self):
        """
        Ratio de vitesse entre 0 et 1.
        """

        base_speed = max(
            0.001,
            self.max_speed
        )

        ratio = self.get_speed() / base_speed

        return max(
            0.0,
            min(1.0, ratio)
        )

    def is_moving(self):
        return self.get_speed() > 0.1

    def is_sprinting(self):
        return (
            self.current_sprint and
            self.is_moving()
        )

    # =============================================================
    # RESET
    # =============================================================

    def reset(self):
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.current_sprint = False
