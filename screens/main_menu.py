import pygame

from core.settings import WIDTH, HEIGHT
from core.states import (
    MENU,
    TEAM_SELECTION,
    MATCH,
    CHAMPIONSHIP,
    CALENDAR,
    STANDINGS,
    SQUAD,
    SETTINGS
)


class MainMenu:

    def __init__(self, game):
        self.game = game

        self.buttons = [
            {
                "rect": pygame.Rect(250, 180, 400, 60),
                "state": MATCH,
                "icon": "play"
            },
            {
                "rect": pygame.Rect(250, 255, 400, 60),
                "state": CHAMPIONSHIP,
                "icon": "cup"
            },
            {
                "rect": pygame.Rect(250, 330, 190, 60),
                "state": TEAM_SELECTION,
                "icon": "team"
            },
            {
                "rect": pygame.Rect(460, 330, 190, 60),
                "state": CALENDAR,
                "icon": "calendar"
            },
            {
                "rect": pygame.Rect(250, 405, 190, 60),
                "state": STANDINGS,
                "icon": "ranking"
            },
            {
                "rect": pygame.Rect(460, 405, 190, 60),
                "state": SETTINGS,
                "icon": "settings"
            }
        ]

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            position = event.pos

            for button in self.buttons:

                if button["rect"].collidepoint(position):
                    self.game.state = button["state"]

    def draw(self, screen):

        # Fond
        screen.fill((7, 15, 27))

        # =========================
        # LOGO BN
        # =========================

        pygame.draw.circle(
            screen,
            (0, 210, 255),
            (WIDTH // 2, 80),
            45,
            4
        )

        pygame.draw.polygon(
            screen,
            (0, 210, 255),
            [
                (WIDTH // 2, 55),
                (WIDTH // 2 - 22, 75),
                (WIDTH // 2, 105),
                (WIDTH // 2 + 22, 75)
            ],
            3
        )

        # =========================
        # BOUTONS
        # =========================

        for button in self.buttons:

            rect = button["rect"]

            pygame.draw.rect(
                screen,
                (15, 35, 55),
                rect,
                border_radius=12
            )

            pygame.draw.rect(
                screen,
                (0, 180, 230),
                rect,
                2,
                border_radius=12
            )

            self.draw_icon(
                screen,
                button["icon"],
                rect.center
            )

    def draw_icon(self, screen, icon, center):

        x, y = center

        cyan = (0, 210, 255)
        white = (240, 245, 250)
        gold = (255, 200, 50)

        # MATCH RAPIDE
        if icon == "play":

            pygame.draw.polygon(
                screen,
                cyan,
                [
                    (x - 15, y - 22),
                    (x + 22, y),
                    (x - 15, y + 22)
                ]
            )

        # CHAMPIONNAT
        elif icon == "cup":

            pygame.draw.rect(
                screen,
                gold,
                (x - 16, y - 20, 32, 25),
                border_radius=5
            )

            pygame.draw.rect(
                screen,
                gold,
                (x - 5, y + 5, 10, 15)
            )

            pygame.draw.rect(
                screen,
                gold,
                (x - 18, y + 20, 36, 6)
            )

        # ÉQUIPE
        elif icon == "team":

            pygame.draw.circle(
                screen,
                cyan,
                (x, y - 12),
                10
            )

            pygame.draw.circle(
                screen,
                white,
                (x - 22, y - 5),
                7
            )

            pygame.draw.circle(
                screen,
                white,
                (x + 22, y - 5),
                7
            )

            pygame.draw.rect(
                screen,
                cyan,
                (x - 12, y + 2, 24, 22),
                border_radius=5
            )

        # CALENDRIER
        elif icon == "calendar":

            pygame.draw.rect(
                screen,
                white,
                (x - 24, y - 20, 48, 40),
                3
            )

            pygame.draw.line(
                screen,
                cyan,
                (x - 24, y - 7),
                (x + 24, y - 7),
                3
            )

            for px in (-10, 10):
                for py in (3, 15):
                    pygame.draw.circle(
                        screen,
                        cyan,
                        (x + px, y + py),
                        3
                    )

        # CLASSEMENT
        elif icon == "ranking":

            pygame.draw.rect(
                screen,
                cyan,
                (x - 25, y - 5, 10, 25)
            )

            pygame.draw.rect(
                screen,
                white,
                (x - 5, y - 20, 10, 40)
            )

            pygame.draw.rect(
                screen,
                gold,
                (x + 15, y + 5, 10, 15)
            )

        # PARAMÈTRES
        elif icon == "settings":

            pygame.draw.circle(
                screen,
                white,
                (x, y),
                20,
                5
            )

            pygame.draw.circle(
                screen,
                cyan,
                (x, y),
                7
            )


class PlaceholderScreen:

    def __init__(self, game, state):
        self.game = game
        self.state = state

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                self.game.state = MENU

        if event.type == pygame.MOUSEBUTTONDOWN:

            # Retour si on touche le haut gauche
            if event.pos[0] < 120 and event.pos[1] < 100:
                self.game.state = MENU

    def draw(self, screen):

        screen.fill((7, 15, 27))

        # Grand panneau central
        pygame.draw.rect(
            screen,
            (15, 35, 55),
            (100, 130, 700, 340),
            border_radius=20
        )

        pygame.draw.rect(
            screen,
            (0, 180, 230),
            (100, 130, 700, 340),
            3,
            border_radius=20
        )

        # Bouton retour
        pygame.draw.rect(
            screen,
            (20, 60, 80),
            (25, 25, 80, 50),
            border_radius=10
        )

        pygame.draw.polygon(
            screen,
            (0, 210, 255),
            [
                (85, 50),
                (55, 75),
                (85, 100)
            ]
        )
