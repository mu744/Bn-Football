import math


class SetPieceSystem:

    TYPES = (
        "free_kick",
        "penalty",
        "corner",
        "throw_in",
        "goal_kick"
    )

    def __init__(self, match):

        self.match = match

        self.active = False
        self.piece_type = None

        self.team = None
        self.player = None

        self.position_x = 0.0
        self.position_y = 0.0

        self.target_x = 0.0
        self.target_y = 0.0

        self.power = 0.0
        self.spin = 0.0

        self.wall_distance = 80.0
        self.wall_players = []

    # ==================================================
    # DÉMARRER UN COUP DE PIED ARRÊTÉ
    # ==================================================

    def start(
        self,
        piece_type,
        team,
        x,
        y,
        player=None
    ):

        if piece_type not in self.TYPES:
            return False

        self.active = True
        self.piece_type = piece_type
        self.team = team
        self.player = player

        self.position_x = float(x)
        self.position_y = float(y)

        self.target_x = float(x)
        self.target_y = float(y)

        self.power = 0.0
        self.spin = 0.0

        self.wall_players = []

        return True

    # ==================================================
    # POSITION DU BALLON
    # ==================================================

    def set_position(self, x, y):

        self.position_x = float(x)
        self.position_y = float(y)

        self.match.ball_x = self.position_x
        self.match.ball_y = self.position_y

        self.match.ball_vx = 0.0
        self.match.ball_vy = 0.0

    # ==================================================
    # CIBLE
    # ==================================================

    def set_target(self, x, y):

        self.target_x = float(x)
        self.target_y = float(y)

    # ==================================================
    # PUISSANCE
    # ==================================================

    def set_power(self, power):

        self.power = max(
            0.0,
            min(1.0, float(power))
        )

    # ==================================================
    # EFFET
    # ==================================================

    def set_spin(self, spin):

        self.spin = max(
            -1.0,
            min(1.0, float(spin))
        )

    # ==================================================
    # MUR
    # ==================================================

    def create_wall(
        self,
        defenders,
        count=4
    ):

        if not defenders:
            self.wall_players = []
            return

        available = [
            p for p in defenders
            if getattr(
                p,
                "on_pitch",
                True
            )
        ]

        available.sort(
            key=lambda p:
            self.distance_to_position(p)
        )

        self.wall_players = available[
            :max(1, count)
        ]

    def distance_to_position(self, player):

        return math.sqrt(
            (player.x - self.position_x) ** 2 +
            (player.y - self.position_y) ** 2
        )

    # ==================================================
    # EXÉCUTER
    # ==================================================

    def execute(self):

        if not self.active:
            return False

        if self.player is None:
            return False

        dx = (
            self.target_x -
            self.position_x
        )

        dy = (
            self.target_y -
            self.position_y
        )

        length = math.sqrt(
            dx * dx +
            dy * dy
        )

        if length <= 0:
            return False

        dx /= length
        dy /= length

        # ------------------------------------------------
        # PUISSANCE DE BASE
        # ------------------------------------------------

        if self.piece_type == "penalty":

            speed = 12.0 + (
                self.power * 8.0
            )

        elif self.piece_type == "free_kick":

            speed = 9.0 + (
                self.power * 10.0
            )

        elif self.piece_type == "corner":

            speed = 7.0 + (
                self.power * 7.0
            )

        elif self.piece_type == "throw_in":

            speed = 5.0 + (
                self.power * 5.0
            )

        else:

            speed = 6.0 + (
                self.power * 5.0
            )

        # ------------------------------------------------
        # BALLE
        # ------------------------------------------------

        self.match.ball_owner = None

        self.match.ball_vx = dx * speed
        self.match.ball_vy = dy * speed

        # Effet latéral.
        self.match.ball_vy += (
            self.spin * 2.0
        )

        self.active = False

        return True

    # ==================================================
    # PENALTY
    # ==================================================

    def start_penalty(
        self,
        team,
        player
    ):

        field = self.match.field

        if team == "blue":

            x = field.right - 75

        else:

            x = field.left + 75

        y = field.centery

        self.start(
            "penalty",
            team,
            x,
            y,
            player
        )

        # Centre du but adverse.
        if team == "blue":

            self.set_target(
                field.right,
                field.centery
            )

        else:

            self.set_target(
                field.left,
                field.centery
            )

        return True

    # ==================================================
    # COUP FRANC
    # ==================================================

    def start_free_kick(
        self,
        team,
        player,
        x,
        y
    ):

        self.start(
            "free_kick",
            team,
            x,
            y,
            player
        )

        field = self.match.field

        if team == "blue":

            target_x = field.right
            target_y = field.centery

        else:

            target_x = field.left
            target_y = field.centery

        self.set_target(
            target_x,
            target_y
        )

        return True

    # ==================================================
    # CORNER
    # ==================================================

    def start_corner(
        self,
        team,
        player,
        x,
        y,
        target_x,
        target_y
    ):

        self.start(
            "corner",
            team,
            x,
            y,
            player
        )

        self.set_target(
            target_x,
            target_y
        )

        return True

    # ==================================================
    # REMISE EN JEU
    # ==================================================

    def start_throw_in(
        self,
        team,
        player,
        x,
        y,
        target_x,
        target_y
    ):

        self.start(
            "throw_in",
            team,
            x,
            y,
            player
        )

        self.set_target(
            target_x,
            target_y
        )

        return True

    # ==================================================
    # SIX MÈTRES
    # ==================================================

    def start_goal_kick(
        self,
        team,
        player,
        x,
        y,
        target_x,
        target_y
    ):

        self.start(
            "goal_kick",
            team,
            x,
            y,
            player
        )

        self.set_target(
            target_x,
            target_y
        )

        return True

    # ==================================================
    # ÉTAT
    # ==================================================

    def is_active(self):

        return self.active

    def get_type(self):

        return self.piece_type

    def get_player(self):

        return self.player

    def get_team(self):

        return self.team

    # ==================================================
    # ANNULATION
    # ==================================================

    def cancel(self):

        self.active = False
        self.piece_type = None
        self.team = None
        self.player = None

        self.wall_players = []

        self.power = 0.0
        self.spin = 0.0

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        self.cancel()

        self.position_x = 0.0
        self.position_y = 0.0

        self.target_x = 0.0
        self.target_y = 0.0
