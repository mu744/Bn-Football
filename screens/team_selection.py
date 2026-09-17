import pygame

from data.teams import TEAMS
from core.states import MENU, SQUAD


class TeamSelection:

    def __init__(self, game):

        self.game = game

        self.buttons = []

        x_positions = [80, 470]
        y_positions = [120, 220, 320, 420]

        for index, team in enumerate(TEAMS):

            column = index % 2
            row = index // 2

            rect = pygame.Rect(
                x_positions[column],
                y_positions[row],
                350,
                75
            )

            self.buttons.append(
                (rect, index)
            )

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                self.game.state = MENU

        if event.type == pygame.MOUSEBUTTONDOWN:

            for rect, index in self.buttons:

                if rect.collidepoint(event.pos):

                    team = TEAMS[index]

                    self.game.save["club"] = team["name"]
                    self.game.save["team_id"] = team["id"]

                    self.game.save_game()

                    self.game.state = SQUAD

    def draw(self, screen):

        screen.fill(
            (7, 15, 27)
        )

        for rect, index in self.buttons:

            team = TEAMS[index]

            pygame.draw.rect(
                screen,
                (15, 35, 55),
                rect,
                border_radius=12
            )

            pygame.draw.rect(
                screen,
                team["color"],
                rect,
                3,
                border_radius=12
            )

            pygame.draw.circle(
                screen,
                team["color"],
                (rect.x + 42, rect.centery),
                23
            )

            pygame.draw.circle(
                screen,
                (5, 15, 25),
                (rect.x + 42, rect.centery),
                15
            )
