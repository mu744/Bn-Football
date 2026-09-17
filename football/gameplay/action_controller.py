import math


class ActionController:
    """
    Gestionnaire des actions du joueur contrôlé.

    Il fait le lien entre :
        MobileInput
            ↓
        ActionController
            ↓
        Gameplay / Match

    Actions :
        déplacement
        sprint
        passe
        tir
        tacle
        changement de joueur
    """

    def __init__(self, match):

        self.match = match
        self.enabled = True

        self.selected_player = None

        self.pass_power = 7.0
        self.shot_power = 11.0
        self.tackle_distance = 42.0

        self.action_cooldown = 0.0

    # =========================================================
    # OUTILS
    # =========================================================

    def distance(self, a, b):

        dx = a.x - b.x
        dy = a.y - b.y

        return math.sqrt(
            dx * dx +
            dy * dy
        )

    def get_home_players(self):

        return [
            p for p in self.match.home_players
            if getattr(p, "on_pitch", True)
        ]

    # =========================================================
    # JOUEUR SELECTIONNE
    # =========================================================

    def select_player(self, player):

        if player is None:
            return False

        if not getattr(player, "on_pitch", True):
            return False

        self.selected_player = player

        return True

    def select_nearest_to_ball(self):

        players = self.get_home_players()

        if not players:
            self.selected_player = None
            return None

        closest = None
        best_distance = float("inf")

        for player in players:

            distance = math.sqrt(
                (player.x - self.match.ball_x) ** 2 +
                (player.y - self.match.ball_y) ** 2
            )

            if distance < best_distance:

                best_distance = distance
                closest = player

        self.selected_player = closest

        return closest

    def ensure_selected_player(self):

        if self.selected_player is None:

            return self.select_nearest_to_ball()

        if not getattr(
            self.selected_player,
            "on_pitch",
            True
        ):

            return self.select_nearest_to_ball()

        return self.selected_player

    # =========================================================
    # DEPLACEMENT
    # =========================================================

    def move_selected_player(
        self,
        direction_x,
        direction_y,
        sprint=False
    ):

        player = self.ensure_selected_player()

        if player is None:
            return False

        magnitude = math.sqrt(
            direction_x ** 2 +
            direction_y ** 2
        )

        if magnitude <= 0.05:

            player.brake()

            return False

        direction_x /= magnitude
        direction_y /= magnitude

        player.move(
            direction_x,
            direction_y,
            self.match.field,
            sprint=sprint
        )

        return True

    # =========================================================
    # PASSE
    # =========================================================

    def find_pass_target(self, player):

        teammates = [
            p for p in self.get_home_players()
            if p is not player
        ]

        if not teammates:
            return None

        best = None
        best_score = -999999

        for teammate in teammates:

            dx = teammate.x - player.x
            dy = teammate.y - player.y

            distance = math.sqrt(
                dx * dx +
                dy * dy
            )

            if distance < 30:
                continue

            if distance > 330:
                continue

            score = 0.0

            # Préférence pour l'avant.
            if teammate.x > player.x:
                score += 70

            # Distance idéale.
            score -= abs(
                distance - 130
            ) * 0.35

            # Évite les joueurs trop entourés.
            opponents = self.match.away_players

            nearest_opponent = 9999

            for opponent in opponents:

                if not getattr(
                    opponent,
                    "on_pitch",
                    True
                ):
                    continue

                d = self.distance(
                    teammate,
                    opponent
                )

                nearest_opponent = min(
                    nearest_opponent,
                    d
                )

            score += min(
                nearest_opponent,
                100
            )

            if score > best_score:

                best_score = score
                best = teammate

        return best

    def pass_ball(self):

        player = self.ensure_selected_player()

        if player is None:
            return False

        if self.match.ball_owner is not player:
            return False

        target = self.find_pass_target(
            player
        )

        if target is None:
            return False

        dx = target.x - player.x
        dy = target.y - player.y

        length = math.sqrt(
            dx * dx +
            dy * dy
        )

        if length <= 0:
            return False

        dx /= length
        dy /= length

        physics = getattr(
            self.match,
            "ball_physics",
            None
        )

        if physics is None:
            return False

        physics.pass_ball(
            dx,
            dy,
            self.pass_power
        )

        return True

    # =========================================================
    # TIR
    # =========================================================

    def shoot(self):

        player = self.ensure_selected_player()

        if player is None:
            return False

        if self.match.ball_owner is not player:
            return False

        field = self.match.field

        # But adverse.
        goal_x = field.right + 30
        goal_y = field.centery

        dx = goal_x - player.x
        dy = goal_y - player.y

        length = math.sqrt(
            dx * dx +
            dy * dy
        )

        if length <= 0:
            return False

        dx /= length
        dy /= length

        physics = getattr(
            self.match,
            "ball_physics",
            None
        )

        if physics is None:
            return False

        physics.shot(
            dx,
            dy,
            self.shot_power
        )

        return True

    # =========================================================
    # TACLE
    # =========================================================

    def tackle(self):

        player = self.ensure_selected_player()

        if player is None:
            return False

        closest = None
        best_distance = float("inf")

        for opponent in self.match.away_players:

            if not getattr(
                opponent,
                "on_pitch",
                True
            ):
                continue

            distance = self.distance(
                player,
                opponent
            )

            if distance < best_distance:

                best_distance = distance
                closest = opponent

        if closest is None:
            return False

        if best_distance > self.tackle_distance:
            return False

        # Si l'adversaire possède la balle,
        # on tente de la récupérer.
        if self.match.ball_owner is closest:

            self.match.ball_owner = player

            self.match.ball_x = player.x
            self.match.ball_y = player.y

            self.match.ball_vx = 0.0
            self.match.ball_vy = 0.0

            return True

        # Sinon, on pousse légèrement le joueur adverse.
        dx = closest.x - player.x
        dy = closest.y - player.y

        length = math.sqrt(
            dx * dx +
            dy * dy
        )

        if length <= 0:
            return False

        dx /= length
        dy /= length

        closest.x += dx * 10
        closest.y += dy * 10

        return True

    # =========================================================
    # CHANGEMENT DE JOUEUR
    # =========================================================

    def switch_player(self):

        players = self.get_home_players()

        if not players:
            return None

        if self.selected_player not in players:

            return self.select_nearest_to_ball()

        current_index = players.index(
            self.selected_player
        )

        # Cherche le prochain joueur.
        for offset in range(
            1,
            len(players) + 1
        ):

            index = (
                current_index +
                offset
            ) % len(players)

            candidate = players[index]

            if candidate is not self.selected_player:

                self.selected_player = candidate

                return candidate

        return self.selected_player

    # =========================================================
    # UPDATE
    # =========================================================

    def update(self, delta_time=0.016):

        if not self.enabled:
            return

        self.action_cooldown -= delta_time

        if self.action_cooldown < 0:

            self.action_cooldown = 0

        self.ensure_selected_player()

    # =========================================================
    # CONTROLE
    # =========================================================

    def enable(self):

        self.enabled = True

    def disable(self):

        self.enabled = False

    def reset(self):

        self.selected_player = None
        self.action_cooldown = 0.0
        self.enabled = True
