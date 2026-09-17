import math


class BallController:

    def __init__(self, player):

        self.player = player

        # Distance normale du ballon
        self.control_distance = 20.0

        # Distance maximale lors d'une accélération
        self.max_touch_distance = 34.0

        # Vitesse à laquelle le ballon rejoint sa position
        self.follow_strength = 0.32

        # Qualité de contrôle
        self.control_rating = 75

    # ==========================================
    # POSITION CIBLE DU BALLON
    # ==========================================

    def get_target_position(self):

        player = self.player

        speed = player.get_current_speed()

        # Plus le joueur va vite,
        # plus la touche de balle s'allonge
        extra_distance = min(
            speed * 1.8,
            self.max_touch_distance - self.control_distance
        )

        distance = (
            self.control_distance +
            extra_distance
        )

        target_x = (
            player.x +
            player.direction_x * distance
        )

        target_y = (
            player.y +
            player.direction_y * distance
        )

        return target_x, target_y

    # ==========================================
    # POSITIONNER LE BALLON
    # ==========================================

    def update_ball_position(
        self,
        ball_x,
        ball_y
    ):

        target_x, target_y = (
            self.get_target_position()
        )

        # Mouvement progressif vers la cible
        ball_x += (
            target_x - ball_x
        ) * self.follow_strength

        ball_y += (
            target_y - ball_y
        ) * self.follow_strength

        return ball_x, ball_y

    # ==========================================
    # DISTANCE JOUEUR / BALLON
    # ==========================================

    def distance_to_ball(
        self,
        ball_x,
        ball_y
    ):

        return math.sqrt(
            (self.player.x - ball_x) ** 2 +
            (self.player.y - ball_y) ** 2
        )

    # ==========================================
    # PERTE DE CONTROLE
    # ==========================================

    def has_lost_control(
        self,
        ball_x,
        ball_y
    ):

        distance = self.distance_to_ball(
            ball_x,
            ball_y
        )

        # Plus le joueur va vite,
        # plus il peut laisser le ballon partir
        limit = (
            self.max_touch_distance +
            self.player.get_current_speed() * 2
        )

        return distance > limit

    # ==========================================
    # REPRISE DU CONTROLE
    # ==========================================

    def can_control(
        self,
        ball_x,
        ball_y
    ):

        return (
            self.distance_to_ball(
                ball_x,
                ball_y
            ) <= 32
        )
