import pygame


class InputManager:
    """
    Gestionnaire unique des commandes.

    Sources prises en charge :
    - clavier
    - écran tactile
    - joystick virtuel
    - futur gamepad

    Les systèmes de gameplay ne dépendent pas directement
    du périphérique utilisé.
    """

    def __init__(self, match, mobile_controls=None):
        self.match = match
        self.mobile_controls = mobile_controls

        self.enabled = True

        self.keyboard_x = 0.0
        self.keyboard_y = 0.0
        self.keyboard_sprint = False

        self.previous_keys = set()

    # --------------------------------------------------
    # MOBILE
    # --------------------------------------------------

    def set_mobile_controls(self, mobile_controls):
        self.mobile_controls = mobile_controls

    # --------------------------------------------------
    # CLAVIER
    # --------------------------------------------------

    def read_keyboard(self):
        keys = pygame.key.get_pressed()

        dx = 0.0
        dy = 0.0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= 1.0

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += 1.0

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= 1.0

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += 1.0

        self.keyboard_x = dx
        self.keyboard_y = dy

        self.keyboard_sprint = bool(
            keys[pygame.K_LSHIFT]
            or keys[pygame.K_RSHIFT]
        )

    # --------------------------------------------------
    # DEPLACEMENT
    # --------------------------------------------------

    def get_movement(self):
        if not self.enabled:
            return 0.0, 0.0

        if self.mobile_controls is not None:
            mobile_input = self.mobile_controls.get_input()

            dx, dy = mobile_input.get_movement()

            if abs(dx) > 0.05 or abs(dy) > 0.05:
                return dx, dy

        return self.keyboard_x, self.keyboard_y

    # --------------------------------------------------
    # SPRINT
    # --------------------------------------------------

    def is_sprinting(self):
        if not self.enabled:
            return False

        if self.mobile_controls is not None:
            mobile_input = self.mobile_controls.get_input()

            if mobile_input.is_sprinting():
                return True

        return self.keyboard_sprint

    # --------------------------------------------------
    # ACTIONS TACTILES
    # --------------------------------------------------

    def mobile_action(self, action):
        if self.mobile_controls is None:
            return False

        mobile_input = self.mobile_controls.get_input()

        if action == "pass":
            return mobile_input.wants_pass()

        if action == "shoot":
            return mobile_input.wants_shoot()

        if action == "tackle":
            return mobile_input.wants_tackle()

        if action == "switch":
            return mobile_input.wants_switch_player()

        return False

    # --------------------------------------------------
    # ACTIONS CLAVIER
    # --------------------------------------------------

    def keyboard_action(self, action):
        keys = pygame.key.get_pressed()

        key_map = {
            "pass": pygame.K_p,
            "shoot": pygame.K_SPACE,
            "tackle": pygame.K_t,
            "switch": pygame.K_TAB,
        }

        key = key_map.get(action)

        if key is None:
            return False

        pressed = bool(keys[key])

        if pressed and key not in self.previous_keys:
            self.previous_keys.add(key)
            return True

        if not pressed:
            self.previous_keys.discard(key)

        return False

    # --------------------------------------------------
    # ACTION GLOBALE
    # --------------------------------------------------

    def action_pressed(self, action):
        if not self.enabled:
            return False

        if self.mobile_action(action):
            return True

        return self.keyboard_action(action)

    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------

    def update(self):
        if not self.enabled:
            return

        self.read_keyboard()

    # --------------------------------------------------
    # EVENEMENTS
    # --------------------------------------------------

    def handle_event(self, event):
        if not self.enabled:
            return False

        if self.mobile_controls is not None:
            return self.mobile_controls.handle_event(event)

        return False

    # --------------------------------------------------
    # CONTROLE
    # --------------------------------------------------

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

        self.keyboard_x = 0.0
        self.keyboard_y = 0.0
        self.keyboard_sprint = False

        self.previous_keys.clear()

    def reset(self):
        self.keyboard_x = 0.0
        self.keyboard_y = 0.0
        self.keyboard_sprint = False

        self.previous_keys.clear()

        self.enabled = True
