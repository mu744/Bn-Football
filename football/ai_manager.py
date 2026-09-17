from football.decision_system import DecisionSystem
from football.team_behavior import TeamBehavior
from football.attack_ai import AttackAI
from football.defense_ai import DefenseAI
from football.transition_ai import TransitionAI


class AIManager:

    def __init__(self, match):

        self.match = match

        self.decision = DecisionSystem(
            match
        )

        self.team_behavior = TeamBehavior(
            match
        )

        self.attack = AttackAI(
            match
        )

        self.defense = DefenseAI(
            match
        )

        self.transition = TransitionAI(
            match
        )

        self.enabled = True

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self, delta_time):

        if not self.enabled:
            return

        # 1. Décisions individuelles.
        self.decision.update(
            delta_time
        )

        # 2. Adaptation du comportement
        # collectif.
        self.team_behavior.update()

        # 3. Transition.
        self.transition.update(
            delta_time
        )

        # 4. Attaque.
        self.attack.update()

        # 5. Défense.
        self.defense.update()

    # ==================================================
    # DIFFICULTÉ
    # ==================================================

    def set_difficulty(
        self,
        difficulty
    ):

        football_ai = getattr(
            self.match,
            "football_ai",
            None
        )

        if football_ai is None:
            return False

        football_ai.set_difficulty(
            difficulty
        )

        return True

    # ==================================================
    # STYLE
    # ==================================================

    def set_team_style(
        self,
        team,
        style
    ):

        return self.team_behavior.set_style(
            team,
            style
        )

    def get_team_style(self, team):

        return self.team_behavior.get_style(
            team
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

        self.decision.reset()
        self.team_behavior.reset()
        self.attack.reset()
        self.defense.reset()
        self.transition.reset()
