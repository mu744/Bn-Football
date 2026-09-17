class EventBus:

    # ==================================================
    # TYPES D'ÉVÉNEMENTS
    # ==================================================

    GOAL = "goal"
    SHOT = "shot"
    PASS = "pass"
    DRIBBLE = "dribble"
    TACKLE = "tackle"
    INTERCEPTION = "interception"

    FOUL = "foul"
    YELLOW_CARD = "yellow_card"
    RED_CARD = "red_card"

    OFFSIDE = "offside"

    CORNER = "corner"
    FREE_KICK = "free_kick"
    PENALTY = "penalty"
    THROW_IN = "throw_in"
    GOAL_KICK = "goal_kick"

    SUBSTITUTION = "substitution"

    MATCH_START = "match_start"
    HALF_TIME = "half_time"
    SECOND_HALF = "second_half"
    FULL_TIME = "full_time"

    def __init__(self):

        self.listeners = {}

        self.history = []

        self.max_history = 500

    # ==================================================
    # ABONNEMENT
    # ==================================================

    def subscribe(
        self,
        event_type,
        callback
    ):

        if not callable(callback):
            return False

        if event_type not in self.listeners:

            self.listeners[event_type] = []

        if callback not in self.listeners[event_type]:

            self.listeners[event_type].append(
                callback
            )

        return True

    # ==================================================
    # DÉSABONNEMENT
    # ==================================================

    def unsubscribe(
        self,
        event_type,
        callback
    ):

        if event_type not in self.listeners:
            return False

        if callback not in self.listeners[
            event_type
        ]:
            return False

        self.listeners[
            event_type
        ].remove(callback)

        return True

    # ==================================================
    # ÉMISSION
    # ==================================================

    def emit(
        self,
        event_type,
        data=None
    ):

        event = {
            "type": event_type,
            "data": data or {}
        }

        self.history.append(event)

        if len(self.history) > self.max_history:

            self.history.pop(0)

        callbacks = list(
            self.listeners.get(
                event_type,
                []
            )
        )

        for callback in callbacks:

            try:

                callback(
                    event
                )

            except Exception:
                # Une erreur dans un module
                # ne doit pas arrêter tout le jeu.
                continue

        return event

    # ==================================================
    # ÉMISSION AVEC MINUTE
    # ==================================================

    def emit_match_event(
        self,
        event_type,
        minute,
        data=None
    ):

        payload = data.copy() if data else {}

        payload["minute"] = minute

        return self.emit(
            event_type,
            payload
        )

    # ==================================================
    # HISTORIQUE
    # ==================================================

    def get_history(self):

        return list(
            self.history
        )

    def get_events(
        self,
        event_type
    ):

        return [
            event
            for event in self.history
            if event["type"] == event_type
        ]

    def get_last_event(self):

        if not self.history:
            return None

        return self.history[-1]

    # ==================================================
    # NETTOYAGE
    # ==================================================

    def clear_history(self):

        self.history.clear()

    def clear_listeners(self):

        self.listeners.clear()

    # ==================================================
    # RESET
    # ==================================================

    def reset(self):

        self.clear_history()
