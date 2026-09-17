import math


class CollisionSystem:

    def __init__(self, match):

        self.match = match

        # Distances générales
        self.ball_collision_distance = 28.0
        self.player_collision_distance = 34.0
        self.hard_collision_distance = 24.0

        # Forces
        self.separation_strength = 0.65
        self.opponent_push_strength = 0.35
        self.ball_deflection_strength = 1.5

        # Limitation des impacts
        self.collision_cooldown = 0.12
        self.player_cooldowns = {}

        # Protection
        self.protection_distance = 42.0

        self.enabled = True

    # ==================================================
    # DISTANCE
    # ==================================================

    def distance(self, a, b):

        return math.sqrt(
            (a.x - b.x) ** 2 +
            (a.y - b.y) ** 2
        )

    def distance_to_ball(self, player):

        return math.sqrt(
            (player.x - self.match.ball_x) ** 2 +
            (player.y - self.match.ball_y) ** 2
        )

    # ==================================================
    # NORMALISATION
    # ==================================================

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
    # COOLDOWN
    # ==================================================

    def get_cooldown_key(self, a, b):

        return tuple(
            sorted(
                (id(a), id(b))
            )
        )

    def can_collide(self, a, b):

        key = self.get_cooldown_key(
            a,
            b
        )

        return (
            self.player_cooldowns.get(
                key,
                0.0
            ) <= 0
        )

    def start_cooldown(self, a, b):

        key = self.get_cooldown_key(
            a,
            b
        )

        self.player_cooldowns[key] = (
            self.collision_cooldown
        )

    # ==================================================
    # JOUEUR ↔ BALLON
    # ==================================================

    def ball_collision(self, player):

        if player is None:
            return False

        if not getattr(
            player,
            "on_pitch",
            True
        ):
            return False

        distance = self.distance_to_ball(
            player
        )

        if distance > self.ball_collision_distance:
            return False

        # Si le joueur possède déjà le ballon,
        # aucune collision supplémentaire.
        if self.match.ball_owner is player:
            return False

        # Si le ballon arrive rapidement,
        # on peut le dévier.
        ball_speed = math.sqrt(
            self.match.ball_vx ** 2 +
            self.match.ball_vy ** 2
        )

        if ball_speed > 1.0:

            dx = player.x - self.match.ball_x
            dy = player.y - self.match.ball_y

            nx, ny = self.normalize(
                dx,
                dy
            )

            # Contact avec le ballon.
            self.match.ball_vx += (
                nx *
                self.ball_deflection_strength
            )

            self.match.ball_vy += (
                ny *
                self.ball_deflection_strength
            )

        # Récupération si suffisamment proche.
        if distance <= 22.0:

            self.match.ball_owner = player

            self.match.ball_vx = 0.0
            self.match.ball_vy = 0.0

            self.match.ball_x = (
                player.x +
                player.direction_x * 20
            )

            self.match.ball_y = (
                player.y +
                player.direction_y * 20
            )

            return True

        return False

    # ==================================================
    # SÉPARATION DES JOUEURS
    # ==================================================

    def separate_players(
        self,
        player_a,
        player_b
    ):

        dx = player_a.x - player_b.x
        dy = player_a.y - player_b.y

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        if distance <= 0:

            dx = 1.0
            dy = 0.0
            distance = 1.0

        if distance >= (
            self.player_collision_distance
        ):
            return False

        nx = dx / distance
        ny = dy / distance

        overlap = (
            self.player_collision_distance -
            distance
        )

        push = overlap * 0.5

        player_a.x += nx * push
        player_a.y += ny * push

        player_b.x -= nx * push
        player_b.y -= ny * push

        return True

    # ==================================================
    # JOUEUR ↔ JOUEUR
    # ==================================================

    def player_collision(
        self,
        player_a,
        player_b
    ):

        if player_a is None:
            return False

        if player_b is None:
            return False

        if player_a is player_b:
            return False

        if not getattr(
            player_a,
            "on_pitch",
            True
        ):
            return False

        if not getattr(
            player_b,
            "on_pitch",
            True
        ):
            return False

        if not self.can_collide(
            player_a,
            player_b
        ):
            return False

        distance = self.distance(
            player_a,
            player_b
        )

        if distance > (
            self.player_collision_distance
        ):
            return False

        self.separate_players(
            player_a,
            player_b
        )

        self.start_cooldown(
            player_a,
            player_b
        )

        # Même équipe :
        # simple séparation.
        if player_a.team == player_b.team:

            return True

        # Adversaires :
        # contact physique léger.
        dx = player_a.x - player_b.x
        dy = player_a.y - player_b.y

        nx, ny = self.normalize(
            dx,
            dy
        )

        speed_a = player_a.get_current_speed()
        speed_b = player_b.get_current_speed()

        impact = (
            speed_a +
            speed_b
        ) * 0.5

        force = min(
            impact *
            self.opponent_push_strength,
            3.0
        )

        player_a.x += nx * force
        player_a.y += ny * force

        player_b.x -= nx * force
        player_b.y -= ny * force

        # Si un adversaire possède le ballon,
        # le contact peut provoquer une perte.
        self.handle_ball_contact(
            player_a,
            player_b,
            impact
        )

        return True

    # ==================================================
    # CONTACT AVEC LE PORTEUR
    # ==================================================

    def handle_ball_contact(
        self,
        player_a,
        player_b,
        impact
    ):

        owner = self.match.ball_owner

        if owner is None:
            return

        if (
            owner is not player_a and
            owner is not player_b
        ):
            return

        if owner is player_a:

            attacker = player_a
            defender = player_b

        else:

            attacker = player_b
            defender = player_a

        # Protection du ballon.
        protecting = getattr(
            attacker,
            "protecting",
            False
        )

        if protecting:
            return

        distance = self.distance(
            attacker,
            defender
        )

        if distance > (
            self.protection_distance
        ):
            return

        # Plus l'impact est fort,
        # plus le ballon risque d'être perdu.
        loss_chance = 0.05

        loss_chance += min(
            impact * 0.025,
            0.25
        )

        # Les joueurs très rapides
        # sont légèrement plus exposés.
        if defender.get_current_speed() > 4.0:

            loss_chance += 0.08

        import random

        if random.random() < loss_chance:

            self.lose_ball(
                attacker,
                defender
            )

    # ==================================================
    # PERTE DU BALLON
    # ==================================================

    def lose_ball(
        self,
        attacker,
        defender
    ):

        if self.match.ball_owner is not attacker:
            return False

        dx = (
            defender.x -
            attacker.x
        )

        dy = (
            defender.y -
            attacker.y
        )

        nx, ny = self.normalize(
            dx,
            dy
        )

        self.match.ball_owner = None

        self.match.ball_x = (
            attacker.x +
            attacker.direction_x * 18
        )

        self.match.ball_y = (
            attacker.y +
            attacker.direction_y * 18
        )

        self.match.ball_vx = (
            nx * 2.5
        )

        self.match.ball_vy = (
            ny * 2.5
        )

        return True

    # ==================================================
    # LIMITES DU TERRAIN
    # ==================================================

    def keep_players_inside_field(self):

        field = self.match.field

        players = (
            self.match.home_players +
            self.match.away_players
        )

        for player in players:

            if not getattr(
                player,
                "on_pitch",
                True
            ):
                continue

            radius = getattr(
                player,
                "radius",
                18
            )

            player.x = max(
                field.left + radius,
                min(
                    field.right - radius,
                    player.x
                )
            )

            player.y = max(
                field.top + radius,
                min(
                    field.bottom - radius,
                    player.y
                )
            )

    # ==================================================
    # TOUTES LES COLLISIONS
    # ==================================================

    def update_player_collisions(self):

        players = (
            self.match.home_players +
            self.match.away_players
        )

        active_players = [
            player
            for player in players
            if getattr(
                player,
                "on_pitch",
                True
            )
        ]

        for index in range(
            len(active_players)
        ):

            player_a = (
                active_players[index]
            )

            for other_index in range(
                index + 1,
                len(active_players)
            ):

                player_b = (
                    active_players[
                        other_index
                    ]
                )

                self.player_collision(
                    player_a,
                    player_b
                )

    def update_ball_collisions(self):

        players = (
            self.match.home_players +
            self.match.away_players
        )

        for player in players:

            if not getattr(
                player,
                "on_pitch",
                True
            ):
                continue

            if self.ball_collision(
                player
            ):
                break

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self, delta_time):

        if not self.enabled:
            return

        # Réduction des cooldowns.
        expired = []

        for key, value in (
            self.player_cooldowns.items()
        ):

            value -= delta_time

            if value <= 0:

                expired.append(key)

            else:

                self.player_cooldowns[key] = value

        for key in expired:

            del self.player_cooldowns[key]

        # Joueur ↔ joueur.
        self.update_player_collisions()

        # Joueur ↔ ballon.
        self.update_ball_collisions()

        # Terrain.
        self.keep_players_inside_field()

    # ==================================================
    # ACTIVATION
    # ==================================================

    def enable(self):

        self.enabled = True

    def disable(self):

        self.enabled = False

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        self.player_cooldowns.clear()
