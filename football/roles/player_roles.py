class PlayerRoles:

    GK = "GK"

    CB = "CB"
    LB = "LB"
    RB = "RB"
    LWB = "LWB"
    RWB = "RWB"

    DM = "DM"
    CM = "CM"
    AM = "AM"

    LW = "LW"
    RW = "RW"
    ST = "ST"
    CF = "CF"

    ROLE_PROFILES = {

        "GK": {
            "attack": 0.05,
            "defense": 1.00,
            "support": 0.10,
            "width": 0.20,
            "depth": 0.10,
        },

        "CB": {
            "attack": 0.15,
            "defense": 1.00,
            "support": 0.30,
            "width": 0.55,
            "depth": 0.30,
        },

        "LB": {
            "attack": 0.55,
            "defense": 0.85,
            "support": 0.65,
            "width": 1.00,
            "depth": 0.55,
        },

        "RB": {
            "attack": 0.55,
            "defense": 0.85,
            "support": 0.65,
            "width": 1.00,
            "depth": 0.55,
        },

        "LWB": {
            "attack": 0.80,
            "defense": 0.65,
            "support": 0.85,
            "width": 1.20,
            "depth": 0.75,
        },

        "RWB": {
            "attack": 0.80,
            "defense": 0.65,
            "support": 0.85,
            "width": 1.20,
            "depth": 0.75,
        },

        "DM": {
            "attack": 0.35,
            "defense": 0.90,
            "support": 0.85,
            "width": 0.65,
            "depth": 0.80,
        },

        "CM": {
            "attack": 0.65,
            "defense": 0.65,
            "support": 1.00,
            "width": 0.75,
            "depth": 0.75,
        },

        "AM": {
            "attack": 0.90,
            "defense": 0.35,
            "support": 0.95,
            "width": 0.70,
            "depth": 0.90,
        },

        "LW": {
            "attack": 0.95,
            "defense": 0.25,
            "support": 0.65,
            "width": 1.20,
            "depth": 1.00,
        },

        "RW": {
            "attack": 0.95,
            "defense": 0.25,
            "support": 0.65,
            "width": 1.20,
            "depth": 1.00,
        },

        "ST": {
            "attack": 1.00,
            "defense": 0.15,
            "support": 0.45,
            "width": 0.60,
            "depth": 1.15,
        },

        "CF": {
            "attack": 0.95,
            "defense": 0.20,
            "support": 0.90,
            "width": 0.55,
            "depth": 1.00,
        },
    }

    @classmethod
    def get_profile(cls, role):

        return cls.ROLE_PROFILES.get(
            role,
            cls.ROLE_PROFILES["CM"]
        ).copy()

    @classmethod
    def is_goalkeeper(cls, role):
        return role == cls.GK

    @classmethod
    def is_defender(cls, role):
        return role in (
            cls.CB,
            cls.LB,
            cls.RB,
            cls.LWB,
            cls.RWB,
        )

    @classmethod
    def is_midfielder(cls, role):
        return role in (
            cls.DM,
            cls.CM,
            cls.AM,
        )

    @classmethod
    def is_attacker(cls, role):
        return role in (
            cls.LW,
            cls.RW,
            cls.ST,
            cls.CF,
        )

    @classmethod
    def all_roles(cls):
        return list(cls.ROLE_PROFILES.keys())
