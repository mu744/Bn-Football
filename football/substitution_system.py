import math


class SubstitutionSystem:

    def __init__(self, match):

        self.match = match

        # Nombre maximum de changements.
        self.max_substitutions = 5

        self.home_used = 0
        self.away_used = 0

        # Temps minimum avant un changement automatique.
        self.minimum_minute = 45

        # Seuil de fatigue.
        self.auto_substitution_stamina = 18.0

        self.enabled = True

        self.last_substitution = None

    # ==================================================
    # ÉQUIPES
    # ==================================================

    def get_team_players(self, team):

        if team == "blue":
            return self.match.home_players

        return self.match.away_players

    # ==================================================
    # NOMBRE DE CHANGEMENTS
    # ==================================================

    def get_used(self, team):

        if team == "blue":
            return self.home_used

        return self.away_used

    def get_remaining(self, team):

        return max(
            0,
            self.max_substitutions -
            self.get_used(team)
        )

    def can_substitute(self, team):

        return (
            self.enabled and
            self.get_remaining(team) > 0
        )

    # ==================================================
    # DISTANCE
    # ==================================================

    def distance(self, a, b):

        return math.sqrt(
            (a.x - b.x) ** 2 +
            (a.y - b.y) ** 2
        )

    # ==================================================
    # TROUVER UN REMPLAÇANT
    # ==================================================

    def find_replacement(
        self,
        team,
        player
    ):

        if player is None:
            return None

        players = self.get_team_players(team)

        # Un joueur disponible est identifié par
        # son statut "on_pitch".
        candidates = []

        for candidate in players:

            if candidate is player:
                continue

            if getattr(
                candidate,
                "on_pitch",
                True
            ):
                continue

            # Priorité au même poste.
            same_position = (
                getattr(
                    candidate,
                    "position",
                    None
                )
                ==
                getattr(
                    player,
                    "position",
                    None
                )
            )

            rating = getattr(
                candidate,
                "rating",
                70
            )

            score = rating

            if same_position:
                score += 30

            candidates.append(
                (score, candidate)
            )

        if not candidates:
            return None

        candidates.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return candidates[0][1]

    # ==================================================
    # EFFECTUER UN CHANGEMENT
    # ==================================================

    def substitute(
        self,
        team,
        player_out,
        player_in,
        minute=0
    ):

        if not self.can_substitute(team):
            return False

        if player_out is None:
            return False

        if player_in is None:
            return False

        if player_out is player_in:
            return False

        if getattr(
            player_in,
            "on_pitch",
            True
        ):
            return False

        players = self.get_team_players(team)

        if player_out not in players:
            return False

        if player_in not in players:
            return False

        # ------------------------------------------
        # TRANSFERT DE POSITION
        # ------------------------------------------

        player_in.x = player_out.x
        player_in.y = player_out.y

        player_in.direction_x = (
            player_out.direction_x
        )

        player_in.direction_y = (
            player_out.direction_y
        )

        # ------------------------------------------
        # ÉTAT DU JOUEUR
        # ------------------------------------------

        player_out.on_pitch = False
        player_in.on_pitch = True

        # Le remplaçant entre avec une bonne énergie.
        player_in.stamina = max(
            70.0,
            getattr(
                player_in,
                "stamina",
                100.0
            )
        )

        # Le joueur sorti ne contrôle plus le ballon.
        if self.match.ball_owner is player_out:

            self.match.ball_owner = player_in

            self.match.ball_x = (
                player_in.x +
                player_in.direction_x * 20
            )

            self.match.ball_y = (
                player_in.y +
                player_in.direction_y * 20
            )

        # ------------------------------------------
        # COMPTEUR
        # ------------------------------------------

        if team == "blue":
            self.home_used += 1
        else:
            self.away_used += 1

        self.last_substitution = {
            "team": team,
            "player_out": player_out,
            "player_in": player_in,
            "minute": minute
        }

        return True

    # ==================================================
    # CHANGEMENT AUTOMATIQUE
    # ==================================================

    def auto_substitute(
        self,
        team,
        minute
    ):

        if minute < self.minimum_minute:
            return False

        if not self.can_substitute(team):
            return False

        players = self.get_team_players(team)

        tired_player = None

        lowest_stamina = (
            self.auto_substitution_stamina
        )

        for player in players:

            if not getattr(
                player,
                "on_pitch",
                True
            ):
                continue

            # Éviter de sortir le gardien
            # automatiquement.
            if getattr(
                player,
                "position",
                ""
            ) == "GK":
                continue

            stamina = getattr(
                player,
                "stamina",
                100
            )

            if stamina < lowest_stamina:

                lowest_stamina = stamina
                tired_player = player

        if tired_player is None:
            return False

        replacement = self.find_replacement(
            team,
            tired_player
        )

        if replacement is None:
            return False

        return self.substitute(
            team,
            tired_player,
            replacement,
            minute
        )

    # ==================================================
    # RÉINITIALISATION
    # ==================================================

    def reset(self):

        self.home_used = 0
        self.away_used = 0

        self.last_substitution = None

        players = (
            self.match.home_players +
            self.match.away_players
        )

        for player in players:

            player.on_pitch = True

    # ==================================================
    # INFORMATIONS
    # ==================================================

    def get_status(self):

        return {
            "home_used": self.home_used,
            "home_remaining": (
                self.get_remaining("blue")
            ),
            "away_used": self.away_used,
            "away_remaining": (
                self.get_remaining("red")
            )
        }

    def get_last_substitution(self):

        return self.last_substitution
