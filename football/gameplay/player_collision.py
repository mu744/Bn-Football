import math


class PlayerCollision:
    """
    Gestion centrale des collisions entre joueurs.

    Cette version est conçue pour fonctionner avec :
    - 11 joueurs par équipe
    - joueurs remplaçants hors terrain
    - mouvements IA
    - mouvements du joueur contrôlé
    - physique générale du match
    """

    def __init__(self, match):
        self.match = match
        self.enabled = True

        self.minimum_distance = 32.0
        self.push_strength = 0.65

        # Évite que les joueurs restent coincés les uns dans les autres.
        self.max_push_per_frame = 4.0

        # Nombre de passes de résolution par frame.
        self.iterations = 2

    # ---------------------------------------------------------
    # OUTILS
    # ---------------------------------------------------------

    def distance(self, player_a, player_b):
        dx = player_a.x - player_b.x
        dy = player_a.y - player_b.y
        return math.sqrt(dx * dx + dy * dy)

    def is_active(self, player):
        return getattr(player, "on_pitch", True)

    # ---------------------------------------------------------
    # COLLISION ENTRE DEUX JOUEURS
    # ---------------------------------------------------------

    def resolve_pair(self, player_a, player_b):
        if not self.is_active(player_a):
            return False

        if not self.is_active(player_b):
            return False

        dx = player_a.x - player_b.x
        dy = player_a.y - player_b.y

        distance = math.sqrt(dx * dx + dy * dy)

        if distance <= 0.0001:
            dx = 1.0
            dy = 0.0
            distance = 1.0

        if distance >= self.minimum_distance:
            return False

        overlap = self.minimum_distance - distance

        dx /= distance
        dy /= distance

        push = min(
            overlap * self.push_strength,
            self.max_push_per_frame
        )

        # Répartition équilibrée de la poussée.
        half_push = push * 0.5

        player_a.x += dx * half_push
        player_a.y += dy * half_push

        player_b.x -= dx * half_push
        player_b.y -= dy * half_push

        return True

    # ---------------------------------------------------------
    # COLLISION ENTRE ÉQUIPES
    # ---------------------------------------------------------

    def resolve_all_players(self):
        players = (
            self.match.home_players +
            self.match.away_players
        )

        collisions = 0

        for _ in range(self.iterations):

            for i in range(len(players)):
                player_a = players[i]

                if not self.is_active(player_a):
                    continue

                for j in range(i + 1, len(players)):
                    player_b = players[j]

                    if not self.is_active(player_b):
                        continue

                    if self.resolve_pair(player_a, player_b):
                        collisions += 1

        return collisions

    # ---------------------------------------------------------
    # LIMITES DU TERRAIN
    # ---------------------------------------------------------

    def keep_inside_field(self, player):
        if not self.is_active(player):
            return

        field = self.match.field
        radius = getattr(player, "radius", 18)

        player.x = max(
            field.left + radius,
            min(field.right - radius, player.x)
        )

        player.y = max(
            field.top + radius,
            min(field.bottom - radius, player.y)
        )

    def keep_all_players_inside_field(self):
        players = (
            self.match.home_players +
            self.match.away_players
        )

        for player in players:
            self.keep_inside_field(player)

    # ---------------------------------------------------------
    # COLLISION AVEC LA BALLE
    # ---------------------------------------------------------

    def ball_contact(self, player):
        if not self.is_active(player):
            return False

        dx = self.match.ball_x - player.x
        dy = self.match.ball_y - player.y

        distance = math.sqrt(dx * dx + dy * dy)

        contact_distance = getattr(player, "radius", 18) + 8

        return distance <= contact_distance

    # ---------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------

    def update(self):
        if not self.enabled:
            return

        self.resolve_all_players()
        self.keep_all_players_inside_field()

    # ---------------------------------------------------------
    # CONTROLE
    # ---------------------------------------------------------

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def reset(self):
        self.enabled = True
