import pygame
import math

from football.team import Team
from football.player import Player


class Match:

    def __init__(self, game):

        self.game = game

        self.field = pygame.Rect(
            45, 80, 810, 440
        )

        self.home_team = Team(
            self.game.save.get("team_id", "bnu")
        )

        opponent_id = "ouaga"

        if opponent_id == self.home_team.id:
            opponent_id = "sahel"

        self.away_team = Team(opponent_id)

        self.home_players = []
        self.away_players = []

        self.selected_index = 9

        self.ball_x = 450
        self.ball_y = 300

        self.ball_vx = 0
        self.ball_vy = 0

        self.ball_radius = 9

        self.ball_owner = None

        self.home_score = 0
        self.away_score = 0

        self.kick_cooldown = 0

        self.pass_cooldown = 0

        self.create_players()

    # ==================================================
    # JOUEURS
    # ==================================================

    def create_players(self):

        self.home_players.clear()
        self.away_players.clear()

        home_positions = self.get_formation_positions(
            self.home_team.formation,
            True
        )

        away_positions = self.get_formation_positions(
            self.away_team.formation,
            False
        )

        starters_home = self.home_team.get_starting_eleven()
        starters_away = self.away_team.get_starting_eleven()

        for index, data in enumerate(starters_home):

            x, y = home_positions[index]

            player = Player(
                x,
                y,
                "blue",
                data["number"]
            )

            player.player_data = data

            self.home_players.append(player)

        for index, data in enumerate(starters_away):

            x, y = away_positions[index]

            player = Player(
                x,
                y,
                "red",
                data["number"]
            )

            player.player_data = data

            self.away_players.append(player)

    # ==================================================
    # FORMATIONS
    # ==================================================

    def get_formation_positions(
        self,
        formation,
        home
    ):

        formations = {

            "4-3-3": [
                (0.50, 0.90),

                (0.18, 0.72),
                (0.38, 0.76),
                (0.62, 0.76),
                (0.82, 0.72),

                (0.28, 0.56),
                (0.50, 0.60),
                (0.72, 0.56),

                (0.18, 0.32),
                (0.50, 0.26),
                (0.82, 0.32)
            ],

            "4-4-2": [
                (0.50, 0.90),

                (0.18, 0.72),
                (0.38, 0.76),
                (0.62, 0.76),
                (0.82, 0.72),

                (0.18, 0.54),
                (0.38, 0.58),
                (0.62, 0.58),
                (0.82, 0.54),

                (0.40, 0.30),
                (0.60, 0.30)
            ],

            "4-2-3-1": [
                (0.50, 0.90),

                (0.18, 0.72),
                (0.38, 0.76),
                (0.62, 0.76),
                (0.82, 0.72),

                (0.38, 0.58),
                (0.62, 0.58),

                (0.22, 0.38),
                (0.50, 0.34),
                (0.78, 0.38),

                (0.50, 0.22)
            ]
        }

        positions = formations.get(
            formation,
            formations["4-3-3"]
        )

        result = []

        for nx, ny in positions:

            x = int(
                self.field.left +
                self.field.width * nx
            )

            if home:

                y = int(
                    self.field.top +
                    self.field.height * ny
                )

            else:

                y = int(
                    self.field.bottom -
                    self.field.height * ny
                )

            result.append((x, y))

        return result

    # ==================================================
    # CHANGEMENT DE JOUEUR
    # ==================================================

    def select_nearest_player(self):

        if not self.home_players:
            return

        best_index = 0
        best_distance = float("inf")

        for index, player in enumerate(
            self.home_players
        ):

            distance = player.distance_to(
                self.ball_x,
                self.ball_y
            )

            if distance < best_distance:

                best_distance = distance
                best_index = index

        self.selected_index = best_index

    def next_player(self):

        if not self.home_players:
            return

        self.selected_index = (
            self.selected_index + 1
        ) % len(self.home_players)

    # ==================================================
    # DEPLACEMENT
    # ==================================================

    def move_selected_player(
        self,
        dx,
        dy
    ):

        if not self.home_players:
            return

        player = self.home_players[
            self.selected_index
        ]

        player.move(
            dx,
            dy,
            self.field
        )

    # ==================================================
    # CONTROLE DU BALLON
    # ==================================================

    def control_ball(self):

        if not self.home_players:
            return

        player = self.home_players[
            self.selected_index
        ]

        distance = player.distance_to(
            self.ball_x,
            self.ball_y
        )

        # Récupération automatique
        if distance < 30:

            self.ball_owner = self.selected_index

            self.ball_x = (
                player.x +
                player.direction_x * 22
            )

            self.ball_y = (
                player.y +
                player.direction_y * 22
            )

            self.ball_vx = 0
            self.ball_vy = 0

    # ==================================================
    # PASSE
    # ==================================================

    def pass_ball(self):

        if self.pass_cooldown > 0:
            return

        if self.ball_owner != self.selected_index:
            return

        current = self.home_players[
            self.selected_index
        ]

        teammates = []

        for index, player in enumerate(
            self.home_players
        ):

            if index == self.selected_index:
                continue

            distance = current.distance_to(
                player.x,
                player.y
            )

            teammates.append(
                (distance, index, player)
            )

        if not teammates:
            return

        # On choisit le coéquipier devant
        # le joueur actuel en priorité.
        best = None
        best_score = -999999

        for distance, index, player in teammates:

            forward = (
                player.y - current.y
            )

            score = (
                -distance
                + forward * 0.4
            )

            if score > best_score:

                best_score = score
                best = player

        if best is None:
            return

        dx = best.x - current.x
        dy = best.y - current.y

        length = math.sqrt(
            dx * dx +
            dy * dy
        )

        if length == 0:
            return

        dx /= length
        dy /= length

        self.ball_owner = None

        self.ball_x = current.x
        self.ball_y = current.y

        self.ball_vx = dx * 9
        self.ball_vy = dy * 9

        self.pass_cooldown = 18

    # ==================================================
    # TIR
    # ==================================================

    def shoot(self):

        if self.kick_cooldown > 0:
            return

        if self.ball_owner != self.selected_index:
            return

        player = self.home_players[
            self.selected_index
        ]

        # Direction vers le but adverse
        dx = 0
        dy = -1

        # Si le joueur regarde déjà quelque part,
        # on utilise sa direction.
        if (
            abs(player.direction_x) > 0.1
            or abs(player.direction_y) > 0.1
        ):

            dx = player.direction_x
            dy = player.direction_y

        length = math.sqrt(
            dx * dx +
            dy * dy
        )

        if length == 0:
            dy = -1
        else:
            dx /= length
            dy /= length

        self.ball_owner = None

        self.ball_x = player.x
        self.ball_y = player.y

        self.ball_vx = dx * 12
        self.ball_vy = dy * 12

        self.kick_cooldown = 20

    # ==================================================
    # BALLON
    # ==================================================

    def update_ball(self):

        if self.ball_owner is not None:
            return

        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy

        self.ball_vx *= 0.97
        self.ball_vy *= 0.97

        if self.ball_y < self.field.top:

            self.ball_y = self.field.top
            self.ball_vy *= -0.7

        if self.ball_y > self.field.bottom:

            self.ball_y = self.field.bottom
            self.ball_vy *= -0.7

        # But adverse
        if self.ball_x < self.field.left:

            if (
                self.field.top + 120
                <
                self.ball_y
                <
                self.field.bottom - 120
            ):

                self.away_score += 1
                self.reset_ball()

            else:

                self.ball_x = self.field.left
                self.ball_vx *= -0.7

        # But joueur
        if self.ball_x > self.field.right:

            if (
                self.field.top + 120
                <
                self.ball_y
                <
                self.field.bottom - 120
            ):

                self.home_score += 1
                self.reset_ball()

            else:

                self.ball_x = self.field.right
                self.ball_vx *= -0.7

    # ==================================================
    # IA
    # ==================================================

    def update_ai(self):

        if not self.away_players:
            return

        closest = min(
            self.away_players,
            key=lambda p:
            p.distance_to(
                self.ball_x,
                self.ball_y
            )
        )

        distance = closest.distance_to(
            self.ball_x,
            self.ball_y
        )

        if distance < 28:

            # Interception
            self.ball_owner = None

            dx = -1
            dy = 0

            self.ball_vx = dx * 6
            self.ball_vy = dy

            return

        dx = self.ball_x - closest.x
        dy = self.ball_y - closest.y

        length = math.sqrt(
            dx * dx +
            dy * dy
        )

        if length > 0:

            dx /= length
            dy /= length

            closest.move(
                dx,
                dy,
                self.field
            )

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self):

        if self.kick_cooldown > 0:
            self.kick_cooldown -= 1

        if self.pass_cooldown > 0:
            self.pass_cooldown -= 1

        self.control_ball()

        self.update_ai()

        self.update_ball()

    # ==================================================
    # RESET
    # ==================================================

    def reset_ball(self):

        self.ball_x = self.field.centerx
        self.ball_y = self.field.centery

        self.ball_vx = 0
        self.ball_vy = 0

        self.ball_owner = None

        self.create_players()

        self.selected_index = 9

    # ==================================================
    # AFFICHAGE
    # ==================================================

    def draw_field(self, screen):

        pygame.draw.rect(
            screen,
            (25, 120, 65),
            self.field
        )

        pygame.draw.rect(
            screen,
            (235, 245, 240),
            self.field,
            4
        )

        pygame.draw.line(
            screen,
            (235, 245, 240),
            (
                self.field.left,
                self.field.centery
            ),
            (
                self.field.right,
                self.field.centery
            ),
            3
        )

        pygame.draw.circle(
            screen,
            (235, 245, 240),
            self.field.center,
            65,
            3
        )

        top_area = pygame.Rect(
            self.field.centerx - 150,
            self.field.top,
            300,
            115
        )

        bottom_area = pygame.Rect(
            self.field.centerx - 150,
            self.field.bottom - 115,
            300,
            115
        )

        pygame.draw.rect(
            screen,
            (235, 245, 240),
            top_area,
            3
        )

        pygame.draw.rect(
            screen,
            (235, 245, 240),
            bottom_area,
            3
        )

    def draw_player(
        self,
        screen,
        player,
        selected=False
    ):

        if player.team == "blue":
            color = (25, 120, 245)
        else:
            color = (225, 65, 75)

        if selected:

            pygame.draw.circle(
                screen,
                (255, 220, 50),
                (
                    int(player.x),
                    int(player.y)
                ),
                27,
                3
            )

        pygame.draw.circle(
            screen,
            color,
            (
                int(player.x),
                int(player.y)
            ),
            18
        )

        pygame.draw.circle(
            screen,
            (245, 245, 245),
            (
                int(player.x),
                int(player.y)
            ),
            5
        )

    def draw_score(self, screen):

        panel = pygame.Rect(
            330, 20,
            240, 45
        )

        pygame.draw.rect(
            screen,
            (5, 15, 25),
            panel,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            (0, 210, 255),
            panel,
            2,
            border_radius=12
        )

        # Score sous forme de points
        for i in range(
            min(self.home_score, 8)
        ):

            pygame.draw.circle(
                screen,
                (0, 210, 255),
                (370 + i * 18, 42),
                5
            )

        pygame.draw.line(
            screen,
            (220, 220, 220),
            (445, 30),
            (445, 55),
            2
        )

        for i in range(
            min(self.away_score, 8)
        ):

            pygame.draw.circle(
                screen,
                (255, 80, 90),
                (500 + i * 18, 42),
                5
            )

    def draw(self, screen):

        screen.fill(
            (4, 12, 20)
        )

        self.draw_field(
            screen
        )

        for index, player in enumerate(
            self.home_players
        ):

            self.draw_player(
                screen,
                player,
                selected=(
                    index ==
                    self.selected_index
                )
            )

        for player in self.away_players:

            self.draw_player(
                screen,
                player
            )

        pygame.draw.circle(
            screen,
            (250, 250, 250),
            (
                int(self.ball_x),
                int(self.ball_y)
            ),
            self.ball_radius
        )

        pygame.draw.circle(
            screen,
            (30, 30, 30),
            (
                int(self.ball_x),
                int(self.ball_y)
            ),
            self.ball_radius,
            2
        )

        self.draw_score(
            screen
        )
