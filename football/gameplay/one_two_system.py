class OneTwoSystem:
    def __init__(self, match):
        self.match = match
        self.enabled = True
        self.active = None

    def start(self, player, teammate):
        if not self.enabled:
            return False

        if player is None or teammate is None:
            return False

        if player.team != teammate.team:
            return False

        if self.match.ball_owner is not player:
            return False

        self.active = {
            "player": player,
            "teammate": teammate,
        }

        self.match.ball_owner = teammate

        return True

    def return_pass(self):
        if self.active is None:
            return False

        player = self.active["player"]
        teammate = self.active["teammate"]

        if self.match.ball_owner is not teammate:
            return False

        self.match.ball_owner = player
        self.active = None

        return True

    def update(self):
        pass

    def reset(self):
        self.active = None
