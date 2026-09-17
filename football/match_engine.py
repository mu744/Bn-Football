class MatchEngine:

    # ==================================================
    # ÉTATS
    # ==================================================

    PRE_MATCH = "pre_match"
    FIRST_HALF = "first_half"
    HALF_TIME = "half_time"
    SECOND_HALF = "second_half"
    FULL_TIME = "full_time"
    PAUSED = "paused"

    def __init__(self, match):

        self.match = match

        # Durée réelle d'une rencontre simulée.
        self.match_duration = 90.0

        self.minute = 0.0

        self.state = self.PRE_MATCH

        self.home_score = 0
        self.away_score = 0

        self.half = 1

        self.running = False

        self.goal_scorer = None
        self.last_goal_team = None

        self.events = []

        # Vitesse de simulation :
        # 1.0 = vitesse normale.
        self.time_scale = 1.0

        self.stoppage_time = 0.0

    # ==================================================
    # DÉMARRER
    # ==================================================

    def start(self):

        self.minute = 0.0

        self.half = 1

        self.home_score = 0
        self.away_score = 0

        self.state = self.FIRST_HALF

        self.running = True

        self.events = []

        self.goal_scorer = None
        self.last_goal_team = None

        self.stoppage_time = 0.0

        self.record_event(
            "match_start",
            0.0
        )

    # ==================================================
    # PAUSE
    # ==================================================

    def pause(self):

        if not self.running:
            return

        self.running = False

        self.state = self.PAUSED

    # ==================================================
    # REPRENDRE
    # ==================================================

    def resume(self):

        if self.state != self.PAUSED:
            return

        self.running = True

        if self.half == 1:

            self.state = self.FIRST_HALF

        else:

            self.state = self.SECOND_HALF

    # ==================================================
    # TEMPS
    # ==================================================

    def update(self, delta_time):

        if not self.running:
            return

        if delta_time <= 0:
            return

        self.minute += (
            delta_time *
            self.time_scale
        )

        # Première mi-temps.
        if (
            self.half == 1
            and self.minute >= 45
        ):

            self.minute = 45.0

            self.half_time()

            return

        # Deuxième mi-temps.
        if (
            self.half == 2
            and self.minute >= 90
        ):

            self.minute = 90.0

            self.full_time()

    # ==================================================
    # MI-TEMPS
    # ==================================================

    def half_time(self):

        self.running = False

        self.state = self.HALF_TIME

        self.record_event(
            "half_time",
            self.minute
        )

    # ==================================================
    # COMMENCER DEUXIÈME MI-TEMPS
    # ==================================================

    def start_second_half(self):

        if self.state != self.HALF_TIME:
            return False

        self.half = 2

        self.minute = 45.0

        self.running = True

        self.state = self.SECOND_HALF

        self.record_event(
            "second_half_start",
            45.0
        )

        return True

    # ==================================================
    # FIN DU MATCH
    # ==================================================

    def full_time(self):

        self.running = False

        self.state = self.FULL_TIME

        self.minute = 90.0

        self.record_event(
            "full_time",
            90.0
        )

    # ==================================================
    # BUT
    # ==================================================

    def goal(
        self,
        team,
        scorer=None
    ):

        if team not in (
            "blue",
            "red"
        ):
            return False

        if self.state not in (
            self.FIRST_HALF,
            self.SECOND_HALF
        ):
            return False

        if team == "blue":

            self.home_score += 1

        else:

            self.away_score += 1

        self.goal_scorer = scorer

        self.last_goal_team = team

        self.record_event(
            "goal",
            self.minute,
            {
                "team": team,
                "scorer": scorer
            }
        )

        return True

    # ==================================================
    # SCORE
    # ==================================================

    def get_score(self):

        return (
            self.home_score,
            self.away_score
        )

    def get_home_score(self):

        return self.home_score

    def get_away_score(self):

        return self.away_score

    # ==================================================
    # DIFFÉRENCE
    # ==================================================

    def get_goal_difference(self, team):

        if team == "blue":

            return (
                self.home_score -
                self.away_score
            )

        if team == "red":

            return (
                self.away_score -
                self.home_score
            )

        return 0

    # ==================================================
    # ÉTAT DU MATCH
    # ==================================================

    def get_state(self):

        return self.state

    def is_running(self):

        return self.running

    def is_finished(self):

        return self.state == self.FULL_TIME

    def is_half_time(self):

        return self.state == self.HALF_TIME

    # ==================================================
    # MINUTE
    # ==================================================

    def get_minute(self):

        return int(self.minute)

    def get_exact_minute(self):

        return self.minute

    # ==================================================
    # TEMPS RESTANT
    # ==================================================

    def get_remaining_time(self):

        return max(
            0.0,
            self.match_duration -
            self.minute
        )

    # ==================================================
    # SITUATION D'ÉQUIPE
    # ==================================================

    def get_team_status(self, team):

        difference = self.get_goal_difference(
            team
        )

        if difference > 0:
            return "winning"

        if difference < 0:
            return "losing"

        return "drawing"

    # ==================================================
    # ÉVÉNEMENTS
    # ==================================================

    def record_event(
        self,
        event_type,
        minute,
        data=None
    ):

        event = {
            "type": event_type,
            "minute": minute,
            "data": data or {}
        }

        self.events.append(event)

    def get_events(self):

        return list(self.events)

    def get_last_event(self):

        if not self.events:
            return None

        return self.events[-1]

    # ==================================================
    # VITESSE
    # ==================================================

    def set_time_scale(self, value):

        self.time_scale = max(
            0.1,
            min(10.0, float(value))
        )

    def get_time_scale(self):

        return self.time_scale

    # ==================================================
    # TEMPS ADDITIONNEL
    # ==================================================

    def set_stoppage_time(self, minutes):

        self.stoppage_time = max(
            0.0,
            float(minutes)
        )

    def get_stoppage_time(self):

        return self.stoppage_time

    # ==================================================
    # RÉSULTAT
    # ==================================================

    def get_result(self):

        if self.home_score > self.away_score:

            return "blue_win"

        if self.away_score > self.home_score:

            return "red_win"

        return "draw"

    # ==================================================
    # RÉINITIALISATION
    # ==================================================

    def reset(self):

        self.minute = 0.0

        self.half = 1

        self.state = self.PRE_MATCH

        self.running = False

        self.home_score = 0
        self.away_score = 0

        self.goal_scorer = None
        self.last_goal_team = None

        self.events = []

        self.stoppage_time = 0.0

        self.time_scale = 1.0
