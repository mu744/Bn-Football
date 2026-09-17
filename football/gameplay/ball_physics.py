import math


class BallPhysics:

    def __init__(self, match):

        self.match = match

        self.friction = 0.965
        self.air_resistance = 0.998
        self.min_speed = 0.08

        self.max_speed = 16.0

        self.spin_x = 0.0
        self.spin_y = 0.0

        self.bounce_factor = 0.72

        self.ground_bounce = True

    # ==================================================
    # OUTILS
    # ==================================================

    def speed(self):

        return math.sqrt(
            self.match.ball_vx ** 2 +
            self.match.ball_vy ** 2
        )

    def normalize(self, x, y):

        length = math.sqrt(
            x * x +
            y * y
        )

        if length <= 0:
            return 0.0, 0.0

        return (
            x / length,
            y / length
        )

    # ==================================================
    # FRAPPE
    # ==================================================

    def kick(
        self,
        direction_x,
        direction_y,
        power,
        spin_x=0.0,
        spin_y=0.0
    ):

        direction_x, direction_y = self.normalize(
            direction_x,
            direction_y
        )

        power = max(
            0.0,
            min(
                power,
                self.max_speed
            )
        )

        self.match.ball_vx = (
            direction_x * power
        )

        self.match.ball_vy = (
            direction_y * power
        )

        self.spin_x = spin_x
        self.spin_y = spin_y

        self.match.ball_owner = None

    # ==================================================
    # PASSE
    # ==================================================

    def pass_ball(
        self,
        direction_x,
        direction_y,
        power=7.0
    ):

        self.kick(
            direction_x,
            direction_y,
            power
        )

    # ==================================================
    # TIR
    # ==================================================

    def shot(
        self,
        direction_x,
        direction_y,
        power=11.0,
        spin=0.0
    ):

        self.kick(
            direction_x,
            direction_y,
            power,
            spin,
            0.0
        )

    # ==================================================
    # SPIN / EFFET
    # ==================================================

    def apply_spin(self):

        if abs(self.spin_x) < 0.001:
            if abs(self.spin_y) < 0.001:
                return

        vx = self.match.ball_vx
        vy = self.match.ball_vy

        self.match.ball_vx += (
            -vy * self.spin_x * 0.012
        )

        self.match.ball_vy += (
            vx * self.spin_y * 0.012
        )

        self.spin_x *= 0.985
        self.spin_y *= 0.985

    # ==================================================
    # LIMITATION DE VITESSE
    # ==================================================

    def limit_speed(self):

        speed = self.speed()

        if speed <= self.max_speed:
            return

        factor = (
            self.max_speed /
            speed
        )

        self.match.ball_vx *= factor
        self.match.ball_vy *= factor

    # ==================================================
    # FROTTEMENT
    # ==================================================

    def apply_friction(self):

        self.match.ball_vx *= (
            self.friction
        )

        self.match.ball_vy *= (
            self.friction
        )

        if self.speed() < self.min_speed:

            self.match.ball_vx = 0.0
            self.match.ball_vy = 0.0

    # ==================================================
    # REBOND SUR LES LIGNES
    # ==================================================

    def bounce_from_field(self):

        field = self.match.field

        radius = 7

        # gauche
        if self.match.ball_x < field.left:

            self.match.ball_x = field.left

            if self.match.ball_vx < 0:
                self.match.ball_vx *= (
                    -self.bounce_factor
                )

        # droite
        if self.match.ball_x > field.right:

            self.match.ball_x = field.right

            if self.match.ball_vx > 0:
                self.match.ball_vx *= (
                    -self.bounce_factor
                )

        # haut
        if self.match.ball_y < field.top:

            self.match.ball_y = (
                field.top + radius
            )

            if self.match.ball_vy < 0:
                self.match.ball_vy *= (
                    -self.bounce_factor
                )

        # bas
        if self.match.ball_y > field.bottom:

            self.match.ball_y = (
                field.bottom - radius
            )

            if self.match.ball_vy > 0:
                self.match.ball_vy *= (
                    -self.bounce_factor
                )

    # ==================================================
    # COLLISION AVEC UN JOUEUR
    # ==================================================

    def player_collision(self, player):

        if player is None:
            return False

        dx = (
            self.match.ball_x -
            player.x
        )

        dy = (
            self.match.ball_y -
            player.y
        )

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        collision_distance = (
            player.radius + 8
        )

        if distance > collision_distance:
            return False

        if distance <= 0:
            dx = 1.0
            dy = 0.0
            distance = 1.0

        dx /= distance
        dy /= distance

        self.match.ball_x = (
            player.x +
            dx * collision_distance
        )

        self.match.ball_y = (
            player.y +
            dy * collision_distance
        )

        velocity = self.speed()

        if velocity < 1.0:
            velocity = 1.0

        self.match.ball_vx = (
            dx * velocity * 0.55
        )

        self.match.ball_vy = (
            dy * velocity * 0.55
        )

        return True

    # ==================================================
    # COLLISIONS
    # ==================================================

    def check_player_collisions(self):

        if self.match.ball_owner is not None:
            return

        players = (
            self.match.home_players +
            self.match.away_players
        )

        closest = None
        closest_distance = float("inf")

        for player in players:

            if not getattr(
                player,
                "on_pitch",
                True
            ):
                continue

            dx = (
                self.match.ball_x -
                player.x
            )

            dy = (
                self.match.ball_y -
                player.y
            )

            distance = math.sqrt(
                dx * dx +
                dy * dy
            )

            if distance < closest_distance:

                closest_distance = distance
                closest = player

        if closest is not None:

            self.player_collision(
                closest
            )

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        if self.match.ball_owner is not None:
            return

        self.apply_spin()

        self.match.ball_x += (
            self.match.ball_vx
        )

        self.match.ball_y += (
            self.match.ball_vy
        )

        self.bounce_from_field()

        self.limit_speed()

        self.match.ball_vx *= (
            self.air_resistance
        )

        self.match.ball_vy *= (
            self.air_resistance
        )

        self.apply_friction()

        self.check_player_collisions()

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        self.match.ball_vx = 0.0
        self.match.ball_vy = 0.0

        self.spin_x = 0.0
        self.spin_y = 0.0
