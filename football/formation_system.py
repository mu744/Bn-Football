import math


class FormationSystem:

    def __init__(self, match):

        self.match = match

        self.enabled = True

        self.home_formation = "4-3-3"
        self.away_formation = "4-3-3"

        self.home_mentality = "balanced"
        self.away_mentality = "balanced"

        self.positions = {}

        self.attack_push = 55.0
        self.defensive_drop = 45.0
        self.width_factor = 1.0

    # ==================================================
    # FORMATIONS
    # ==================================================

    FORMATIONS = {

        "4-3-3": [
            "GK",
            "DF", "DF", "DF", "DF",
            "MC", "MC", "MC",
            "AT", "AT", "AT"
        ],

        "4-4-2": [
            "GK",
            "DF", "DF", "DF", "DF",
            "MC", "MC", "MC", "MC",
            "AT", "AT"
        ],

        "4-2-3-1": [
            "GK",
            "DF", "DF", "DF", "DF",
            "MC", "MC",
            "AT", "AT", "AT",
            "AT"
        ],

        "3-5-2": [
            "GK",
            "DF", "DF", "DF",
            "MC", "MC", "MC", "MC", "MC",
            "AT", "AT"
        ]
    }

    # ==================================================
    # CONFIGURATION
    # ==================================================

    def set_formation(
        self,
        team,
        formation
    ):

        if formation not in self.FORMATIONS:
            return False

        if team == "blue":
            self.home_formation = formation
        elif team == "red":
            self.away_formation = formation
        else:
            return False

        self.apply_positions(team)

        return True

    def get_formation(self, team):

        if team == "blue":
            return self.home_formation

        if team == "red":
            return self.away_formation

        return None

    # ==================================================
    # MENTALITÉ
    # ==================================================

    def set_mentality(
        self,
        team,
        mentality
    ):

        allowed = (
            "defensive",
            "balanced",
            "offensive",
            "counter"
        )

        if mentality not in allowed:
            return False

        if team == "blue":
            self.home_mentality = mentality

        elif team == "red":
            self.away_mentality = mentality

        else:
            return False

        return True

    def get_mentality(self, team):

        if team == "blue":
            return self.home_mentality

        if team == "red":
            return self.away_mentality

        return "balanced"

    # ==================================================
    # JOUEURS
    # ==================================================

    def get_players(self, team):

        if team == "blue":
            return self.match.home_players

        return self.match.away_players

    # ==================================================
    # POSITION DE BASE
    # ==================================================

    def create_base_positions(
        self,
        team
    ):

        players = self.get_players(team)

        formation = self.get_formation(team)

        roles = self.FORMATIONS.get(
            formation,
            self.FORMATIONS["4-3-3"]
        )

        field = self.match.field

        active_players = [
            player
            for player in players
            if getattr(
                player,
                "on_pitch",
                True
            )
        ]

        for index, player in enumerate(
            active_players[:11]
        ):

            role = roles[
                min(index, len(roles) - 1)
            ]

            player.position = role

            if team == "blue":

                base_x = field.left + (
                    field.width *
                    (0.10 + index * 0.075)
                )

            else:

                base_x = field.right - (
                    field.width *
                    (0.10 + index * 0.075)
                )

            # Répartition verticale.
            row = index % 5

            base_y = (
                field.top +
                field.height *
                (0.20 + row * 0.15)
            )

            self.positions[
                id(player)
            ] = (
                base_x,
                base_y
            )

    # ==================================================
    # POSITION DYNAMIQUE
    # ==================================================

    def calculate_dynamic_position(
        self,
        player,
        team
    ):

        field = self.match.field

        base = self.positions.get(
            id(player)
        )

        if base is None:

            return player.x, player.y

        base_x, base_y = base

        ball_x = self.match.ball_x

        mentality = self.get_mentality(
            team
        )

        owner = self.match.ball_owner

        attacking = (
            owner is not None
            and owner.team == team
        )

        # ----------------------------------------------
        # AVANCÉE / RECUL
        # ----------------------------------------------

        if attacking:

            if mentality == "offensive":
                push = self.attack_push * 1.30

            elif mentality == "counter":
                push = self.attack_push * 1.50

            elif mentality == "defensive":
                push = self.attack_push * 0.45

            else:
                push = self.attack_push

        else:

            if mentality == "defensive":
                push = -self.defensive_drop * 1.20

            else:
                push = -self.defensive_drop

        # ----------------------------------------------
        # ADAPTATION À LA POSITION DU BALLON
        # ----------------------------------------------

        ball_offset = (
            ball_x - field.centery
        )

        # Correction volontairement limitée :
        # le ballon influence la ligne sans
        # faire courir toute l'équipe dessus.
        ball_influence = (
            (ball_x - field.left)
            / max(1, field.width)
        )

        ball_influence -= 0.5

        if team == "blue":
            direction = 1
        else:
            direction = -1

        dynamic_x = (
            base_x +
            direction *
            push *
            0.45
        )

        dynamic_x += (
            ball_influence *
            direction *
            70
        )

        # ----------------------------------------------
        # LARGEUR
        # ----------------------------------------------

        center_y = field.centery

        width = self.width_factor

        if mentality == "offensive":
            width *= 1.20

        elif mentality == "defensive":
            width *= 0.80

        offset_y = (
            base_y -
            center_y
        ) * width

        dynamic_y = (
            center_y +
            offset_y
        )

        # ----------------------------------------------
        # RÔLE
        # ----------------------------------------------

        role = getattr(
            player,
            "position",
            ""
        )

        if role == "AT":

            if attacking:
                dynamic_x += (
                    direction * 30
                )

        elif role == "DF":

            if not attacking:
                dynamic_x -= (
                    direction * 15
                )

        elif role == "MC":

            dynamic_x += (
                direction *
                (push * 0.20)
            )

        # ----------------------------------------------
        # LIMITES
        # ----------------------------------------------

        dynamic_x = max(
            field.left + 20,
            min(
                field.right - 20,
                dynamic_x
            )
        )

        dynamic_y = max(
            field.top + 20,
            min(
                field.bottom - 20,
                dynamic_y
            )
        )

        return (
            dynamic_x,
            dynamic_y
        )

    # ==================================================
    # APPLICATION
    # ==================================================

    def apply_positions(
        self,
        team
    ):

        self.create_base_positions(
            team
        )

    # ==================================================
    # DÉPLACEMENT PROGRESSIF
    # ==================================================

    def update_player(
        self,
        player,
        team
    ):

        if not getattr(
            player,
            "on_pitch",
            True
        ):
            return

        target_x, target_y = (
            self.calculate_dynamic_position(
                player,
                team
            )
        )

        # GK : ne pas utiliser la même
        # logique que les joueurs de champ.
        if getattr(
            player,
            "position",
            ""
        ) == "GK":

            return

        dx = target_x - player.x
        dy = target_y - player.y

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        if distance <= 2:
            return

        # Mouvement lent pour éviter
        # les téléportations.
        factor = min(
            0.035,
            distance / 100
        )

        player.x += dx * factor
        player.y += dy * factor

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        if not self.enabled:
            return

        for player in self.match.home_players:

            self.update_player(
                player,
                "blue"
            )

        for player in self.match.away_players:

            self.update_player(
                player,
                "red"
            )

    # ==================================================
    # LARGEUR
    # ==================================================

    def set_width(
        self,
        value
    ):

        self.width_factor = max(
            0.60,
            min(
                1.40,
                float(value)
            )
        )

    def increase_width(self):

        self.set_width(
            self.width_factor + 0.10
        )

    def decrease_width(self):

        self.set_width(
            self.width_factor - 0.10
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

        self.positions.clear()

        self.home_mentality = "balanced"
        self.away_mentality = "balanced"

        self.width_factor = 1.0

        self.apply_positions("blue")
        self.apply_positions("red")
