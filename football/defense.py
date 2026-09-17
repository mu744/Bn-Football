import math
import random


class DefenseController:

    def __init__(self, match):

        self.match = match

        # ==========================================
        # TACLE
        # ==========================================

        self.tackle_distance = 42.0
        self.sliding_tackle_distance = 58.0

        self.tackle_cooldown = 0.0
        self.sliding_cooldown = 0.0

        # ==========================================
        # INTERCEPTION
        # ==========================================

        self.interception_distance = 34.0

        # ==========================================
        # DÉFENSE
        # ==========================================

        self.marking_distance = 115.0
        self.press_distance = 155.0

        self.chase_speed = 3.4
        self.press_speed = 4.0

        # ==========================================
        # TACLE GLISSÉ
        # ==========================================

        self.sliding_duration = 0.32
        self.sliding_timer = 0.0
        self.sliding_player = None

        # ==========================================
        # ÉTAT
        # ==========================================

        self.last_tackler = None
        self.last_action = "position"

    # ==================================================
    # OUTILS
    # ==================================================

    def distance(self, player, x, y):

        return math.sqrt(
            (player.x - x) ** 2 +
            (player.y - y) ** 2
        )

    def distance_players(self, a, b):

        return math.sqrt(
            (a.x - b.x) ** 2 +
            (a.y - b.y) ** 2
        )

    def get_defenders(self, team):

        if team == "blue":
            return self.match.home_players

        return self.match.away_players

    def get_attackers(self, team):

        if team == "blue":
            return self.match.away_players

        return self.match.home_players

    # ==================================================
    # COOLDOWNS
    # ==================================================

    def update(self, delta_time):

        if self.tackle_cooldown > 0:

            self.tackle_cooldown -= delta_time

            if self.tackle_cooldown < 0:
                self.tackle_cooldown = 0

        if self.sliding_cooldown > 0:

            self.sliding_cooldown -= delta_time

            if self.sliding_cooldown < 0:
                self.sliding_cooldown = 0

        if self.sliding_timer > 0:

            self.update_sliding(delta_time)

    # ==================================================
    # JOUEUR LE PLUS PROCHE DU BALLON
    # ==================================================

    def nearest_defender(
        self,
        defenders,
        ball_x,
        ball_y
    ):

        closest = None
        best_distance = float("inf")

        for player in defenders:

            distance = self.distance(
                player,
                ball_x,
                ball_y
            )

            if distance < best_distance:

                best_distance = distance
                closest = player

        return closest

    # ==================================================
    # ADVERSAIRE LE PLUS PROCHE
    # ==================================================

    def nearest_opponent(self, player):

        opponents = self.get_attackers(
            player.team
        )

        closest = None
        best_distance = float("inf")

        for opponent in opponents:

            distance = self.distance_players(
                player,
                opponent
            )

            if distance < best_distance:

                best_distance = distance
                closest = opponent

        return closest, best_distance

    # ==================================================
    # MARQUAGE
    # ==================================================

    def find_marking_target(self, defender):

        opponents = self.get_attackers(
            defender.team
        )

        if not opponents:
            return None

        best_target = None
        best_score = -999999

        for opponent in opponents:

            distance = self.distance_players(
                defender,
                opponent
            )

            score = 0.0

            # Priorité aux joueurs proches.
            score -= distance

            # Priorité au joueur qui possède le ballon.
            if self.match.ball_owner is opponent:

                score += 250

            # Les attaquants sont davantage surveillés.
            if getattr(
                opponent,
                "position",
                ""
            ) == "AT":

                score += 80

            # Un joueur proche du but devient prioritaire.
            field = self.match.field

            if defender.team == "blue":

                goal_distance = (
                    opponent.x -
                    field.left
                )

            else:

                goal_distance = (
                    field.right -
                    opponent.x
                )

            score -= max(
                0,
                goal_distance
            ) * 0.25

            if score > best_score:

                best_score = score
                best_target = opponent

        return best_target

    # ==================================================
    # POSITION DE MARQUAGE
    # ==================================================

    def marking_position(
        self,
        defender,
        attacker
    ):

        if attacker is None:
            return

        field = self.match.field

        # Le défenseur se place entre l'attaquant
        # et son propre but.
        if defender.team == "blue":

            goal_x = field.left

        else:

            goal_x = field.right

        dx = goal_x - attacker.x
        dy = field.centery - attacker.y

        length = math.sqrt(
            dx * dx +
            dy * dy
        )

        if length <= 0:
            return

        dx /= length
        dy /= length

        target_x = (
            attacker.x +
            dx * 42
        )

        target_y = (
            attacker.y +
            dy * 42
        )

        return target_x, target_y

    # ==================================================
    # DÉPLACEMENT DÉFENSIF
    # ==================================================

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

        if length <= 1.5:
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
    # PRESSION SUR LE PORTEUR
    # ==================================================

    def pressure(
        self,
        defenders,
        ball_x,
        ball_y
    ):

        defender = self.nearest_defender(
            defenders,
            ball_x,
            ball_y
        )

        if defender is None:
            return None

        distance = self.distance(
            defender,
            ball_x,
            ball_y
        )

        if distance > self.press_distance:
            return defender

        self.move_toward(
            defender,
            ball_x,
            ball_y,
            self.press_speed
        )

        self.last_action = "press"

        return defender

    # ==================================================
    # REPLACEMENT DÉFENSIF
    # ==================================================

    def defensive_position(
        self,
        defender
    ):

        field = self.match.field

        if defender.team == "blue":

            target_x = (
                field.left +
                field.width * 0.28
            )

        else:

            target_x = (
                field.right -
                field.width * 0.28
            )

        target_y = (
            field.centery +
            (
                self.match.ball_y -
                field.centery
            ) * 0.35
        )

        self.move_toward(
            defender,
            target_x,
            target_y,
            2.4
        )

        self.last_action = "reposition"

    # ==================================================
    # TACLE DEBOUT
    # ==================================================

    def can_tackle(self):

        return self.tackle_cooldown <= 0

    def tackle(self, defender):

        if defender is None:
            return False

        if not self.can_tackle():
            return False

        owner = self.match.ball_owner

        if owner is None:
            return False

        if owner.team == defender.team:
            return False

        distance = self.distance_players(
            defender,
            owner
        )

        if distance > self.tackle_distance:
            return False

        chance = 0.70

        # Approche rapide.
        if defender.get_current_speed() > 4:

            chance += 0.08

        # Très proche = meilleure précision.
        if distance < 25:

            chance += 0.10

        # Évite un taux de réussite absolu.
        chance = max(
            0.20,
            min(0.90, chance)
        )

        self.tackle_cooldown = 0.55
        self.last_tackler = defender

        if random.random() <= chance:

            self.match.ball_owner = defender

            self.match.ball_vx = 0.0
            self.match.ball_vy = 0.0

            (
                self.match.ball_x,
                self.match.ball_y
            ) = defender.ball_control.update_ball_position(
                self.match.ball_x,
                self.match.ball_y
            )

            self.last_action = "tackle"

            return True

        self.last_action = "missed_tackle"

        return False

    # ==================================================
    # TACLE GLISSÉ
    # ==================================================

    def sliding_tackle(self, defender):

        if defender is None:
            return False

        if self.sliding_cooldown > 0:
            return False

        owner = self.match.ball_owner

        if owner is None:
            return False

        if owner.team == defender.team:
            return False

        distance = self.distance_players(
            defender,
            owner
        )

        if distance > self.sliding_tackle_distance:
            return False

        dx = owner.x - defender.x
        dy = owner.y - defender.y

        length = math.sqrt(
            dx * dx +
            dy * dy
        )

        if length <= 0:
            return False

        dx /= length
        dy /= length

        self.sliding_player = defender
        self.sliding_timer = self.sliding_duration

        defender.direction_x = dx
        defender.direction_y = dy

        self.sliding_cooldown = 1.0
        self.last_tackler = defender

        # Une glissade a moins de précision
        # qu'un tacle debout.
        chance = 0.58

        if distance < 30:

            chance += 0.12

        success = random.random() <= chance

        if success:

            self.match.ball_owner = defender

            self.match.ball_vx = 0.0
            self.match.ball_vy = 0.0

            (
                self.match.ball_x,
                self.match.ball_y
            ) = defender.ball_control.update_ball_position(
                self.match.ball_x,
                self.match.ball_y
            )

            self.last_action = "sliding_tackle"

            return True

        self.last_action = "sliding_miss"

        return False

    # ==================================================
    # MOUVEMENT DU TACLE GLISSÉ
    # ==================================================

    def update_sliding(self, delta_time):

        if self.sliding_player is None:

            self.sliding_timer = 0

            return

        player = self.sliding_player

        speed = 7.5

        player.x += (
            player.direction_x *
            speed
        )

        player.y += (
            player.direction_y *
            speed
        )

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

        self.sliding_timer -= delta_time

        if self.sliding_timer <= 0:

            self.sliding_timer = 0
            self.sliding_player = None

    # ==================================================
    # INTERCEPTION
    # ==================================================

    def try_interception(self, defender):

        if defender is None:
            return False

        if self.match.ball_owner is not None:
            return False

        distance = self.distance(
            defender,
            self.match.ball_x,
            self.match.ball_y
        )

        if distance > self.interception_distance:
            return False

        chance = 0.68

        if random.random() > chance:
            return False

        self.match.ball_owner = defender

        self.match.ball_vx = 0.0
        self.match.ball_vy = 0.0

        (
            self.match.ball_x,
            self.match.ball_y
        ) = defender.ball_control.update_ball_position(
            self.match.ball_x,
            self.match.ball_y
        )

        self.last_tackler = defender
        self.last_action = "interception"

        return True

    # ==================================================
    # DÉFENSE AUTOMATIQUE
    # ==================================================

    def update_defender(self, defender):

        if defender is None:
            return

        # Si le défenseur possède le ballon,
        # il ne défend plus.
        if self.match.ball_owner is defender:
            return

        ball_x = self.match.ball_x
        ball_y = self.match.ball_y

        distance = self.distance(
            defender,
            ball_x,
            ball_y
        )

        # Ballon très proche.
        if distance <= self.tackle_distance:

            if self.match.ball_owner is not None:

                owner = self.match.ball_owner

                if owner.team != defender.team:

                    self.tackle(defender)

                    return

        # Ballon libre.
        if self.match.ball_owner is None:

            if self.try_interception(defender):

                return

        # Marquage.
        target = self.find_marking_target(
            defender
        )

        if target is not None:

            target_distance = (
                self.distance_players(
                    defender,
                    target
                )
            )

            if target_distance <= self.marking_distance:

                position = self.marking_position(
                    defender,
                    target
                )

                if position is not None:

                    self.move_toward(
                        defender,
                        position[0],
                        position[1],
                        self.chase_speed
                    )

                    self.last_action = "marking"

                    return

        # Sinon replacement.
        self.defensive_position(
            defender
        )

    # ==================================================
    # RÉINITIALISATION
    # ==================================================

    def reset(self):

        self.tackle_cooldown = 0.0
        self.sliding_cooldown = 0.0

        self.sliding_timer = 0.0
        self.sliding_player = None

        self.last_tackler = None
        self.last_action = "position"
