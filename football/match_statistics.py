class MatchStatistics:

    TEAM_STATS = (
        "goals",
        "shots",
        "shots_on_target",
        "passes",
        "passes_completed",
        "dribbles",
        "dribbles_completed",
        "tackles",
        "interceptions",
        "fouls",
        "yellow_cards",
        "red_cards",
        "corners",
        "offsides",
        "saves",
        "possession_time",
        "distance"
    )

    PLAYER_STATS = (
        "goals",
        "assists",
        "shots",
        "shots_on_target",
        "passes",
        "passes_completed",
        "dribbles",
        "dribbles_completed",
        "tackles",
        "interceptions",
        "fouls",
        "offsides",
        "saves",
        "ball_losses",
        "distance"
    )

    def __init__(self, match):

        self.match = match

        self.teams = {
            "blue": self.create_team_stats(),
            "red": self.create_team_stats()
        }

        self.players = {}

        self.previous_positions = {}

    # ==================================================
    # CRÉATION
    # ==================================================

    def create_team_stats(self):

        return {
            stat: 0
            for stat in self.TEAM_STATS
        }

    def create_player_stats(self):

        return {
            stat: 0
            for stat in self.PLAYER_STATS
        }

    # ==================================================
    # JOUEUR
    # ==================================================

    def initialize_player(self, player):

        if player is None:
            return

        key = id(player)

        if key not in self.players:

            self.players[key] = {
                "player": player,
                "stats": self.create_player_stats()
            }

            self.previous_positions[key] = (
                player.x,
                player.y
            )

    # ==================================================
    # ENREGISTRER UNE STATISTIQUE
    # ==================================================

    def add_team_stat(
        self,
        team,
        stat,
        amount=1
    ):

        if team not in self.teams:
            return False

        if stat not in self.TEAM_STATS:
            return False

        self.teams[team][stat] += amount

        return True

    def add_player_stat(
        self,
        player,
        stat,
        amount=1
    ):

        if player is None:
            return False

        if stat not in self.PLAYER_STATS:
            return False

        self.initialize_player(player)

        self.players[id(player)]["stats"][stat] += amount

        return True

    # ==================================================
    # BUT
    # ==================================================

    def record_goal(
        self,
        player,
        team,
        assist=None
    ):

        self.add_team_stat(
            team,
            "goals"
        )

        self.add_player_stat(
            player,
            "goals"
        )

        if assist is not None:

            self.add_player_stat(
                assist,
                "assists"
            )

    # ==================================================
    # TIR
    # ==================================================

    def record_shot(
        self,
        player,
        on_target=False
    ):

        if player is None:
            return

        team = player.team

        self.add_team_stat(
            team,
            "shots"
        )

        self.add_player_stat(
            player,
            "shots"
        )

        if on_target:

            self.add_team_stat(
                team,
                "shots_on_target"
            )

            self.add_player_stat(
                player,
                "shots_on_target"
            )

    # ==================================================
    # PASSE
    # ==================================================

    def record_pass(
        self,
        player,
        completed=True
    ):

        if player is None:
            return

        team = player.team

        self.add_team_stat(
            team,
            "passes"
        )

        self.add_player_stat(
            player,
            "passes"
        )

        if completed:

            self.add_team_stat(
                team,
                "passes_completed"
            )

            self.add_player_stat(
                player,
                "passes_completed"
            )

    # ==================================================
    # DRIBBLE
    # ==================================================

    def record_dribble(
        self,
        player,
        completed=True
    ):

        if player is None:
            return

        team = player.team

        self.add_team_stat(
            team,
            "dribbles"
        )

        self.add_player_stat(
            player,
            "dribbles"
        )

        if completed:

            self.add_team_stat(
                team,
                "dribbles_completed"
            )

            self.add_player_stat(
                player,
                "dribbles_completed"
            )

    # ==================================================
    # TACLE
    # ==================================================

    def record_tackle(self, player):

        if player is None:
            return

        self.add_team_stat(
            player.team,
            "tackles"
        )

        self.add_player_stat(
            player,
            "tackles"
        )

    # ==================================================
    # INTERCEPTION
    # ==================================================

    def record_interception(self, player):

        if player is None:
            return

        self.add_team_stat(
            player.team,
            "interceptions"
        )

        self.add_player_stat(
            player,
            "interceptions"
        )

    # ==================================================
    # FAUTE
    # ==================================================

    def record_foul(self, player):

        if player is None:
            return

        self.add_team_stat(
            player.team,
            "fouls"
        )

        self.add_player_stat(
            player,
            "fouls"
        )

    # ==================================================
    # CARTONS
    # ==================================================

    def record_yellow_card(self, player):

        if player is None:
            return

        self.add_team_stat(
            player.team,
            "yellow_cards"
        )

    def record_red_card(self, player):

        if player is None:
            return

        self.add_team_stat(
            player.team,
            "red_cards"
        )

    # ==================================================
    # CORNER
    # ==================================================

    def record_corner(self, team):

        self.add_team_stat(
            team,
            "corners"
        )

    # ==================================================
    # HORS-JEU
    # ==================================================

    def record_offside(self, player):

        if player is None:
            return

        self.add_team_stat(
            player.team,
            "offsides"
        )

        self.add_player_stat(
            player,
            "offsides"
        )

    # ==================================================
    # ARRÊT
    # ==================================================

    def record_save(self, goalkeeper):

        if goalkeeper is None:
            return

        self.add_team_stat(
            goalkeeper.team,
            "saves"
        )

        self.add_player_stat(
            goalkeeper,
            "saves"
        )

    # ==================================================
    # PERTE DE BALLE
    # ==================================================

    def record_ball_loss(self, player):

        if player is None:
            return

        self.add_player_stat(
            player,
            "ball_losses"
        )

    # ==================================================
    # DISTANCE
    # ==================================================

    def update_distance(self):

        players = (
            self.match.home_players +
            self.match.away_players
        )

        for player in players:

            self.initialize_player(player)

            key = id(player)

            old_x, old_y = (
                self.previous_positions[key]
            )

            dx = player.x - old_x
            dy = player.y - old_y

            distance = (
                dx * dx +
                dy * dy
            ) ** 0.5

            if distance > 0:

                self.add_team_stat(
                    player.team,
                    "distance",
                    distance
                )

                self.add_player_stat(
                    player,
                    "distance",
                    distance
                )

            self.previous_positions[key] = (
                player.x,
                player.y
            )

    # ==================================================
    # POSSESSION
    # ==================================================

    def update_possession(
        self,
        delta_time
    ):

        owner = self.match.ball_owner

        if owner is None:
            return

        team = owner.team

        self.add_team_stat(
            team,
            "possession_time",
            delta_time
        )

    # ==================================================
    # MISE À JOUR
    # ==================================================

    def update(self, delta_time):

        self.update_distance()

        self.update_possession(
            delta_time
        )

    # ==================================================
    # POURCENTAGE DE POSSESSION
    # ==================================================

    def get_possession_percentages(self):

        blue = self.teams["blue"][
            "possession_time"
        ]

        red = self.teams["red"][
            "possession_time"
        ]

        total = blue + red

        if total <= 0:

            return {
                "blue": 50,
                "red": 50
            }

        return {
            "blue": round(
                blue / total * 100
            ),
            "red": round(
                red / total * 100
            )
        }

    # ==================================================
    # PRÉCISION DES PASSES
    # ==================================================

    def get_pass_accuracy(self, team):

        if team not in self.teams:
            return 0

        total = self.teams[team]["passes"]

        completed = self.teams[team][
            "passes_completed"
        ]

        if total <= 0:
            return 0

        return round(
            completed / total * 100
        )

    # ==================================================
    # STATISTIQUES D'ÉQUIPE
    # ==================================================

    def get_team_stats(self, team):

        if team not in self.teams:
            return {}

        result = self.teams[team].copy()

        result["possession"] = (
            self.get_possession_percentages()
            [team]
        )

        result["pass_accuracy"] = (
            self.get_pass_accuracy(team)
        )

        return result

    # ==================================================
    # STATISTIQUES JOUEUR
    # ==================================================

    def get_player_stats(self, player):

        if player is None:
            return {}

        self.initialize_player(player)

        return self.players[
            id(player)
        ]["stats"].copy()

    # ==================================================
    # TOUTES LES STATISTIQUES
    # ==================================================

    def get_all_stats(self):

        return {
            "blue": self.get_team_stats(
                "blue"
            ),
            "red": self.get_team_stats(
                "red"
            )
        }

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        self.teams = {
            "blue": self.create_team_stats(),
            "red": self.create_team_stats()
        }

        self.players.clear()

        self.previous_positions.clear()

        players = (
            self.match.home_players +
            self.match.away_players
        )

        for player in players:

            self.initialize_player(
                player
            )
