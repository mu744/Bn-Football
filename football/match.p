import math
import random
import pygame

from football.player import Player
from football.ai import FootballAI
from football.tactics import get_positions
from football.team import Team


class Match:

    def __init__(self, game):

        self.game = game

        # ==========================================
        # TERRAIN
        # ==========================================

        self.field = pygame.Rect(
            70,
            70,
            760,
            460
        )

        # ==========================================
        # EQUIPES
        # ==========================================

        home_id = self.game.save.get(
            "team_id",
            "bnu"
        )

        opponent_id = "ouaga"

        if opponent_id == home_id:
            opponent_id = "sahel"

        self.home_team = Team(home_id)
        self.away_team = Team(opponent_id)

        # ==========================================
        # JOUEURS
        # ==========================================

        self.home_players = []
        self.away_players = []

        self.create_players()

        # ==========================================
        # IA
        # ==========================================

        difficulty = self.game.save.get(
            "difficulty",
            "normal"
        )

        self.ai = FootballAI(
            self.away_team,
            difficulty
        )

        self.ai_controlled_player = None

        # ==========================================
        # CONTROLEUR HUMAIN
        # ==========================================

        self.selected_index = 0

        # ==========================================
        # BALLON
        # ==========================================

        self.ball_x = self.field.centerx
        self.ball_y = self.field.centery

        self.ball_vx = 0.0
        self.ball_vy = 0.0

        self.ball_owner = None

        # ==========================================
        # SCORE
        # ==========================================

        self.home_score = 0
        self.away_score = 0

        # ==========================================
        # TEMPS
        # ==========================================

        self.match_time = 0.0

        # ==========================================
        # POSITION INITIALE
        # ==========================================

        self.reset_positions()

    # ==========================================
    # CREATION DES JOUEURS
    # ==========================================

    def create_players(self):

        home_positions = get_positions(
            self.home_team.formation,
            self.field
        )

        away_positions = get_positions(
            self.away_team.formation,
            self.field
        )

        for i in range(11):

            hx, hy = home_positions[i]

            home_player = Player(
                hx,
                hy,
                "blue",
                i + 1
            )

            self.home_players.append(
                home_player
            )

            ax, ay = away_positions[i]

            mirrored_x = (
                self.field.left +
                self.field.right -
                ax
            )

            away_player = Player(
                mirrored_x,
                ay,
                "red",
                i + 1
            )

            self.away_players.append(
                away_player
            )

    # ==========================================
    # RESET DES POSITIONS
    # ==========================================

    def reset_positions(self):

        positions_home = get_positions(
            self.home_team.formation,
            self.field
        )

        positions_away = get_positions(
            self.away_team.formation,
            self.field
        )

        for i, player in enumerate(
            self.home_players
        ):

            player.x, player.y = (
                positions_home[i]
            )

            player.stop()

        for i, player in enumerate(
            self.away_players
        ):

            x, y = positions_away[i]

            player.x = (
                self.field.left +
                self.field.right -
                x
            )

            player.y = y

            player.stop()

        self.ball_x = self.field.centerx
        self.ball_y = self.field.centery

        self.ball_vx = 0.0
        self.ball_vy = 0.0

        self.ball_owner = None

        self.ai_controlled_player = None

    # ==========================================
    # SELECTION JOUEUR
    # ==========================================

    def select_nearest_player(self):

        if not self.home_players:
            return

        best_index = 0
        best_distance = float("inf")

        for i, player in enumerate(
            self.home_players
        ):

            distance = player.distance_to(
                self.ball_x,
                self.ball_y
            )

            if distance < best_distance:

                best_distance = distance
                best_index = i

        self.selected_index = best_index

    # ==========================================
    # JOUEUR ACTUEL
    # ==========================================

    def get_selected_player(self):

        if not self.home_players:
            return None

        return self.home_players[
            self.selected_index
        ]

    # ==========================================
    # CHANGER DE JOUEUR
    # ==========================================

    def next_player(self):

        if not self.home_players:
            return

        self.selected_index = (
            self.selected_index + 1
        ) % len(self.home_players)

    # ==========================================
    # DEPLACEMENT HUMAIN
    # ==========================================

    def move_selected_player(
        self,
        dx,
        dy
    ):

        player = self.get_selected_player()

        if player is None:
            return

        player.move(
            dx,
            dy,
            self.field
        )

        self.control_ball(
            player
        )

    # ==========================================
    # CONTROLE / CONDUITE DU BALLON
    # ==========================================

    def control_ball(self, player):

        distance = player.distance_to(
            self.ball_x,
            self.ball_y
        )

        # Le joueur doit être suffisamment proche
        if distance > 32:
            return

        self.ball_owner = player

        self.ball_vx = 0.0
        self.ball_vy = 0.0

        # La conduite de balle est progressive.
        self.ball_control_update(
            player
        )

    # ==========================================
    # MISE A JOUR DE LA CONDUITE
    # ==========================================

    def ball_control_update(
        self,
        player
    ):

        if not hasattr(
            player,
            "ball_control"
        ):
            return

        self.ball_x, self.ball_y = (
            player.ball_control.update_ball_position(
                self.ball_x,
                self.ball_y
            )
        )

    # ==========================================
    # PASSE
    # ==========================================

    def pass_ball(self):

        player = self.get_selected_player()

        if player is None:
            return

        if self.ball_owner is not player:
            return

        teammates = [
            p for p in self.home_players
            if p is not player
        ]

        if not teammates:
            return

        # Pour l'instant on garde une passe simple
        # vers le coéquipier disponible le plus proche.

        target = min(
            teammates,
            key=lambda p: player.distance_to(
                p.x,
                p.y
            )
        )

        dx = target.x - player.x
        dy = target.y - player.y

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        if distance <= 0:
            return

        speed = 8.0

        self.ball_vx = (
            dx / distance
        ) * speed

        self.ball_vy = (
            dy / distance
        ) * speed

        self.ball_owner = None

    # ==========================================
    # TIR
    # ==========================================

    def shoot(self):

        player = self.get_selected_player()

        if player is None:
            return

        if self.ball_owner is not player:
            return

        goal_x = self.field.right
        goal_y = self.field.centery

        dx = goal_x - player.x
        dy = goal_y - player.y

        distance = math.sqrt(
            dx * dx +
            dy * dy
        )

        if distance <= 0:
            return

        speed = 13.0

        self.ball_vx = (
            dx / distance
        ) * speed

        self.ball_vy = (
            dy / distance
        ) * speed

        self.ball_owner = None

    # ==========================================
    # IA : CHOIX DU JOUEUR
    # ==========================================

    def ai_choose_player(self):

        player = self.ai.choose_nearest_player(
            self.away_players,
            self.ball_x,
            self.ball_y
        )

        if player is None:
            return

        self.ai_controlled_player = player

    # ==========================================
    # IA : MOUVEMENT
    # ==========================================

    def update_ai(self, delta_time):

        if self.ai_controlled_player is None:

            self.ai_choose_player()

        if self.ai.can_react(
            delta_time
        ):

            self.ai_choose_player()

        player = self.ai_controlled_player

        if player is None:
            return

        if self.ball_owner is None:

            self.ai.chase_ball(
                player,
                self.ball_x,
                self.ball_y,
                self.field
            )

        elif self.ball_owner in self.away_players:

            self.ai_attack()

        else:

            if self.ai.should_press(
                player,
                self.ball_x,
                self.ball_y
            ):

                self.ai.chase_ball(
                    player,
                    self.ball_x,
                    self.ball_y,
                    self.field
                )

    # ==========================================
    # IA : ATTAQUE
    # ==========================================

    def ai_attack(self):

        owner = self.ball_owner

        if owner is None:
            return

        goal_x = self.field.left
        goal_y = self.field.centery

        # Tentative de tir
        if self.ai.should_shoot(
            owner,
            goal_x,
            goal_y
        ):

            dx = goal_x - owner.x
            dy = goal_y - owner.y

            distance = math.sqrt(
                dx * dx +
                dy * dy
            )

            if distance > 0:

                speed = 11.0

                self.ball_vx = (
                    dx / distance
                ) * speed

                self.ball_vy = (
                    dy / distance
                ) * speed

                self.ball_owner = None

                return

        # Tentative de passe
        target = self.ai.choose_pass_target(
            owner,
            self.away_players,
            goal_x
        )

        if target is not None:

            dx = target.x - owner.x
            dy = target.y - owner.y

            distance = math.sqrt(
                dx * dx +
                dy * dy
            )

            if distance > 0:

                speed = 7.5

                self.ball_vx = (
                    dx / distance
                ) * speed

                self.ball_vy = (
                    dy / distance
                ) * speed

                self.ball_owner = None

                return

        # Sinon le joueur avance
        owner.x -= (
            owner.speed *
            self.ai.difficulty[
                "decision_speed"
            ]
        )

        owner.x = max(
            self.field.left +
            owner.radius,
            min(
                self.field.right -
                owner.radius,
                owner.x
            )
        )

    # ==========================================
    # PHYSIQUE DU BALLON
    # ==========================================

    def update_ball(self):

        # ======================================
        # BALLON CONTROLE
        # ======================================

        if self.ball_owner is not None:

            owner = self.ball_owner

            self.ball_control_update(
                owner
            )

            # Vérifie si le joueur a perdu
            # le contrôle du ballon.

            if hasattr(
                owner,
                "ball_control"
            ):

                if owner.ball_control.has_lost_control(
                    self.ball_x,
                    self.ball_y
                ):

                    self.ball_owner = None

            return

        # ======================================
        # BALLON LIBRE
        # ======================================

        self.ball_x += self.ball_vx
        self.ball_y += self.ball_vy

        # Friction
        self.ball_vx *= 0.985
        self.ball_vy *= 0.985

        # ======================================
        # REBONDS VERTICAUX
        # ======================================

        if self.ball_y < self.field.top:

            self.ball_y = self.field.top

            self.ball_vy *= -0.7

        if self.ball_y > self.field.bottom:

            self.ball_y = self.field.bottom

            self.ball_vy *= -0.7

        # ======================================
        # BUT EQUIPE DOMICILE
        # ======================================

        if self.ball_x > self.field.right:

            if abs(
                self.ball_y -
                self.field.centery
            ) < 70:

                self.home_score += 1

                self.reset_positions()

                return

        # ======================================
        # BUT EQUIPE EXTERIEURE
        # ======================================

        if self.ball_x < self.field.left:

            if abs(
                self.ball_y -
                self.field.centery
            ) < 70:

                self.away_score += 1

                self.reset_positions()

                return

        # ======================================
        # LIMITE DU BALLON
        # ======================================

        self.ball_x = max(
            self.field.left - 30,
            min(
                self.field.right + 30,
                self.ball_x
            )
        )

    # ==========================================
    # POSSESSION
    # ==========================================

    def update_possession(self):

        if self.ball_owner is not None:
            return

        all_players = (
            self.home_players +
            self.away_players
        )

        closest = None
        closest_distance = float("inf")

        for player in all_players:

            distance = player.distance_to(
                self.ball_x,
                self.ball_y
            )

            if distance < closest_distance:

                closest_distance = distance
                closest = player

        if (
            closest is not None
            and closest_distance < 24
        ):

            self.ball_owner = closest

    # ==========================================
    # MISE A JOUR GENERALE
    # ==========================================

    def update(self):

        delta_time = (
            self.game.clock.get_time()
            / 1000.0
        )

        self.match_time += delta_time

        self.update_ai(
            delta_time
        )

        self.update_ball()

        self.update_possession()

    # ==========================================
    # DESSIN
    # ==========================================

    def draw(self, screen):

        # ======================================
        # PELOUSE
        # ======================================

        screen.fill(
            (8, 100, 45)
        )

        # ======================================
        # TERRAIN
        # ======================================

        pygame.draw.rect(
            screen,
            (235, 235, 235),
            self.field,
            4
        )

        # Ligne centrale
        pygame.draw.line(
            screen,
            (235, 235, 235),
            (
                self.field.centerx,
                self.field.top
            ),
            (
                self.field.centerx,
                self.field.bottom
            ),
            3
        )

        # Cercle central
        pygame.draw.circle(
            screen,
            (235, 235, 235),
            self.field.center,
            70,
            3
        )

        # Surface gauche
        pygame.draw.rect(
            screen,
            (235, 235, 235),
            (
                self.field.left,
                self.field.centery - 100,
                120,
                200
            ),
            3
        )

        # Surface droite
        pygame.draw.rect(
            screen,
            (235, 235, 235),
            (
                self.field.right - 120,
                self.field.centery - 100,
                120,
                200
            ),
            3
        )

        # ======================================
        # JOUEURS
        # ======================================

        for player in self.home_players:

            player.draw(screen)

        for player in self.away_players:

            player.draw(screen)

        # ======================================
        # JOUEUR SELECTIONNE
        # ======================================

        selected = self.get_selected_player()

        if selected is not None:

            pygame.draw.circle(
                screen,
                (255, 230, 60),
                (
                    int(selected.x),
                    int(selected.y)
                ),
                selected.radius + 5,
                3
            )

        # ======================================
        # BALLON
        # ======================================

        pygame.draw.circle(
            screen,
            (250, 250, 250),
            (
                int(self.ball_x),
                int(self.ball_y)
            ),
            7
        )

        pygame.draw.circle(
            screen,
            (20, 20, 20),
            (
                int(self.ball_x),
                int(self.ball_y)
            ),
            7,
            2
        )

        # ======================================
        # SCORE
        # ======================================

        pygame.draw.rect(
            screen,
            (5, 15, 25),
            (
                340,
                10,
                220,
                45
            ),
            border_radius=10
        )

        # Score domicile
        for i in range(
            min(
                self.home_score,
                5
            )
        ):

            pygame.draw.circle(
                screen,
                (30, 130, 240),
                (
                    365 + i * 25,
                    32
                ),
                6
            )

        # Score extérieur
        for i in range(
            min(
                self.away_score,
                5
            )
        ):

            pygame.draw.circle(
                screen,
                (220, 60, 70),
                (
                    455 + i * 25,
                    32
                ),
                6
            )
