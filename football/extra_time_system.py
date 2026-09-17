import random


class ExtraTimeSystem:

    NORMAL = "normal"
    EXTRA_TIME = "extra_time"
    PENALTY_SHOOTOUT = "penalty_shootout"
    FINISHED = "finished"

    def __init__(self, match):

        self.match = match

        self.state = self.NORMAL

        self.extra_time = 30.0
        self.minute = 90.0

        self.home_score = 0
        self.away_score = 0

        self.penalty_round = 0

        self.home_penalties = []
        self.away_penalties = []

        self.max_penalty_rounds = 5

        self.finished = False

        self.winner = None

    # ==================================================
    # CONFIGURATION
    # ==================================================

    def set_score(
        self,
        home_score,
        away_score
    ):

        self.home_score = int(
            home_score
        )

        self.away_score = int(
            away_score
        )

    # ==================================================
    # VÉRIFICATION
    # ==================================================

    def is_draw(self):

        return (
            self.home_score ==
            self.away_score
        )

    def needs_extra_time(self):

        return self.is_draw()

    # ==================================================
    # PROLONGATION
    # ==================================================

    def start_extra_time(self):

        if not self.needs_extra_time():
            return False

        self.state = self.EXTRA_TIME

        self.minute = 90.0

        self.finished = False

        return True

    def update_extra_time(
        self,
        delta_time
    ):

        if self.state != self.EXTRA_TIME:
            return

        self.minute += delta_time

        if self.minute >= 120:

            self.minute = 120

            self.finish_extra_time()

    def finish_extra_time(self):

        if self.home_score != self.away_score:

            self.finish_match()

            return

        self.start_penalty_shootout()

    # ==================================================
    # BUT PENDANT PROLONGATION
    # ==================================================

    def goal(self, team):

        if self.state not in (
            self.EXTRA_TIME,
            self.NORMAL
        ):
            return False

        if team == "blue":

            self.home_score += 1

        elif team == "red":

            self.away_score += 1

        else:

            return False

        return True

    # ==================================================
    # SÉANCE DE TIRS AU BUT
    # ==================================================

    def start_penalty_shootout(self):

        self.state = (
            self.PENALTY_SHOOTOUT
        )

        self.penalty_round = 0

        self.home_penalties = []

        self.away_penalties = []

        self.finished = False

        self.winner = None

    # ==================================================
    # TIR AU BUT
    # ==================================================

    def take_penalty(
        self,
        team,
        scored=None
    ):

        if self.state != self.PENALTY_SHOOTOUT:
            return False

        if team not in (
            "blue",
            "red"
        ):
            return False

        # Si le résultat n'est pas fourni,
        # on le simule.
        if scored is None:

            scored = (
                random.random() < 0.75
            )

        scored = bool(scored)

        if team == "blue":

            self.home_penalties.append(
                scored
            )

        else:

            self.away_penalties.append(
                scored
            )

        self.check_penalty_result()

        return scored

    # ==================================================
    # SCORE DE LA SÉANCE
    # ==================================================

    def penalty_score(self, team):

        if team == "blue":

            return sum(
                self.home_penalties
            )

        if team == "red":

            return sum(
                self.away_penalties
            )

        return 0

    # ==================================================
    # VÉRIFICATION
    # ==================================================

    def check_penalty_result(self):

        home_count = len(
            self.home_penalties
        )

        away_count = len(
            self.away_penalties
        )

        home_score = (
            self.penalty_score("blue")
        )

        away_score = (
            self.penalty_score("red")
        )

        # Après chaque équipe ayant tiré
        # le même nombre de penalties.
        if home_count == away_count:

            self.penalty_round = home_count

            # Victoire définitive après 5 tirs.
            if (
                home_count >=
                self.max_penalty_rounds
            ):

                if home_score != away_score:

                    self.finish_penalties(
                        "blue"
                        if home_score > away_score
                        else "red"
                    )

                    return

            # Mort subite après les 5 premiers.
            if home_count > 5:

                if home_score != away_score:

                    self.finish_penalties(
                        "blue"
                        if home_score > away_score
                        else "red"
                    )

    # ==================================================
    # FIN DE LA SÉANCE
    # ==================================================

    def finish_penalties(self, winner):

        self.winner = winner

        self.state = self.FINISHED

        self.finished = True

    # ==================================================
    # FIN DU MATCH
    # ==================================================

    def finish_match(self):

        if self.home_score > self.away_score:

            self.winner = "blue"

        elif self.away_score > self.home_score:

            self.winner = "red"

        else:

            self.winner = None

        self.state = self.FINISHED

        self.finished = True

    # ==================================================
    # ÉTAT
    # ==================================================

    def get_state(self):

        return self.state

    def is_finished(self):

        return self.finished

    def get_winner(self):

        return self.winner

    # ==================================================
    # SCORE
    # ==================================================

    def get_score(self):

        return (
            self.home_score,
            self.away_score
        )

    def get_penalty_score(self):

        return (
            self.penalty_score("blue"),
            self.penalty_score("red")
        )

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        self.state = self.NORMAL

        self.minute = 90.0

        self.home_score = 0
        self.away_score = 0

        self.penalty_round = 0

        self.home_penalties = []

        self.away_penalties = []

        self.finished = False

        self.winner = None
