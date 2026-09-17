import math
import random


class GoalkeeperController:

    def __init__(self, player, match):

        self.player = player
        self.match = match

        # ==========================================
        # POSITION DE BASE
        # ==========================================

        self.home_x = player.x
        self.home_y = player.y

        # ==========================================
        # MOUVEMENT
        # ==========================================

        self.move_range_x = 85
        self.move_range_y = 115

        self.normal_speed = 3.8
        self.fast_speed = 6.5

        # ==========================================
        # RÉFLEXES
        # ==========================================

        self.reflexes = 0.82

        # ==========================================
        # SAUVE
        # ==========================================

        self.save_distance = 58.0
        self.catch_distance = 34.0

        self.save_cooldown = 0.0

        # ==========================================
        # PLONGEON
        # ==========================================

        self.diving = False
        self.dive_timer = 0.0
        self.dive_duration = 0.28

        self.dive_speed = 9.0

        self.dive_direction_x = 0.0
        self.dive_direction_y = 0.0

        # ==========================================
        # ANTICIPATION
        # ==========================================

        self.prediction_time = 7.0

        # ==========================================
        # SORTIE
        # ==========================================

        self.rush_distance = 145.0
        self.rush_speed = 4.6

        # ==========================================
        # ÉTAT
        # ==========================================

        self.last_action = "position"
        self.last_save = False

    # ==================================================
    # OUTILS
    # ==================================================

    def distance(self, x1, y1, x2, y2):

        return math.sqrt(
            (x1 - x2) ** 2 +
            (y1 - y2) ** 2
        )

    def distance_to_ball(self):

        return self.distance(
            self.player.x,
            self.player.y,
            self.match.ball_x,
            self.match.ball_y
        )

    def ball_speed(self):

        return math.sqrt(
            self.match.ball_vx ** 2 +
            self.match.ball_vy ** 2
        )

    # ==================================================
    # LIMITES DE LA SURFACE DU GARDIEN
    # ==================================================

    def keep_inside_area(self):

        field = self.match.field

        if self.player.team == "blue":

            min_x = field.left + 18
            max_x = field.left + self.move_range_x

        else:

            min_x = field.right - self.move_range_x
            max_x = field.right - 18

        min_y = field.centery - self.move_range_y
        max_y = field.centery + self.move_range_y

        self.player.x = max(
            min_x,
            min(max_x, self.player.x)
        )

        self.player.y = max(
            min_y,
            min(max_y, self.player.y)
        )

    # ==================================================
    # PRÉDICTION DU BALLON
    # ==================================================

    def predict_ball_position(self):

        field = self.match.field

        predicted_x = (
            self.match.ball_x +
            self.match.ball_vx *
            self.prediction_time
        )

        predicted_y = (
            self.match.ball_y +
            self.match.ball_vy *
            self.prediction_time
        )

        predicted_x = max(
            field.left,
            min(field.right, predicted_x)
        )

        predicted_y = max(
            field.top,
            min(field.bottom, predicted_y)
        )

        return predicted_x, predicted_y

    # ==================================================
    # DIRECTION DE LA BALLE
    # ==================================================

    def ball_coming_toward_goal(self):

        if self.player.team == "blue":

            return self.match.ball_vx < -0.15

        return self.match.ball_vx > 0.15

    # ==================================================
    # POSITION DE BASE
    # ==================================================

    def get_home_position(self):

        field = self.match.field

        if self.player.team == "blue":

            goal_x = field.left + 32

        else:

            goal_x = field.right - 32

        target_y = (
            field.centery +
            (
                self.match.ball_y -
                field.centery
            ) * 0.40
        )

        return goal_x, target_y

    # ==================================================
    # DÉPLACEMENT VERS UNE POSITION
    # ==================================================

    def move_toward(
        self,
        target_x,
        target_y,
        speed
    ):

        dx = target_x - self.player.x
        dy = target_y - self.player.y

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        if distance <= 1.5:

            return

        dx /= distance
        dy /= distance

        self.player.x += dx * speed
        self.player.y += dy * speed

        self.player.direction_x = dx
        self.player.direction_y = dy

    # ==================================================
    # POSITIONNEMENT INTELLIGENT
    # ==================================================

    def position(self):

        field = self.match.field

        ball_x = self.match.ball_x
        ball_y = self.match.ball_y

        # Position de la ligne de but
        if self.player.team == "blue":

            base_x = field.left + 32

        else:

            base_x = field.right - 32

        # Le gardien suit légèrement la hauteur du ballon.
        target_y = (
            field.centery +
            (
                ball_y -
                field.centery
            ) * 0.48
        )

        # Si le ballon arrive rapidement,
        # le gardien se prépare davantage.
        speed = self.normal_speed

        if self.ball_speed() > 9:

            speed = self.fast_speed

        self.move_toward(
            base_x,
            target_y,
            speed
        )

        self.keep_inside_area()

        self.last_action = "position"

    # ==================================================
    # SORTIE DU GARDIEN
    # ==================================================

    def can_rush(self):

        if self.match.ball_owner is not None:

            return False

        distance = self.distance_to_ball()

        if distance > self.rush_distance:

            return False

        # Le gardien ne sort que si le ballon
        # se dirige vers sa zone.
        if not self.ball_coming_toward_goal():

            return False

        return True

    def rush(self):

        ball_x = self.match.ball_x
        ball_y = self.match.ball_y

        self.move_toward(
            ball_x,
            ball_y,
            self.rush_speed
        )

        self.keep_inside_area()

        self.last_action = "rush"

    # ==================================================
    # RÉACTION À UN TIR
    # ==================================================

    def should_attempt_save(self):

        if self.match.ball_owner is not None:

            return False

        if self.save_cooldown > 0:

            return False

        speed = self.ball_speed()

        if speed < 1.5:

            return False

        distance = self.distance_to_ball()

        if distance > self.save_distance:

            return False

        if not self.ball_coming_toward_goal():

            return False

        return True

    # ==================================================
    # PLONGEON
    # ==================================================

    def start_dive(self):

        if self.diving:

            return False

        predicted_x, predicted_y = (
            self.predict_ball_position()
        )

        dx = predicted_x - self.player.x
        dy = predicted_y - self.player.y

        length = math.sqrt(
            dx * dx +
            dy * dy
        )

        if length <= 0:

            return False

        dx /= length
        dy /= length

        self.dive_direction_x = dx
        self.dive_direction_y = dy

        self.diving = True
        self.dive_timer = self.dive_duration

        self.last_action = "dive"

        return True

    def update_dive(self, delta_time):

        if not self.diving:

            return False

        self.player.x += (
            self.dive_direction_x *
            self.dive_speed
        )

        self.player.y += (
            self.dive_direction_y *
            self.dive_speed
        )

        self.dive_timer -= delta_time

        self.keep_inside_area()

        if self.dive_timer <= 0:

            self.diving = False

            self.save_cooldown = 0.45

        return True

    # ==================================================
    # TENTATIVE D'ARRÊT
    # ==================================================

    def try_save(self):

        if not self.should_attempt_save():

            return False

        ball_speed = self.ball_speed()

        # Plus le tir est rapide,
        # plus la réaction devient difficile.
        difficulty_factor = max(
            0.50,
            1.0 - max(
                0.0,
                ball_speed - 8.0
            ) / 30.0
        )

        chance = (
            self.reflexes *
            difficulty_factor
        )

        # Légère amélioration si le gardien
        # est proche de la trajectoire prévue.
        predicted_x, predicted_y = (
            self.predict_ball_position()
        )

        prediction_distance = self.distance(
            self.player.x,
            self.player.y,
            predicted_x,
            predicted_y
        )

        if prediction_distance < 45:

            chance += 0.08

        chance = max(
            0.20,
            min(0.94, chance)
        )

        if random.random() > chance:

            self.start_dive()

            self.last_save = False

            return False

        # Le gardien réussit l'intervention.
        self.start_dive()

        self.match.ball_owner = self.player

        self.match.ball_vx = 0.0
        self.match.ball_vy = 0.0

        (
            self.match.ball_x,
            self.match.ball_y
        ) = self.player.ball_control.update_ball_position(
            self.match.ball_x,
            self.match.ball_y
        )

        self.save_cooldown = 0.80

        self.last_action = "save"
        self.last_save = True

        return True

    # ==================================================
    # RÉCUPÉRATION DU BALLON
    # ==================================================

    def catch_loose_ball(self):

        if self.match.ball_owner is not None:

            return False

        distance = self.distance_to_ball()

        if distance > self.catch_distance:

            return False

        if self.ball_speed() > 7.5:

            return False

        self.match.ball_owner = self.player

        self.match.ball_vx = 0.0
        self.match.ball_vy = 0.0

        (
            self.match.ball_x,
            self.match.ball_y
        ) = self.player.ball_control.update_ball_position(
            self.match.ball_x,
            self.match.ball_y
        )

        self.last_action = "catch"

        return True

    # ==================================================
    # MISE À JOUR PRINCIPALE
    # ==================================================

    def update(self, delta_time):

        self.last_save = False

        # Réduction des cooldowns.
        if self.save_cooldown > 0:

            self.save_cooldown -= delta_time

            if self.save_cooldown < 0:

                self.save_cooldown = 0

        # Le gardien possède déjà le ballon.
        if self.match.ball_owner is self.player:

            self.last_action = "possession"

            return

        # Plongeon en cours.
        if self.diving:

            self.update_dive(delta_time)

            # Une fois le plongeon terminé,
            # le gardien reprend son positionnement.
            return

        # Ballon libre proche.
        if self.catch_loose_ball():

            return

        # Tentative d'arrêt.
        if self.try_save():

            return

        # Sortie du gardien.
        if self.can_rush():

            self.rush()

            return

        # Positionnement normal.
        self.position()

    # ==================================================
    # RÉINITIALISATION
    # ==================================================

    def reset(self):

        self.player.x = self.home_x
        self.player.y = self.home_y

        self.save_cooldown = 0.0

        self.diving = False
        self.dive_timer = 0.0

        self.dive_direction_x = 0.0
        self.dive_direction_y = 0.0

        self.last_action = "position"
        self.last_save = False
