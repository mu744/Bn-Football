from football.roles.player_roles import PlayerRoles
from football.roles.role_behavior import RoleBehavior


class RoleManager:

    def __init__(self, match):

        self.match = match
        self.behaviors = {}

        self.enabled = True

        self.initialize()

    # ==================================================
    # INITIALISATION
    # ==================================================

    def initialize(self):

        players = (
            self.match.home_players
            +
            self.match.away_players
        )

        for player in players:

            role = getattr(
                player,
                "role",
                None
            )

            if role not in PlayerRoles.all_roles():

                role = self.convert_old_position(
                    getattr(
                        player,
                        "position",
                        "MC"
                    )
                )

            player.role = role

            self.behaviors[
                id(player)
            ] = RoleBehavior(
                player
            )

    # ==================================================
    # COMPATIBILITÉ ANCIEN SYSTÈME
    # ==================================================

    def convert_old_position(
        self,
        position
    ):

        if position == "GK":
            return "GK"

        if position == "DF":
            return "CB"

        if position == "MC":
            return "CM"

        if position == "AT":
            return "ST"

        return "CM"

    # ==================================================
    # RÔLE
    # ==================================================

    def set_role(
        self,
        player,
        role
    ):

        if player is None:
            return False

        behavior = self.get_behavior(
            player
        )

        if behavior is None:
            return False

        return behavior.set_role(
            role
        )

    def get_role(self, player):

        if player is None:
            return None

        return getattr(
            player,
            "role",
            "CM"
        )

    def get_behavior(self, player):

        if player is None:
            return None

        return self.behaviors.get(
            id(player)
        )

    # ==================================================
    # GROUPEMENT
    # ==================================================

    def get_players_by_role(
        self,
        team,
        role
    ):

        players = (
            self.match.home_players
            if team == "blue"
            else self.match.away_players
        )

        return [
            player
            for player in players
            if getattr(
                player,
                "role",
                None
            ) == role
            and getattr(
                player,
                "on_pitch",
                True
            )
        ]

    def get_defenders(self, team):

        players = (
            self.match.home_players
            if team == "blue"
            else self.match.away_players
        )

        return [
            player
            for player in players
            if PlayerRoles.is_defender(
                getattr(
                    player,
                    "role",
                    "CM"
                )
            )
        ]

    def get_midfielders(self, team):

        players = (
            self.match.home_players
            if team == "blue"
            else self.match.away_players
        )

        return [
            player
            for player in players
            if PlayerRoles.is_midfielder(
                getattr(
                    player,
                    "role",
                    "CM"
                )
            )
        ]

    def get_attackers(self, team):

        players = (
            self.match.home_players
            if team == "blue"
            else self.match.away_players
        )

        return [
            player
            for player in players
            if PlayerRoles.is_attacker(
                getattr(
                    player,
                    "role",
                    "CM"
                )
            )
        ]

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        if not self.enabled:
            return

        # Maintient la compatibilité avec
        # l'ancien champ position.
        players = (
            self.match.home_players
            +
            self.match.away_players
        )

        for player in players:

            role = getattr(
                player,
                "role",
                None
            )

            if role not in PlayerRoles.all_roles():
                continue

            if role == "GK":
                player.position = "GK"

            elif PlayerRoles.is_defender(role):
                player.position = "DF"

            elif PlayerRoles.is_midfielder(role):
                player.position = "MC"

            elif PlayerRoles.is_attacker(role):
                player.position = "AT"

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

        self.behaviors.clear()
        self.initialize()
