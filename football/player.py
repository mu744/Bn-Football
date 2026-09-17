import math
import pygame

from football.movement import MovementController
from football.ball_control import BallController


class Player:
    """
    Joueur central de BN-Football.

    Cette classe contient uniquement les données et comportements
    fondamentaux du joueur.

    Les systèmes spécialisés (IA, fatigue, dribble, tir, passe,
    tacle, etc.) restent dans leurs propres modules.
    """

    def __init__(self, x, y, team, number=1):
        # ---------------------------------------------------------
        # IDENTITÉ
        # ---------------------------------------------------------
        self.x = float(x)
        self.y = float(y)

        self.team = team
        self.number = number

        self.name = f"Player {number}"
        self.position = "CM"
        self.role = "CM"

        # ---------------------------------------------------------
        # ÉTAT
        # ---------------------------------------------------------
        self.on_pitch = True
        self.is_sprinting = False
        self.has_ball = False

        # ---------------------------------------------------------
        # PHYSIQUE
        # ---------------------------------------------------------
        self.radius = 18

        self.speed = 4.5
        self.acceleration = 0.55
        self.base_speed = self.speed

        self.direction_x = 1 if team == "blue" else -1
        self.direction_y = 0.0

        # ---------------------------------------------------------
        # ENDURANCE
        # ---------------------------------------------------------
        self.stamina = 100.0
        self.max_stamina = 100.0

        # ---------------------------------------------------------
        # CARACTÉRISTIQUES
        # ---------------------------------------------------------
        self.rating = 75

        self.control_rating = 75
        self.heading_rating = 75
        self.volley_rating = 75
        self.passing_rating = 75
        self.shooting_rating = 75
        self.dribbling_rating = 75
        self.defending_rating = 75
        self.physical = 75

        # ---------------------------------------------------------
        # CONTRÔLE
        # ---------------------------------------------------------
        self.movement = MovementController(self)
        self.ball_control = BallController(self)

        # ---------------------------------------------------------
        # ÉTAT INTERNE
        # ---------------------------------------------------------
        self.last_move_x = 0.0
        self.last_move_y = 0.0

    # =============================================================
    # DÉPLACEMENT
    # =============================================================

    def move(self, dx, dy, field, sprint=False):
        """
        Déplace le joueur.

        sprint=True active le sprint et permet au système de fatigue
        de détecter correctement l'effort.
        """

        self.is_sprinting = bool(sprint)

        magnitude = math.sqrt(dx * dx + dy * dy)

        if magnitude <= 0.001:
            self.brake()
            return

        # Normalisation
        dx /= magnitude
        dy /= magnitude

        self.last_move_x = dx
        self.last_move_y = dy

        self.movement.accelerate(
            dx,
            dy,
            sprint=self.is_sprinting
        )

        self.movement.update(field)

    def brake(self):
        """
        Ralentissement progressif.
        """

        self.is_sprinting = False
        self.movement.brake()

    def stop(self):
        """
        Arrêt immédiat.
        """

        self.is_sprinting = False
        self.movement.stop()

    # =============================================================
    # VITESSE
    # =============================================================

    def get_current_speed(self):
        return self.movement.get_speed()

    def get_speed_ratio(self):
        """
        Retourne un ratio entre 0 et 1 représentant la vitesse actuelle.
        """

        current = self.get_current_speed()

        if self.speed <= 0:
            return 0.0

        return max(
            0.0,
            min(1.0, current / self.speed)
        )

    # =============================================================
    # ENDURANCE
    # =============================================================

    def get_stamina_ratio(self):
        if self.max_stamina <= 0:
            return 0.0

        return max(
            0.0,
            min(1.0, self.stamina / self.max_stamina)
        )

    def is_exhausted(self):
        return self.stamina <= 15.0

    # =============================================================
    # DIRECTION
    # =============================================================

    def set_direction(self, dx, dy):
        length = math.sqrt(dx * dx + dy * dy)

        if length <= 0.001:
            return

        self.direction_x = dx / length
        self.direction_y = dy / length

    def get_direction(self):
        return self.direction_x, self.direction_y

    # =============================================================
    # BALLON
    # =============================================================

    def owns_ball(self, match):
        return getattr(match, "ball_owner", None) is self

    def set_ball_state(self, has_ball):
        self.has_ball = bool(has_ball)

    # =============================================================
    # DISTANCE
    # =============================================================

    def distance_to(self, x, y):
        dx = self.x - x
        dy = self.y - y

        return math.sqrt(dx * dx + dy * dy)

    def distance_to_player(self, other):
        if other is None:
            return float("inf")

        return self.distance_to(other.x, other.y)

    # =============================================================
    # UTILITAIRES
    # =============================================================

    def is_active(self):
        return getattr(self, "on_pitch", True)

    def get_team_side(self):
        return self.team

    def get_role(self):
        return getattr(self, "role", self.position)

    def get_rating(self):
        return getattr(self, "rating", 75)

    # =============================================================
    # RESET
    # =============================================================

    def reset_state(self):
        self.is_sprinting = False
        self.has_ball = False
        self.stamina = self.max_stamina

        self.movement.stop()

    # =============================================================
    # AFFICHAGE
    # =============================================================

    def draw(self, screen):
        """
        Affichage temporaire 2D.

        Le renderer 2D/3D pourra remplacer cette partie plus tard
        sans modifier la logique du joueur.
        """

        if not self.on_pitch:
            return

        if self.team == "blue":
            color = (30, 110, 240)
        else:
            color = (220, 60, 70)

        # Joueur
        pygame.draw.circle(
            screen,
            color,
            (int(self.x), int(self.y)),
            self.radius
        )

        # Centre
        pygame.draw.circle(
            screen,
            (245, 245, 245),
            (int(self.x), int(self.y)),
            5
        )

        # Direction
        direction_length = 10

        end_x = (
            self.x +
            self.direction_x * direction_length
        )

        end_y = (
            self.y +
            self.direction_y * direction_length
        )

        pygame.draw.line(
            screen,
            (255, 255, 255),
            (int(self.x), int(self.y)),
            (int(end_x), int(end_y)),
            2
        )

        # Indication sprint
        if self.is_sprinting:
            pygame.draw.circle(
                screen,
                (255, 220, 80),
                (int(self.x), int(self.y)),
                self.radius + 3,
                2
            )
