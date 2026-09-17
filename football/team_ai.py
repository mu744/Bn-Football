import math
import random


class TeamAI:

    def __init__(self, match):

        self.match = match

        # Vitesse générale des déplacements IA.
        self.base_speed = 2.2
        self.chase_speed = 3.2
        self.press_speed = 3.7

        # Distances de comportement.
        self.support_distance = 150.0
        self.defensive_distance = 180.0
        self.press_distance = 145.0

        self.enabled = True

    # ==================================================
    # OUTILS
    # ==================================================

    def distance(self, a, b):

        return math.sqrt(
            (a.x - b.x) ** 2 +
            (a.y - b.y) ** 2
        )

    def move_toward(
        self,
        player,
        target_x,
        target_y,
        speed
    ):

        dx = target_x - player.x
        dy = target_y - player.y

        length = math.sqrt(
            dx * dx +
            dy * dy
        )

        if length <= 2:
            return

        dx /= length
        dy /= length

        player.x += dx * speed
        player.y += dy * speed

        player.direction_x = dx
        player.direction_y = dy

        field = self.match.field

        player.x = max(
            field.left + player.radius,
            min(
                field.right - player.radius,
                player.x
            )
        )

        player.y = max(
            field.top + player.radius,
            min(
                field.bottom - player.radius,
                player.y
            )
        )

    # ==================================================
    # ÉQUIPE
    # ==================================================

    def get_team_players(self, team):

        if team == "blue":
            return self.match.home_players

        return self.match.away_players

    def get_opponents(self, team):

        if team == "blue":
            return self.match.away_players

        return self.match.home_players

    # ==================================================
    # JOUEUR LE PLUS PROCHE DU BALLON
    # ==================================================

    def nearest_player(
        self,
        players,
        x,
        y
    ):

        closest = None
        best_distance = float("inf")

        for player in players:

            d = math.sqrt(
                (player.x - x) ** 2 +
                (player.y - y) ** 2
            )

            if d < best_distance:

                best_distance = d
                closest = player

        return closest

    # ==================================================
    # PORTEUR DU BALLON
    # ==================================================

    def ball_owner(self, team):

        owner = self.match.ball_owner

        if owner is not None:
            return owner

        return None

    # ==================================================
    # DÉPLACEMENT OFFENSIF
    # ==================================================

    def offensive_movement(self, player):

        owner = self.match.ball_owner

        if owner is None:
            return

        if owner.team != player.team:
            return

        # Le porteur ne cherche pas son propre soutien.
        if owner is player:
            return

        distance = self.distance(
            player,
            owner
        )

        # Les joueurs trop éloignés se rapprochent.
        if distance > self.support_distance:

            self.move_toward(
                player,
                owner.x,
                owner.y,
                self.base_speed
            )

            return

        # Les attaquants cherchent progressivement
        # à avancer.
        position = getattr(
            player,
            "position",
            ""
        )

        if position == "AT":

            if player.team == "blue":

                target_x = player.x + 25

            else:

                target_x = player.x - 25

            self.move_toward(
                player,
                target_x,
                player.y,
                self.base_speed
            )

            return

        # Milieux : soutien autour du porteur.
        if position == "MC":

            offset = (
                -45
                if player.y < owner.y
                else 45
            )

            target_x = owner.x

            target_y = owner.y + offset

            self.move_toward(
                player,
                target_x,
                target_y,
                self.base_speed
            )

    # ==================================================
    # DÉPLACEMENT DÉFENSIF
    # ==================================================

    def defensive_movement(self, player):

        owner = self.match.ball_owner

        opponents = self.get_opponents(
            player.team
        )

        # ------------------------------------------
        # BALLON CHEZ UN ADVERSAIRE
        # ------------------------------------------

        if owner is not None:

            if owner.team != player.team:

                distance = self.distance(
                    player,
                    owner
                )

                # Le joueur le plus proche presse.
                nearest = self.nearest_player(
                    self.get_team_players(
                        player.team
                    ),
                    owner.x,
                    owner.y
                )

                if nearest is player:

                    if distance <= self.press_distance:

                        self.move_toward(
                            player,
                            owner.x,
                            owner.y,
                            self.press_speed
                        )

                        return

                # Les autres joueurs couvrent.
                target = self.find_marking_target(
                    player,
                    opponents
                )

                if target is not None:

                    self.move_toward(
                        player,
                        target.x,
                        target.y,
                        self.base_speed
                    )

                    return

        # ------------------------------------------
        # BALLON LIBRE
        # ------------------------------------------

        if owner is None:

            distance = self.distance(
                player,
                self.match.ball_x,
                self.match.ball_y
            )

            nearest = self.nearest_player(
                self.get_team_players(
                    player.team
                ),
                self.match.ball_x,
                self.match.ball_y
            )

            if nearest is player:

                if distance < self.defensive_distance:

                    self.move_toward(
                        player,
                        self.match.ball_x,
                        self.match.ball_y,
                        self.chase_speed
                    )

                    return

        # Sinon replacement.
        self.reposition(player)

    # ==================================================
    # CIBLE DE MARQUAGE
    # ==================================================

    def find_marking_target(
        self,
        defender,
        opponents
    ):

        best = None
        best_score = -999999

        for opponent in opponents:

            distance = self.distance(
                defender,
                opponent
            )

            score = -distance

            position = getattr(
                opponent,
                "position",
                ""
            )

            if position == "AT":

                score += 60

            if self.match.ball_owner is opponent:

                score += 180

            if score > best_score:

                best_score = score
                best = opponent

        return best

    # ==================================================
    # REPLACEMENT
    # ==================================================

    def reposition(self, player):

        field = self.match.field

        # Position générale basée sur l'équipe.
        if player.team == "blue":

            center_x = (
                field.left +
                field.width * 0.34
            )

        else:

            center_x = (
                field.right -
                field.width * 0.34
            )

        center_y = (
            field.centery +
            (
                self.match.ball_y -
                field.centery
            ) * 0.30
        )

        # Chaque joueur garde une légère séparation
        # grâce à sa position actuelle.
        target_x = (
            center_x +
            (player.x - center_x) * 0.55
        )

        target_y = (
            center_y +
            (player.y - center_y) * 0.55
        )

        self.move_toward(
            player,
            target_x,
            target_y,
            self.base_speed * 0.65
        )

    # ==================================================
    # ÉVITER LES COLLISIONS ENTRE COÉQUIPIERS
    # ==================================================

    def avoid_teammates(self, player):

        teammates = self.get_team_players(
            player.team
        )

        for teammate in teammates:

            if teammate is player:
                continue

            dx = player.x - teammate.x
            dy = player.y - teammate.y

            distance = math.sqrt(
                dx * dx +
                dy * dy
            )

            if distance <= 34 and distance > 0:

                dx /= distance
                dy /= distance

                player.x += dx * 0.8
                player.y += dy * 0.8

    # ==================================================
    # APPEL EN PROFONDEUR
    # ==================================================

    def make_run(self, player):

        owner = self.match.ball_owner

        if owner is None:
            return

        if owner.team != player.team:
            return

        position = getattr(
            player,
            "position",
            ""
        )

        if position != "AT":
            return

        # Direction du but adverse.
        if player.team == "blue":

            target_x = (
                player.x + 55
            )

        else:

            target_x = (
                player.x - 55
            )

        # Variation verticale pour éviter
        # que tous les joueurs courent pareil.
        variation = random.choice(
            [-35, 0, 35]
        )

        target_y = (
            player.y + variation
        )

        self.move_toward(
            player,
            target_x,
            target_y,
            self.chase_speed
        )

    # ==================================================
    # DÉCISION D'UN JOUEUR
    # ==================================================

    def update_player(self, player):

        if player is None:
            return

        # Gardien géré par son propre système.
        if getattr(
            player,
            "position",
            ""
        ) == "GK":

            return

        owner = self.match.ball_owner

        # ------------------------------------------
        # POSSESSION DE SON ÉQUIPE
        # ------------------------------------------

        if owner is not None:

            if owner.team == player.team:

                self.offensive_movement(
                    player
                )

                self.make_run(
                    player
                )

            else:

                self.defensive_movement(
                    player
                )

        # ------------------------------------------
        # BALLON LIBRE
        # ------------------------------------------

        else:

            self.defensive_movement(
                player
            )

        self.avoid_teammates(
            player
        )

    # ==================================================
    # MISE À JOUR DES DEUX ÉQUIPES
    # ==================================================

    def update(self):

        if not self.enabled:
            return

        for player in self.match.home_players:

            self.update_player(
                player
            )

        for player in self.match.away_players:

            self.update_player(
                player
            )

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

        self.enabled = True
