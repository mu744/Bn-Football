class MatchManager:

    def __init__(self, match):

        self.match = match

        # Modules disponibles.
        self.gameplay = getattr(
            match,
            "gameplay_engine",
            None
        )

        self.team_ai = getattr(
            match,
            "team_ai",
            None
        )

        self.tactics = getattr(
            match,
            "tactics_system",
            None
        )

        self.dynamic_strategy = getattr(
            match,
            "dynamic_strategy",
            None
        )

        self.substitutions = getattr(
            match,
            "substitution_system",
            None
        )

        self.referee = getattr(
            match,
            "referee_system",
            None
        )

        self.set_pieces = getattr(
            match,
            "set_piece_system",
            None
        )

        self.statistics = getattr(
            match,
            "statistics",
            None
        )

        self.extra_time = getattr(
            match,
            "extra_time_system",
            None
        )

        self.enabled = True

    # ==================================================
    # MISE À JOUR CENTRALE
    # ==================================================

    def update(self, delta_time):

        if not self.enabled:
            return

        # 1. Temps et état du match.
        if hasattr(self.match, "update_match_time"):
            self.match.update_match_time(
                delta_time
            )

        # 2. Stratégie dynamique.
        self.update_strategy()

        # 3. Intelligence collective.
        if self.team_ai is not None:

            self.team_ai.update()

        # 4. Gameplay.
        if self.gameplay is not None:

            self.gameplay.update(
                delta_time
            )

        # 5. Arbitrage.
        if self.referee is not None:

            self.referee.update(
                delta_time
            )

        # 6. Statistiques.
        if self.statistics is not None:

            self.statistics.update(
                delta_time
            )

        # 7. Remplacements automatiques.
        self.update_substitutions()

    # ==================================================
    # STRATÉGIE
    # ==================================================

    def update_strategy(self):

        if self.dynamic_strategy is None:
            return

        engine = getattr(
            self.match,
            "match_engine",
            None
        )

        if engine is None:
            return

        blue_score = (
            engine.get_home_score()
        )

        red_score = (
            engine.get_away_score()
        )

        minute = (
            engine.get_exact_minute()
        )

        self.dynamic_strategy.update(
            blue_score,
            red_score,
            minute
        )

    # ==================================================
    # REMPLACEMENTS
    # ==================================================

    def update_substitutions(self):

        if self.substitutions is None:
            return

        engine = getattr(
            self.match,
            "match_engine",
            None
        )

        if engine is None:
            return

        minute = engine.get_exact_minute()

        self.substitutions.auto_substitute(
            "blue",
            minute
        )

        self.substitutions.auto_substitute(
            "red",
            minute
        )

    # ==================================================
    # BUT
    # ==================================================

    def register_goal(
        self,
        team,
        scorer=None,
        assist=None
    ):

        engine = getattr(
            self.match,
            "match_engine",
            None
        )

        if engine is not None:

            engine.goal(
                team,
                scorer
            )

        if self.statistics is not None:

            self.statistics.record_goal(
                scorer,
                team,
                assist
            )

    # ==================================================
    # PASSE
    # ==================================================

    def register_pass(
        self,
        player,
        completed=True
    ):

        if self.statistics is None:
            return

        self.statistics.record_pass(
            player,
            completed
        )

    # ==================================================
    # TIR
    # ==================================================

    def register_shot(
        self,
        player,
        on_target=False
    ):

        if self.statistics is None:
            return

        self.statistics.record_shot(
            player,
            on_target
        )

    # ==================================================
    # TACLE
    # ==================================================

    def register_tackle(self, player):

        if self.statistics is None:
            return

        self.statistics.record_tackle(
            player
        )

    # ==================================================
    # INTERCEPTION
    # ==================================================

    def register_interception(
        self,
        player
    ):

        if self.statistics is None:
            return

        self.statistics.record_interception(
            player
        )

    # ==================================================
    # FAUTE
    # ==================================================

    def register_foul(self, player):

        if self.statistics is None:
            return

        self.statistics.record_foul(
            player
        )

    # ==================================================
    # ARRÊT
    # ==================================================

    def register_save(self, goalkeeper):

        if self.statistics is None:
            return

        self.statistics.record_save(
            goalkeeper
        )

    # ==================================================
    # ÉTAT
    # ==================================================

    def enable(self):

        self.enabled = True

    def disable(self):

        self.enabled = False

    def is_enabled(self):

        return self.enabled

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        modules = (
            self.gameplay,
            self.team_ai,
            self.dynamic_strategy,
            self.substitutions,
            self.referee,
            self.set_pieces,
            self.statistics,
            self.extra_time
        )

        for module in modules:

            if module is not None and hasattr(
                module,
                "reset"
            ):

                module.reset()
