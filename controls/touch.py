import math
import pygame


class TouchController:
    """
    Contrôleur tactile Android de BN-Football.

    Commandes :
        JOYSTICK  -> déplacement
        SPRINT    -> accélération
        PASS      -> passe
        SHOOT     -> tir
        TACKLE    -> tacle
        SWITCH    -> changement de joueur

    Compatible :
        - écran tactile Android
        - souris
        - multitouch
    """

    def __init__(self, width=900, height=600):

        self.width = width
        self.height = height

        self.enabled = True

        # -----------------------------------------------------
        # JOYSTICK
        # -----------------------------------------------------

        self.joystick_center = (
            105,
            height - 105
        )

        self.joystick_radius = 65
        self.knob_radius = 28

        self.joystick_active = False

        self.joystick_x = 0.0
        self.joystick_y = 0.0

        self.joystick_pointer = None

        # -----------------------------------------------------
        # BOUTONS
        # -----------------------------------------------------

        self.button_radius = 34

        self.buttons = {
            "pass": (
                width - 105,
                height - 170
            ),

            "shoot": (
                width - 75,
                height - 95
            ),

            "sprint": (
                width - 175,
                height - 80
            ),

            "tackle": (
                width - 205,
                height - 165
            ),

            "switch": (
                width - 275,
                height - 105
            )
        }

        # -----------------------------------------------------
        # ETAT DES BOUTONS
        # -----------------------------------------------------

        self.button_down = {
            "pass": False,
            "shoot": False,
            "sprint": False,
            "tackle": False,
            "switch": False
        }

        # Action déclenchée une seule fois.
        self.button_pressed = {
            "pass": False,
            "shoot": False,
            "sprint": False,
            "tackle": False,
            "switch": False
        }

        # -----------------------------------------------------
        # MULTITOUCH
        # -----------------------------------------------------

        self.active_fingers = {}

        # -----------------------------------------------------
        # SOURIS
        # -----------------------------------------------------

        self.mouse_active = False

    # =========================================================
    # OUTILS
    # =========================================================

    def distance(self, x1, y1, x2, y2):

        dx = x1 - x2
        dy = y1 - y2

        return math.sqrt(
            dx * dx +
            dy * dy
        )

    def inside_circle(self, pos, center, radius):

        return self.distance(
            pos[0],
            pos[1],
            center[0],
            center[1]
        ) <= radius

    # =========================================================
    # JOYSTICK
    # =========================================================

    def update_joystick(self, x, y):

        cx, cy = self.joystick_center

        dx = x - cx
        dy = y - cy

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        if distance > self.joystick_radius:

            dx /= distance
            dy /= distance

            dx *= self.joystick_radius
            dy *= self.joystick_radius

        self.joystick_x = (
            dx / self.joystick_radius
        )

        self.joystick_y = (
            dy / self.joystick_radius
        )

        self.joystick_active = True

    def release_joystick(self):

        self.joystick_active = False

        self.joystick_x = 0.0
        self.joystick_y = 0.0

        self.joystick_pointer = None

    def get_movement(self):

        return (
            self.joystick_x,
            self.joystick_y
        )

    # =========================================================
    # BOUTONS
    # =========================================================

    def get_button_at(self, x, y):

        for name, center in self.buttons.items():

            if self.inside_circle(
                (x, y),
                center,
                self.button_radius
            ):
                return name

        return None

    def press_button(self, name):

        if name not in self.button_down:
            return

        # Nouvelle pression.
        if not self.button_down[name]:

            self.button_pressed[name] = True

        self.button_down[name] = True

    def release_button(self, name):

        if name not in self.button_down:
            return

        self.button_down[name] = False

    def is_down(self, name):

        return self.button_down.get(
            name,
            False
        )

    def consume_pressed(self, name):

        if not self.button_pressed.get(
            name,
            False
        ):
            return False

        self.button_pressed[name] = False

        return True

    # =========================================================
    # EVENEMENTS SOURIS
    # =========================================================

    def handle_mouse_down(self, pos):

        x, y = pos

        if self.inside_circle(
            pos,
            self.joystick_center,
            self.joystick_radius
        ):

            self.mouse_active = True
            self.joystick_pointer = "mouse"

            self.update_joystick(x, y)

            return True

        button = self.get_button_at(x, y)

        if button is not None:

            self.press_button(button)

            return True

        return False

    def handle_mouse_motion(self, pos):

        if not self.mouse_active:
            return False

        self.update_joystick(
            pos[0],
            pos[1]
        )

        return True

    def handle_mouse_up(self, pos):

        handled = False

        if self.mouse_active:

            self.release_joystick()

            self.mouse_active = False

            handled = True

        # Relâchement des boutons.
        for name in self.buttons:

            if self.button_down[name]:

                self.release_button(name)
                handled = True

        return handled

    # =========================================================
    # MULTITOUCH ANDROID
    # =========================================================

    def handle_finger_down(self, event):

        x = event.x * self.width
        y = event.y * self.height

        finger_id = event.finger_id

        self.active_fingers[finger_id] = (
            x,
            y
        )

        if self.inside_circle(
            (x, y),
            self.joystick_center,
            self.joystick_radius
        ):

            self.joystick_pointer = finger_id

            self.update_joystick(
                x,
                y
            )

            return True

        button = self.get_button_at(
            x,
            y
        )

        if button is not None:

            self.press_button(button)

            return True

        return False

    def handle_finger_motion(self, event):

        finger_id = event.finger_id

        x = event.x * self.width
        y = event.y * self.height

        self.active_fingers[finger_id] = (
            x,
            y
        )

        if self.joystick_pointer == finger_id:

            self.update_joystick(
                x,
                y
            )

            return True

        return False

    def handle_finger_up(self, event):

        finger_id = event.finger_id

        x = event.x * self.width
        y = event.y * self.height

        self.active_fingers.pop(
            finger_id,
            None
        )

        handled = False

        if self.joystick_pointer == finger_id:

            self.release_joystick()

            handled = True

        button = self.get_button_at(
            x,
            y
        )

        if button is not None:

            self.release_button(
                button
            )

            handled = True

        return handled

    # =========================================================
    # EVENEMENT GENERAL
    # =========================================================

    def handle_event(self, event):

        if not self.enabled:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:

            return self.handle_mouse_down(
                event.pos
            )

        if event.type == pygame.MOUSEMOTION:

            return self.handle_mouse_motion(
                event.pos
            )

        if event.type == pygame.MOUSEBUTTONUP:

            return self.handle_mouse_up(
                event.pos
            )

        if event.type == pygame.FINGERDOWN:

            return self.handle_finger_down(
                event
            )

        if event.type == pygame.FINGERMOTION:

            return self.handle_finger_motion(
                event
            )

        if event.type == pygame.FINGERUP:

            return self.handle_finger_up(
                event
            )

        return False

    # =========================================================
    # AFFICHAGE
    # =========================================================

    def draw(self, screen):

        if not self.enabled:
            return

        # -----------------------------------------------------
        # JOYSTICK
        # -----------------------------------------------------

        cx, cy = self.joystick_center

        pygame.draw.circle(
            screen,
            (20, 30, 45),
            (int(cx), int(cy)),
            self.joystick_radius
        )

        pygame.draw.circle(
            screen,
            (70, 100, 125),
            (int(cx), int(cy)),
            self.joystick_radius,
            3
        )

        knob_x = (
            cx +
            self.joystick_x *
            self.joystick_radius
        )

        knob_y = (
            cy +
            self.joystick_y *
            self.joystick_radius
        )

        pygame.draw.circle(
            screen,
            (0, 210, 255),
            (int(knob_x), int(knob_y)),
            self.knob_radius
        )

        pygame.draw.circle(
            screen,
            (220, 245, 255),
            (int(knob_x), int(knob_y)),
            self.knob_radius,
            2
        )

        # -----------------------------------------------------
        # BOUTONS
        # -----------------------------------------------------

        button_colors = {
            "pass": (40, 160, 220),
            "shoot": (220, 70, 70),
            "sprint": (40, 190, 110),
            "tackle": (220, 170, 50),
            "switch": (140, 100, 220)
        }

        for name, center in self.buttons.items():

            pressed = self.button_down[name]

            radius = self.button_radius

            if pressed:
                radius -= 4

            color = button_colors.get(
                name,
                (80, 100, 120)
            )

            pygame.draw.circle(
                screen,
                color,
                (
                    int(center[0]),
                    int(center[1])
                ),
                radius
            )

            pygame.draw.circle(
                screen,
                (230, 240, 250),
                (
                    int(center[0]),
                    int(center[1])
                ),
                radius,
                2
            )

    # =========================================================
    # CONTROLE
    # =========================================================

    def enable(self):

        self.enabled = True

    def disable(self):

        self.enabled = False

        self.release_joystick()

        for name in self.button_down:

            self.button_down[name] = False

            self.button_pressed[name] = False

    def reset(self):

        self.release_joystick()

        for name in self.button_down:

            self.button_down[name] = False

            self.button_pressed[name] = False

        self.active_fingers.clear()

        self.mouse_active = False
