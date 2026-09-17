class AdvancedTactics:

    MENTALITIES = {
        "defensive": {
            "attack": 0.55,
            "defense": 1.25,
            "width": 0.75,
            "depth": 0.65,
            "pressing": 0.45,
            "tempo": 0.70,
            "counter_attack": 0.85,
        },

        "balanced": {
            "attack": 1.00,
            "defense": 1.00,
            "width": 1.00,
            "depth": 1.00,
            "pressing": 0.70,
            "tempo": 1.00,
            "counter_attack": 0.60,
        },

        "offensive": {
            "attack": 1.30,
            "defense": 0.75,
            "width": 1.20,
            "depth": 1.25,
            "pressing": 0.90,
            "tempo": 1.20,
            "counter_attack": 0.50,
        },

        "all_out_attack": {
            "attack": 1.55,
            "defense": 0.50,
            "width": 1.35,
            "depth": 1.45,
            "pressing": 1.00,
            "tempo": 1.35,
            "counter_attack": 0.40,
        }
    }

    PRESSING = {
        "low": 0.45,
        "medium": 0.70,
        "high": 0.90,
        "extreme": 1.00
    }

    def __init__(
        self,
        formation="4-3-3",
        mentality="balanced"
    ):

        self.formation = formation

        if mentality not in self.MENTALITIES:
            mentality = "balanced"

        self.mentality = mentality

        self.width = 1.0
        self.depth = 1.0

        self.pressing = "medium"

        self.tempo = 1.0

        self.counter_attack = True

        self.possession_style = True

        self.attack_support = 1.0

        self.defensive_line = 1.0

    # ==================================================
    # FORMATION
    # ==================================================

    def set_formation(self, formation):

        if not formation:
            return False

        self.formation = formation

        return True

    def get_formation(self):

        return self.formation

    # ==================================================
    # MENTALITÉ
    # ==================================================

    def set_mentality(self, mentality):

        if mentality not in self.MENTALITIES:
            return False

        self.mentality = mentality

        return True

    def get_mentality(self):

        return self.mentality

    def get_mentality_profile(self):

        return self.MENTALITIES[
            self.mentality
        ].copy()

    # ==================================================
    # LARGEUR
    # ==================================================

    def set_width(self, value):

        self.width = max(
            0.50,
            min(1.50, float(value))
        )

    def increase_width(self, amount=0.10):

        self.set_width(
            self.width + amount
        )

    def decrease_width(self, amount=0.10):

        self.set_width(
            self.width - amount
        )

    # ==================================================
    # PROFONDEUR
    # ==================================================

    def set_depth(self, value):

        self.depth = max(
            0.50,
            min(1.50, float(value))
        )

    def increase_depth(self, amount=0.10):

        self.set_depth(
            self.depth + amount
        )

    def decrease_depth(self, amount=0.10):

        self.set_depth(
            self.depth - amount
        )

    # ==================================================
    # PRESSING
    # ==================================================

    def set_pressing(self, level):

        if level not in self.PRESSING:
            return False

        self.pressing = level

        return True

    def get_pressing_strength(self):

        return self.PRESSING[
            self.pressing
        ]

    # ==================================================
    # RYTHME
    # ==================================================

    def set_tempo(self, value):

        self.tempo = max(
            0.50,
            min(1.50, float(value))
        )

    def increase_tempo(self):

        self.set_tempo(
            self.tempo + 0.10
        )

    def decrease_tempo(self):

        self.set_tempo(
            self.tempo - 0.10
        )

    # ==================================================
    # CONTRE-ATTAQUE
    # ==================================================

    def enable_counter_attack(self):

        self.counter_attack = True

    def disable_counter_attack(self):

        self.counter_attack = False

    def is_counter_attack_enabled(self):

        return self.counter_attack

    # ==================================================
    # POSSESSION
    # ==================================================

    def enable_possession(self):

        self.possession_style = True

    def disable_possession(self):

        self.possession_style = False

    def wants_possession(self):

        return self.possession_style

    # ==================================================
    # SOUTIEN OFFENSIF
    # ==================================================

    def set_attack_support(self, value):

        self.attack_support = max(
            0.50,
            min(1.50, float(value))
        )

    # ==================================================
    # LIGNE DÉFENSIVE
    # ==================================================

    def set_defensive_line(self, value):

        self.defensive_line = max(
            0.50,
            min(1.50, float(value))
        )

    # ==================================================
    # PROFIL COMPLET
    # ==================================================

    def get_profile(self):

        mentality = self.get_mentality_profile()

        return {
            "formation": self.formation,
            "mentality": self.mentality,
            "width": self.width *
                     mentality["width"],
            "depth": self.depth *
                     mentality["depth"],
            "pressing": (
                self.get_pressing_strength() *
                mentality["pressing"]
            ),
            "tempo": (
                self.tempo *
                mentality["tempo"]
            ),
            "attack": mentality["attack"],
            "defense": mentality["defense"],
            "counter_attack": (
                self.counter_attack and
                mentality["counter_attack"] > 0
            ),
            "possession": self.possession_style,
            "attack_support": self.attack_support,
            "defensive_line": self.defensive_line
        }

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        self.width = 1.0
        self.depth = 1.0
        self.pressing = "medium"
        self.tempo = 1.0
        self.counter_attack = True
        self.possession_style = True
        self.attack_support = 1.0
        self.defensive_line = 1.0
        self.mentality = "balanced"
