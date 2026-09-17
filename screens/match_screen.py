import pygame

from football.match import Match
from core.states import MENU


class MatchScreen:

    def __init__(self, game):

        self.game = game
        self.match = Match(game)

        self.move_x = 0
        self.move_y = 0

        self.left_button = pygame.Rect(
            45, 495, 70, 55
        )

        self.right_button = pygame.Rect(
            125, 495, 70, 55
        )

        self.up_button = pygame.Rect(
            85, 430, 70, 55
        )

        self.down_button = pygame.Rect(
            85, 560, 70, 30
        )

        self.pass_button = pygame.Rect(
            650, 475, 75, 65
        )

        self.shoot_button = pygame.Rect(
            745, 475, 95, 65
        )

        self.select_button = pygame.Rect(
            600, 20, 120, 45
        )

        self.back_button = pygame.Rect(
            20, 20, 90, 45
        )

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                self.game.state = MENU
                return

            if event.key == pygame.K_LEFT:
                self.move_x = -1

            elif event.key == pygame.K_RIGHT:
                self.move_x = 1

            elif event.key == pygame.K_UP:
                self.move_y = -1

            elif event.key == pygame.K_DOWN:
                self.move_y = 1

            elif event.key == pygame.K_SPACE:

                self.match.shoot()

            elif event.key == pygame.K_p:

                self.match.pass_ball()

            elif event.key == pygame.K_TAB:

                self.match.select_nearest_player()

            elif event.key == pygame.K_c:

                self.match.next_player()

        elif event.type == pygame.KEYUP:

            if event.key in (
                pygame.K_LEFT,
                pygame.K_RIGHT
            ):

                self.move_x = 0

            if event.key in (
                pygame.K_UP,
                pygame.K_DOWN
            ):

                self.move_y = 0

        elif event.type == pygame.MOUSEBUTTONDOWN:

            pos = event.pos

            if self.back_button.collidepoint(pos):

                self.game.state = MENU
                return

            if self.select_button.collidepoint(pos):

                self.match.select_nearest_player()
                return

            if self.pass_button.collidepoint(pos):

                self.match.pass_ball()
                return

            if self.shoot_button.collidepoint(pos):

                self.match.shoot()
                return

            if self.left_button.collidepoint(pos):

                self.move_x = -1

            elif self.right_button.collidepoint(pos):

                self.move_x = 1

            elif self.up_button.collidepoint(pos):

                self.move_y = -1

            elif self.down_button.collidepoint(pos):

                self.move_y = 1

        elif event.type == pygame.MOUSEBUTTONUP:

            pos = event.pos

            if (
                self.left_button.collidepoint(pos)
                or self.right_button.collidepoint(pos)
            ):

                self.move_x = 0

            if (
                self.up_button.collidepoint(pos)
                or self.down_button.collidepoint(pos)
            ):

                self.move_y = 0

    def update(self):

        if self.move_x != 0 or self.move_y != 0:

            self.match.move_selected_player(
                self.move_x,
                self.move_y
            )

        self.match.update()

    def button(
        self,
        screen,
        rect,
        border,
        fill
    ):

        pygame.draw.rect(
            screen,
            fill,
            rect,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            border,
            rect,
            2,
            border_radius=12
        )

    def arrow(
        self,
        screen,
        center,
        direction
    ):

        x, y = center

        if direction == "left":

            points = [
                (x - 18, y),
                (x + 10, y - 15),
                (x + 10, y + 15)
            ]

        elif direction == "right":

            points = [
                (x + 18, y),
                (x - 10, y - 15),
                (x - 10, y + 15)
            ]

        elif direction == "up":

            points = [
                (x, y - 18),
                (x - 15, y + 10),
                (x + 15, y + 10)
            ]

        else:

            points = [
                (x, y + 18),
                (x - 15, y - 10),
                (x + 15, y - 10)
            ]

        pygame.draw.polygon(
            screen,
            (230, 245, 255),
            points
        )

    def draw_controls(self, screen):

        self.button(
            screen,
            self.left_button,
            (0, 210, 255),
            (10, 30, 45)
        )

        self.button(
            screen,
            self.right_button,
            (0, 210, 255),
            (10, 30, 45)
        )

        self.button(
            screen,
            self.up_button,
            (0, 210, 255),
            (10, 30, 45)
        )

        self.button(
            screen,
            self.down_button,
            (0, 210, 255),
            (10, 30, 45)
        )

        self.arrow(
            screen,
            self.left_button.center,
            "left"
        )

        self.arrow(
            screen,
            self.right_button.center,
            "right"
        )

        self.arrow(
            screen,
            self.up_button.center,
            "up"
        )

        self.arrow(
            screen,
            self.down_button.center,
            "down"
        )

        # PASS
        self.button(
            screen,
            self.pass_button,
            (80, 210, 255),
            (10, 65, 90)
        )

        # TIR
        self.button(
            screen,
            self.shoot_button,
            (255, 80, 100),
            (70, 20, 30)
        )

        # SELECTION
        self.button(
            screen,
            self.select_button,
            (0, 210, 255),
            (10, 30, 45)
        )

        # RETOUR
        self.button(
            screen,
            self.back_button,
            (0, 210, 255),
            (10, 30, 45)
        )

    def draw(self, screen):

        self.match.draw(screen)

        self.draw_controls(screen)
