import pygame

from football.team import Team
from football.tactics import (
    get_positions,
    get_formation_names
)

from core.states import (
    MENU,
    TEAM_SELECTION,
    MATCH
)


class SquadScreen:

    def __init__(self, game):

        self.game = game

        self.team = None

        self.selected_player = None
        self.selected_bench = None

        self.formations = get_formation_names()

        self.formation = self.game.save.get(
            "formation",
            "4-3-3"
        )

        self.field = pygame.Rect(
            300, 85,
            560, 450
        )

        self.back_button = pygame.Rect(
            25, 25,
            120, 45
        )

        self.play_button = pygame.Rect(
            700, 25,
            160, 45
        )

        self.formation_buttons = [
            pygame.Rect(25, 130, 240, 55),
            pygame.Rect(25, 200, 240, 55),
            pygame.Rect(25, 270, 240, 55)
        ]

        self.refresh()

    def refresh(self):

        team_id = self.game.save.get(
            "team_id",
            "bnu"
        )

        self.team = Team(team_id)

        self.formation = self.game.save.get(
            "formation",
            self.team.formation
        )

        pygame.display.set_caption(
            "BN-Football - Tactique " + self.formation
        )

    def save_formation(self):

        self.game.save["formation"] = self.formation

        self.game.save_game()

    def change_formation(self, formation):

        self.formation = formation

        self.save_formation()

        self.selected_player = None
        self.selected_bench = None

        pygame.display.set_caption(
            "BN-Football - Tactique " + self.formation
        )

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                self.game.state = MENU

            if event.key == pygame.K_1:
                self.change_formation("4-3-3")

            if event.key == pygame.K_2:
                self.change_formation("4-4-2")

            if event.key == pygame.K_3:
                self.change_formation("4-2-3-1")

        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        pos = event.pos

        if self.back_button.collidepoint(pos):

            self.game.state = TEAM_SELECTION
            return

        if self.play_button.collidepoint(pos):

            self.game.state = MATCH
            return

        for index, rect in enumerate(
            self.formation_buttons
        ):

            if rect.collidepoint(pos):

                self.change_formation(
                    self.formations[index]
                )

                return

        # Sélection des titulaires
        positions = get_positions(
            self.formation,
            self.field
        )

        for index, player_pos in enumerate(positions):

            dx = pos[0] - player_pos[0]
            dy = pos[1] - player_pos[1]

            if dx * dx + dy * dy <= 25 * 25:

                self.selected_player = index
                self.selected_bench = None

                return

        # Remplaçants
        bench = self.team.get_bench()

        for index, player in enumerate(bench):

            rect = pygame.Rect(
                25,
                365 + index * 38,
                240,
                32
            )

            if rect.collidepoint(pos):

                self.selected_bench = index

                if self.selected_player is not None:

                    self.make_substitution(
                        self.selected_player,
                        index
                    )

                return

    def make_substitution(
        self,
        starter_index,
        bench_index
    ):

        starters = self.team.players[:11]
        bench = self.team.players[11:]

        if starter_index >= len(starters):
            return

        if bench_index >= len(bench):
            return

        starters[starter_index], bench[bench_index] = (
            bench[bench_index],
            starters[starter_index]
        )

        self.team.players = starters + bench

        # On sauvegarde les joueurs actifs.
        self.game.save["lineup"] = [
            player["number"]
            for player in self.team.players
        ]

        self.game.save_game()

        self.selected_player = None
        self.selected_bench = None

    def player_color(self, player):

        position = player["position"]

        if position == "GK":
            return (245, 190, 40)

        if position == "DF":
            return (30, 150, 240)

        if position == "MC":
            return (40, 210, 150)

        return (230, 70, 100)

    def draw_field(self, screen):

        pygame.draw.rect(
            screen,
            (15, 95, 60),
            self.field,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            (220, 245, 230),
            self.field,
            4,
            border_radius=12
        )

        # Ligne centrale
        center_y = self.field.centery

        pygame.draw.line(
            screen,
            (220, 245, 230),
            (self.field.left, center_y),
            (self.field.right, center_y),
            3
        )

        # Cercle central
        pygame.draw.circle(
            screen,
            (220, 245, 230),
            (self.field.centerx, center_y),
            55,
            3
        )

        # Surface de réparation
        area = pygame.Rect(
            self.field.left + 120,
            self.field.bottom - 125,
            320,
            125
        )

        pygame.draw.rect(
            screen,
            (220, 245, 230),
            area,
            3
        )

        # Petit rectangle
        small = pygame.Rect(
            self.field.left + 190,
            self.field.bottom - 60,
            180,
            60
        )

        pygame.draw.rect(
            screen,
            (220, 245, 230),
            small,
            3
        )

        # But
        goal = pygame.Rect(
            self.field.centerx - 55,
            self.field.bottom - 12,
            110,
            12
        )

        pygame.draw.rect(
            screen,
            (245, 245, 245),
            goal
        )

    def draw_player(
        self,
        screen,
        player,
        position,
        selected=False
    ):

        color = self.player_color(player)

        if selected:

            pygame.draw.circle(
                screen,
                (255, 220, 60),
                position,
                29,
                4
            )

        pygame.draw.circle(
            screen,
            color,
            position,
            22
        )

        pygame.draw.circle(
            screen,
            (240, 250, 255),
            position,
            7
        )

        # Petite barre de rating
        rating_width = int(
            player["rating"] * 0.35
        )

        pygame.draw.rect(
            screen,
            (5, 15, 25),
            (
                position[0] - 24,
                position[1] + 27,
                48,
                6
            ),
            border_radius=3
        )

        pygame.draw.rect(
            screen,
            color,
            (
                position[0] - 24,
                position[1] + 27,
                min(48, rating_width),
                6
            ),
            border_radius=3
        )

    def draw_side_panel(self, screen):

        panel = pygame.Rect(
            15, 15,
            265, 570
        )

        pygame.draw.rect(
            screen,
            (8, 18, 32),
            panel,
            border_radius=16
        )

        pygame.draw.rect(
            screen,
            (0, 210, 255),
            panel,
            2,
            border_radius=16
        )

        # Boutons formation
        for index, rect in enumerate(
            self.formation_buttons
        ):

            formation = self.formations[index]

            selected = (
                formation == self.formation
            )

            if selected:
                color = (0, 160, 210)
            else:
                color = (20, 40, 60)

            pygame.draw.rect(
                screen,
                color,
                rect,
                border_radius=10
            )

            pygame.draw.rect(
                screen,
                (0, 210, 255),
                rect,
                2,
                border_radius=10
            )

            # Mini représentation tactique
            self.draw_mini_formation(
                screen,
                rect,
                formation
            )

        # Remplaçants
        bench = self.team.get_bench()

        for index, player in enumerate(bench):

            rect = pygame.Rect(
                25,
                365 + index * 38,
                240,
                32
            )

            color = self.player_color(player)

            pygame.draw.rect(
                screen,
                (15, 30, 45),
                rect,
                border_radius=7
            )

            pygame.draw.rect(
                screen,
                color,
                rect,
                2,
                border_radius=7
            )

            pygame.draw.circle(
                screen,
                color,
                (rect.x + 17, rect.centery),
                8
            )

    def draw_mini_formation(
        self,
        screen,
        rect,
        formation
    ):

        mini_field = pygame.Rect(
            rect.x + 150,
            rect.y + 7,
            75,
            41
        )

        pygame.draw.rect(
            screen,
            (10, 70, 45),
            mini_field,
            border_radius=5
        )

        positions = get_positions(
            formation,
            mini_field
        )

        for x, y in positions:

            pygame.draw.circle(
                screen,
                (235, 245, 250),
                (x, y),
                3
            )

    def draw_player_info(self, screen):

        if self.selected_player is None:
            return

        starters = self.team.get_starting_eleven()

        if self.selected_player >= len(starters):
            return

        player = starters[
            self.selected_player
        ]

        panel = pygame.Rect(
            300,
            545,
            560,
            45
        )

        pygame.draw.rect(
            screen,
            (7, 16, 28),
            panel,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            self.player_color(player),
            panel,
            2,
            border_radius=10
        )

        # Informations représentées graphiquement
        stats = [
            player["stats"]["pace"],
            player["stats"]["shooting"],
            player["stats"]["passing"],
            player["stats"]["defense"],
            player["stats"]["physical"]
        ]

        for index, value in enumerate(stats):

            x = 315 + index * 105

            pygame.draw.rect(
                screen,
                (25, 40, 55),
                (x, 562, 80, 8),
                border_radius=4
            )

            pygame.draw.rect(
                screen,
                self.player_color(player),
                (
                    x,
                    562,
                    min(80, int(value * 0.8)),
                    8
                ),
                border_radius=4
            )

    def draw(self, screen):

        self.refresh()

        screen.fill(
            (5, 12, 22)
        )

        self.draw_side_panel(
            screen
        )

        self.draw_field(
            screen
        )

        positions = get_positions(
            self.formation,
            self.field
        )

        starters = self.team.get_starting_eleven()

        for index, player in enumerate(starters):

            if index >= len(positions):
                break

            self.draw_player(
                screen,
                player,
                positions[index],
                selected=(
                    self.selected_player == index
                )
            )

        self.draw_player_info(
            screen
        )

        # Retour
        pygame.draw.rect(
            screen,
            (15, 35, 50),
            self.back_button,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            (0, 210, 255),
            self.back_button,
            2,
            border_radius=10
        )

        # Jouer
        pygame.draw.rect(
            screen,
            (0, 150, 100),
            self.play_button,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            (80, 255, 180),
            self.play_button,
            2,
            border_radius=10
        )
