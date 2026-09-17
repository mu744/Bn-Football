class TeamBehavior:

    def __init__(self, match):

        self.match = match
        self.enabled = True

        self.styles = {
            "possession": {
                "tempo": 0.75,
                "risk": 0.30,
                "width": 1.00
            },

            "direct": {
                "tempo": 1.20,
                "risk": 0.65,
                "width": 1.10
            },

            "counter": {
                "tempo": 1.40,
                "risk": 0.80,
                "width": 1.15
            },

            "defensive": {
                "tempo": 0.60,
                "risk": 0.20,
                "width": 0.80
            }
        }

        self.team_styles = {
            "blue": "possession",
            "red": "possession"
        }

    # ==================================================
    # STYLE
    # ==================================================

    def set_style(self, team, style):

        if team not in self.team_styles:
            return False

        if style not in self.styles:
            return False

        self.team_styles[team] = style

        return True

    def get_style(self, team):

        return self.team_styles.get(
            team,
            "possession"
        )

    def get_profile(self, team):

        return self.styles[
            self.get_style(team)
        ].copy()

    # ==================================================
    # POSSESSION
    # ==================================================

    def has_ball(self, team):

        owner = self.match.ball_owner

        if owner is None:
            return False

        return owner.team == team

    # ==================================================
    # SITUATION
    # ==================================================

    def get_situation(self, team):

        owner = self.match.ball_owner

        if owner is None:
            return "loose"

        if owner.team == team:
            return "attack"

        return "defense"

    # ==================================================
    # STYLE AUTOMATIQUE
    # ==================================================

    def adapt_style(
        self,
        team,
        own_score,
        opponent_score,
        minute
    ):

        difference = (
            own_score -
            opponent_score
        )

        remaining = 90 - minute

        if difference < 0:

            if remaining <= 20:

                self.set_style(
                    team,
                    "direct"
                )

            else:

                self.set_style(
                    team,
                    "counter"
                )

        elif difference > 0:

            if remaining <= 15:

                self.set_style(
                    team,
                    "defensive"
                )

            else:

                self.set_style(
                    team,
                    "possession"
                )

        else:

            self.set_style(
                team,
                "possession"
            )

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        if not self.enabled:
            return

        engine = getattr(
            self.match,
            "match_engine",
            None
        )

        if engine is None:
            return

        minute = engine.get_exact_minute()

        self.adapt_style(
            "blue",
            engine.get_home_score(),
            engine.get_away_score(),
            minute
        )

        self.adapt_style(
            "red",
            engine.get_away_score(),
            engine.get_home_score(),
            minute
        )

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        self.team_styles = {
            "blue": "possession",
            "red": "possession"
        }
