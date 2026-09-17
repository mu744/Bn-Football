class PlayerController:
    """
    Contrôleur central du joueur humain.

    Reçoit les commandes depuis InputManager et applique
    les déplacements au joueur sélectionné.
    """

    def __init__(self, match, action_controller=None):
        self.match = match
        self.actions = action_controller
        self.enabled = True

        self.direction_x = 0.0
        self.direction_y = 0.0
        self.sprinting = False

    def set_direction(self, dx, dy):
        if not self.enabled:
            return

        self.direction_x = float(dx)
        self.direction_y = float(dy)

    def set_sprint(self, sprint):
        if not self.enabled:
            return

        self.sprinting = bool(sprint)

    def get_player(self):
        if not self.enabled:
            return None

        if hasattr(self.match, "get_selected_player"):
            return self.match.get_selected_player()

        if self.actions is not None:
            return self.actions.ensure_selected_player()

        return None

    def update_movement(self):
        player = self.get_player()

        if player is None:
            return

        dx = self.direction_x
        dy = self.direction_y

        if abs(dx) < 0.01 and abs(dy) < 0.01:
            player.brake()
            player.is_sprinting = False
            return

        player.is_sprinting = self.sprinting

        player.move(
            dx,
            dy,
            self.match.field,
            sprint=self.sprinting
        )

    def update(self):
        if not self.enabled:
            return

        self.update_movement()

    def move(self, dx, dy, sprint=False):
        self.set_direction(dx, dy)
        self.set_sprint(sprint)
        self.update()

    def stop(self):
        player = self.get_player()

        if player is not None:
            player.stop()
            player.is_sprinting = False

        self.direction_x = 0.0
        self.direction_y = 0.0
        self.sprinting = False

    def enable(self):
        self.enabled = True

    def disable(self):
        self.stop()
        self.enabled = False

    def reset(self):
        self.direction_x = 0.0
        self.direction_y = 0.0
        self.sprinting = False
        self.enabled = True
