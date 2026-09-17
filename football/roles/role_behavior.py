from football.roles.player_roles import PlayerRoles


class RoleBehavior:

    def __init__(self, player):

        self.player = player
        self.role = getattr(
            player,
            "role",
            "CM"
        )

    def set_role(self, role):

        if role not in PlayerRoles.all_roles():
            return False

        self.role = role
        self.player.role = role
        return True

    def get_role(self):

        return self.role

    def get_profile(self):

        return PlayerRoles.get_profile(
            self.role
        )

    def wants_to_attack(self):

        return (
            self.get_profile()["attack"] >= 0.65
        )

    def wants_to_defend(self):

        return (
            self.get_profile()["defense"] >= 0.65
        )

    def support_level(self):

        return self.get_profile()["support"]

    def width_level(self):

        return self.get_profile()["width"]

    def depth_level(self):

        return self.get_profile()["depth"]

    def attacking_priority(self):

        profile = self.get_profile()

        return (
            profile["attack"] *
            0.55
            +
            profile["support"] *
            0.25
            +
            profile["depth"] *
            0.20
        )

    def defensive_priority(self):

        profile = self.get_profile()

        return (
            profile["defense"] *
            0.65
            +
            profile["support"] *
            0.20
            +
            (1.0 - profile["attack"]) *
            0.15
        )

    def should_join_attack(
        self,
        team_has_ball
    ):

        if not team_has_ball:
            return False

        return (
            self.attacking_priority()
            >= 0.55
        )

    def should_return_defensively(
        self,
        team_has_ball
    ):

        if team_has_ball:
            return False

        return (
            self.defensive_priority()
            >= 0.50
        )

    def get_behavior_state(
        self,
        team_has_ball
    ):

        if self.role == "GK":
            return "goalkeeper"

        if team_has_ball:

            if self.wants_to_attack():
                return "attack"

            return "support"

        if self.wants_to_defend():
            return "defend"

        return "recover"

    def reset(self):

        self.role = getattr(
            self.player,
            "role",
            "CM"
        )
