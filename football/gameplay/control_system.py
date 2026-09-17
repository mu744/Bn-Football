import math


class ControlSystem:

    def __init__(self, match):
        self.match = match

        # Distance maximale pour récupérer le ballon
        self.control_radius = 34.0

        # Distance idéale du ballon devant le joueur
        self.ball_distance = 22.0

        # Force avec laquelle le ballon suit le joueur
        self.follow_strength = 0.38

        # Petite marge pour éviter les récupérations instantanées
        self.recovery_margin = 4.0

    # ==================================================
    # OUTILS
    # ==================================================

    def distance(self, player, x, y):
        return math.sqrt(
            (player.x - x) ** 2 +
            (player.y - y) ** 2
        )

    def get_control_distance(self, player):
        speed = player.get_current_speed()

        # Plus le joueur court vite,
        # plus le ballon est légèrement éloigné.
        extra = min(speed * 1.5, 14.0)

        return self.ball_distance + extra

    # ==================================================
    # POSITION DU BALLON
    # ==================================================

    def get_ball_target(self, player):

        distance = self.get_control_distance(player)

        target_x = (
            player.x +
            player.direction_x * distance
        )

        target_y = (
            player.y +
            player.direction_y * distance
        )

        return target_x, target_y

    def follow_player(self, player):

        target_x, target_y = self.get_ball_target(
            player
        )

        self.match.ball_x += (
            target_x - self.match.ball_x
        ) * self.follow_strength

        self.match.ball_y += (
            target_y - self.match.ball_y
        ) * self.follow_strength

        self.match.ball_vx = 0.0
        self.match.ball_vy = 0.0

    # ==================================================
    # RECUPERATION
    # ==================================================

    def can_take_ball(self, player):

        if self.match.ball_owner is player:
            return False

        distance = self.distance(
            player,
            self.match.ball_x,
            self.match.ball_y
        )

        return distance <= (
            self.control_radius +
            self.recovery_margin
        )

    def take_ball(self, player):

        if not self.can_take_ball(player):
            return False

        self.match.ball_owner = player

        self.match.ball_vx = 0.0
        self.match.ball_vy = 0.0

        self.follow_player(player)

        return True

    # ==================================================
    # CONTROLE
    # ==================================================

    def update(self):

        owner = self.match.ball_owner

        if owner is None:
            return

        # Le propriétaire conserve le ballon
        # tant qu'il reste suffisamment proche.
        distance = self.distance(
            owner,
            self.match.ball_x,
            self.match.ball_y
        )

        max_distance = (
            self.control_radius +
            owner.get_current_speed() * 2.0
        )

        if distance > max_distance:
            self.match.ball_owner = None
            return

        self.follow_player(owner)

    # ==================================================
    # VERIFICATION DE POSSESSION
    # ==================================================

    def check_recovery(self):

        if self.match.ball_owner is not None:
            return

        players = (
            self.match.home_players +
            self.match.away_players
        )

        closest_player = None
        closest_distance = float("inf")

        for player in players:

            distance = self.distance(
                player,
                self.match.ball_x,
                self.match.ball_y
            )

            if distance < closest_distance:
                closest_distance = distance
                closest_player = player

        if closest_player is None:
            return

        if closest_distance <= self.control_radius:

            self.take_ball(
                closest_player
            )
