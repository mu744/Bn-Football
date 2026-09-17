import math
import pygame

from football.player import Player
from football.ai import FootballAI
from football.tactics import get_positions
from football.team import Team
from football.defense import DefenseController
from football.goalkeeper import GoalkeeperController

from football.gameplay.control_system import ControlSystem
from football.gameplay.pass_system import PassSystem
from football.gameplay.shoot_system import ShootSystem
from football.gameplay.tackle_system import TackleSystem
from football.gameplay.power_system import PowerSystem
from football.gameplay.ball_physics import BallPhysics
from football.gameplay.player_controller import PlayerController
from football.gameplay.action_controller import ActionController

from controls.mobile_controls import MobileControls
from football.gameplay.input_manager import InputManager

from football.system_registry import SystemRegistry
from football.match_controller import MatchController
from football.match_context import MatchContext


class Match:
    """
    BN-Football
    ===========
    Contrôleur principal d'un match.

    Cette classe constitue le point de liaison entre :

    - joueurs
    - équipes
    - ballon
    - physique
    - gameplay
    - IA
    - tactiques
    - défense
    - gardiens
    - endurance
    - fatigue
    - contrôles clavier/tactiles
    - statistiques
    - arbitre
    - remplacements
    - coups de pied arrêtés
    - architecture future 3D

    L'objectif est de conserver cette classe stable pendant
    les prochaines étapes du projet.
    """

    # ==========================================================
    # INITIALISATION
    # ==========================================================

    def __init__(self, game):

        self.game = game

        # ------------------------------------------------------
        # ÉTAT DU MATCH
        # ------------------------------------------------------

        self.paused = False
        self.finished = False

        self.match_phase = "first_half"
        self.match_result = None

        self.match_time = 0.0
        self.match_duration = 90.0

        # ------------------------------------------------------
        # TERRAIN
        # ------------------------------------------------------

        self.field = pygame.Rect(
            70,
            70,
            760,
            460
        )

        # ------------------------------------------------------
        # ÉQUIPES
        # ------------------------------------------------------

        home_id = self.game.save.get(
            "team_id",
            "bnu"
        )

        opponent_id = "ouaga"

        if opponent_id == home_id:
            opponent_id = "sahel"

        self.home_team = Team(home_id)
        self.away_team = Team(opponent_id)

        # ------------------------------------------------------
        # JOUEURS
        # ------------------------------------------------------

        self.home_players = []
        self.away_players = []

        self.goalkeepers = []

        # ------------------------------------------------------
        # BALLON
        # ------------------------------------------------------

        self.ball_x = float(
            self.field.centerx
        )

        self.ball_y = float(
            self.field.centery
        )

        self.ball_vx = 0.0
        self.ball_vy = 0.0

        self.ball_owner = None

        # ------------------------------------------------------
        # SCORE
        # ------------------------------------------------------

        self.home_score = 0
        self.away_score = 0

        # ------------------------------------------------------
        # DIFFICULTÉ
        # ------------------------------------------------------

        self.difficulty = self.game.save.get(
            "difficulty",
            "normal"
        )

        # ------------------------------------------------------
        # SÉLECTION JOUEUR
        # ------------------------------------------------------

        self.selected_index = 0

        # ------------------------------------------------------
        # COMPATIBILITÉ FUTURE
        # ------------------------------------------------------

        self.graphics_mode = self.game.save.get(
            "graphics_mode",
            "standard"
        )

        self.renderer = None
        self.camera = None

        # ------------------------------------------------------
        # CRÉATION DES JOUEURS
        # ------------------------------------------------------

        self.create_players()

        # ------------------------------------------------------
        # IA DE BASE
        # ------------------------------------------------------

        self.ai = FootballAI(
            self,
            self.difficulty
        )

        self.football_ai = self.ai

        self.ai_controlled_player = None

        # ------------------------------------------------------
        # SYSTÈMES DE BASE
        # ------------------------------------------------------

        self.control_system = ControlSystem(self)

        self.pass_system = PassSystem(self)

        self.shoot_system = ShootSystem(self)

        self.tackle_system = TackleSystem(self)

        self.power_system = PowerSystem()

        self.ball_physics = BallPhysics(self)

        # ------------------------------------------------------
        # CONTRÔLE DU JOUEUR
        # ------------------------------------------------------

        self.action_controller = ActionController(
            self
        )

        self.player_controller = PlayerController(
            self,
            self.action_controller
        )

        # ------------------------------------------------------
        # CONTRÔLES MOBILES
        # ------------------------------------------------------

        self.mobile_controls = MobileControls(
            self,
            900,
            600
        )

        # ------------------------------------------------------
        # GESTIONNAIRE D'ENTRÉES CENTRAL
        # ------------------------------------------------------

        self.input_manager = InputManager(
            self,
            self.mobile_controls
        )

        # ------------------------------------------------------
        # DÉFENSE LEGACY / COMPATIBILITÉ
        # ------------------------------------------------------

        self.defense = DefenseController(
            self
        )

        # ------------------------------------------------------
        # CHARGE DE PUISSANCE
        # ------------------------------------------------------

        self.charging_action = None

        self.charging_pass_type = "normal"

        self.previous_power_keys = set()

        # ------------------------------------------------------
        # ARCHITECTURE CENTRALE
        # ------------------------------------------------------

        self.system_registry = SystemRegistry(
            self
        )

        self.system_registry.initialize()

        self.context = MatchContext(
            self
        )

        self.match_controller = MatchController(
            self
        )

        # ------------------------------------------------------
        # BRANCHEMENT DES CONTRÔLES
        # ------------------------------------------------------

        self.match_controller.attach_controls(
            self.mobile_controls,
            self.player_controller
        )

        self.match_controller.attach_input_manager(
            self.input_manager
        )

        self.match_controller.attach_action_controller(
            self.action_controller
        )

        # ------------------------------------------------------
        # POSITION INITIALE
        # ------------------------------------------------------

        self.reset_positions()

        self.select_nearest_player()

    # ==========================================================
    # CRÉATION DES JOUEURS
    # ==========================================================

    def create_players(self):

        self.home_players.clear()
        self.away_players.clear()
        self.goalkeepers.clear()

        home_positions = get_positions(
            self.home_team.formation,
            self.field
        )

        away_positions = get_positions(
            self.away_team.formation,
            self.field
        )

        # ------------------------------------------------------
        # ÉQUIPE DOMICILE
        # ------------------------------------------------------

        for i in range(11):

            hx, hy = home_positions[i]

            player = Player(
                hx,
                hy,
                "blue",
                i + 1
            )

            if i < len(self.home_team.players):

                data = self.home_team.players[i]

                player.rating = data["rating"]
                player.position = data["position"]

                player.control_rating = data[
                    "stats"
                ].get(
                    "passing",
                    75
                )

                player.heading_rating = data[
                    "stats"
                ].get(
                    "physical",
                    75
                )

                player.volley_rating = data[
                    "stats"
                ].get(
                    "shooting",
                    70
                )

                player.physical = data[
                    "stats"
                ].get(
                    "physical",
                    70
                )

            else:

                player.rating = 70
                player.position = "MC"
                player.physical = 70
                player.control_rating = 70
                player.heading_rating = 70
                player.volley_rating = 70

            player.on_pitch = True
            player.is_sprinting = False

            self.home_players.append(
                player
            )

        # ------------------------------------------------------
        # ÉQUIPE EXTÉRIEURE
        # ------------------------------------------------------

        for i in range(11):

            ax, ay = away_positions[i]

            mirrored_x = (
                self.field.left
                + self.field.right
                - ax
            )

            player = Player(
                mirrored_x,
                ay,
                "red",
                i + 1
            )

            if i < len(self.away_team.players):

                data = self.away_team.players[i]

                player.rating = data["rating"]
                player.position = data["position"]

                player.control_rating = data[
                    "stats"
                ].get(
                    "passing",
                    75
                )

                player.heading_rating = data[
                    "stats"
                ].get(
                    "physical",
                    75
                )

                player.volley_rating = data[
                    "stats"
                ].get(
                    "shooting",
                    70
                )

                player.physical = data[
                    "stats"
                ].get(
                    "physical",
                    70
                )

            else:

                player.rating = 70
                player.position = "MC"
                player.physical = 70
                player.control_rating = 70
                player.heading_rating = 70
                player.volley_rating = 70

            player.on_pitch = True
            player.is_sprinting = False

            self.away_players.append(
                player
            )

        # ------------------------------------------------------
        # GARDIENS
        # ------------------------------------------------------

        if self.home_players:

            goalkeeper_player = (
                self.home_players[0]
            )

            goalkeeper_player.position = "GK"
            goalkeeper_player.role = "GK"

            self.goalkeepers.append(
                GoalkeeperController(
                    goalkeeper_player,
                    self
                )
            )

        if self.away_players:

            goalkeeper_player = (
                self.away_players[0]
            )

            goalkeeper_player.position = "GK"
            goalkeeper_player.role = "GK"

            self.goalkeepers.append(
                GoalkeeperController(
                    goalkeeper_player,
                    self
                )
            )

    # ==========================================================
    # RÉINITIALISATION DES POSITIONS
    # ==========================================================

    def reset_positions(self):

        home_positions = get_positions(
            self.home_team.formation,
            self.field
        )

        away_positions = get_positions(
            self.away_team.formation,
            self.field
        )

        # ------------------------------------------------------
        # JOUEURS DOMICILE
        # ------------------------------------------------------

        for i, player in enumerate(
            self.home_players
        ):

            if i >= len(home_positions):
                continue

            player.x, player.y = (
                home_positions[i]
            )

            player.stop()

            player.stamina = 100.0
            player.is_sprinting = False
            player.on_pitch = True

        # ------------------------------------------------------
        # JOUEURS EXTÉRIEURS
        # ------------------------------------------------------

        for i, player in enumerate(
            self.away_players
        ):

            if i >= len(away_positions):
                continue

            x, y = away_positions[i]

            player.x = (
                self.field.left
                + self.field.right
                - x
            )

            player.y = y

            player.stop()

            player.stamina = 100.0
            player.is_sprinting = False
            player.on_pitch = True

        # ------------------------------------------------------
        # BALLON
        # ------------------------------------------------------

        self.ball_x = float(
            self.field.centerx
        )

        self.ball_y = float(
            self.field.centery
        )

        self.ball_vx = 0.0
        self.ball_vy = 0.0

        self.ball_owner = None

        # ------------------------------------------------------
        # IA
        # ------------------------------------------------------

        self.ai_controlled_player = None

        # ------------------------------------------------------
        # PUISSANCE
        # ------------------------------------------------------

        self.cancel_power_action()

        # ------------------------------------------------------
        # PHYSIQUE
        # ------------------------------------------------------

        if hasattr(
            self,
            "ball_physics"
        ):

            self.ball_physics.reset()

        # ------------------------------------------------------
        # SYSTÈMES
        # ------------------------------------------------------

        if hasattr(
            self,
            "dribble_system"
        ) and self.dribble_system:

            self.dribble_system.reset()

        if hasattr(
            self,
            "ball_protection"
        ) and self.ball_protection:

            self.ball_protection.reset()

        if hasattr(
            self,
            "stamina_system"
        ) and self.stamina_system:

            if hasattr(
                self.stamina_system,
                "reset"
            ):
                self.stamina_system.reset()

        if hasattr(
            self,
            "fatigue_effects"
        ) and self.fatigue_effects:

            if hasattr(
                self.fatigue_effects,
                "reset"
            ):
                self.fatigue_effects.reset()

        # ------------------------------------------------------
        # CONTRÔLEUR
        # ------------------------------------------------------

        if hasattr(
            self,
            "action_controller"
        ):

            self.action_controller.reset()

            self.action_controller.select_nearest_to_ball()

        # ------------------------------------------------------
        # GARDIENS
        # ------------------------------------------------------

        for goalkeeper in self.goalkeepers:

            goalkeeper.home_x = (
                goalkeeper.player.x
            )

            goalkeeper.home_y = (
                goalkeeper.player.y
            )

            if hasattr(
                goalkeeper,
                "save_cooldown"
            ):
                goalkeeper.save_cooldown = 0.0

            if hasattr(
                goalkeeper,
                "cooldown"
            ):
                goalkeeper.cooldown = 0.0

            goalkeeper.reset()

    # ==========================================================
    # JOUEUR SÉLECTIONNÉ
    # ==========================================================

    def select_nearest_player(self):

        players = [
            p
            for p in self.home_players
            if getattr(
                p,
                "on_pitch",
                True
            )
        ]

        if not players:
            return None

        closest = min(
            players,
            key=lambda p: math.sqrt(
                (p.x - self.ball_x) ** 2
                +
                (p.y - self.ball_y) ** 2
            )
        )

        self.selected_index = (
            self.home_players.index(
                closest
            )
        )

        self.action_controller.select_player(
            closest
        )

        return closest

    def get_selected_player(self):

        selected = getattr(
            self.action_controller,
            "selected_player",
            None
        )

        if (
            selected is not None
            and getattr(
                selected,
                "on_pitch",
                True
            )
            and selected in self.home_players
        ):

            self.selected_index = (
                self.home_players.index(
                    selected
                )
            )

            return selected

        players = [
            p
            for p in self.home_players
            if getattr(
                p,
                "on_pitch",
                True
            )
        ]

        if not players:
            return None

        if (
            self.selected_index < 0
            or self.selected_index >= len(
                self.home_players
            )
        ):

            self.selected_index = 0

        player = self.home_players[
            self.selected_index
        ]

        if not getattr(
            player,
            "on_pitch",
            True
        ):

            return self.select_nearest_player()

        self.action_controller.select_player(
            player
        )

        return player

    def next_player(self):

        players = [
            p
            for p in self.home_players
            if getattr(
                p,
                "on_pitch",
                True
            )
        ]

        if not players:
            return None

        current = self.get_selected_player()

        if current not in players:

            return self.select_nearest_player()

        index = players.index(
            current
        )

        index = (
            index + 1
        ) % len(players)

        selected = players[index]

        self.action_controller.select_player(
            selected
        )

        self.selected_index = (
            self.home_players.index(
                selected
            )
        )

        return selected

    # ==========================================================
    # CONTRÔLE DU BALLON
    # ==========================================================

    def control_ball(self, player):

        if player is None:
            return False

        return self.control_system.take_ball(
            player
        )

    # ==========================================================
    # PASSES
    # ==========================================================

    def pass_ball(self, power=None):

        player = self.get_selected_player()

        if player is None:
            return False

        return self.pass_system.normal_pass(
            player,
            power
        )

    def short_pass(self, power=None):

        player = self.get_selected_player()

        if player is None:
            return False

        return self.pass_system.short_pass(
            player,
            power
        )

    def long_pass(self, power=None):

        player = self.get_selected_player()

        if player is None:
            return False

        return self.pass_system.long_pass(
            player,
            power
        )

    def directional_pass(
        self,
        direction_x,
        direction_y,
        power=None
    ):

        player = self.get_selected_player()

        if player is None:
            return False

        return self.pass_system.directional_pass(
            player,
            direction_x,
            direction_y,
            power
        )

    # ==========================================================
    # PASSE EN PROFONDEUR
    # ==========================================================

    def through_ball(self, target=None):

        player = self.get_selected_player()

        if player is None:
            return False

        teammates = [
            p
            for p in self.home_players
            if (
                p is not player
                and getattr(
                    p,
                    "on_pitch",
                    True
                )
            )
        ]

        if not teammates:
            return False

        if target is None:

            target = min(
                teammates,
                key=lambda p:
                abs(p.x - player.x)
                +
                abs(p.y - player.y)
            )

        gameplay = self.context.get(
            "gameplay"
        )

        if gameplay is None:
            return False

        return gameplay.pass_through(
            player,
            target
        )

    # ==========================================================
    # TIRS
    # ==========================================================

    def shoot(self, power=None):

        player = self.get_selected_player()

        if player is None:
            return False

        return self.shoot_system.normal_shot(
            player,
            power
        )

    def low_shot(self, power=None):

        player = self.get_selected_player()

        if player is None:
            return False

        return self.shoot_system.low_shot(
            player,
            power
        )

    def strong_shot(self, power=None):

        player = self.get_selected_player()

        if player is None:
            return False

        return self.shoot_system.strong_shot(
            player,
            power
        )

    def targeted_shot(
        self,
        target_y,
        power=None
    ):

        player = self.get_selected_player()

        if player is None:
            return False

        return self.shoot_system.targeted_shot(
            player,
            target_y,
            power
        )

    # ==========================================================
    # DRIBBLE / PROTECTION
    # ==========================================================

    def protect_ball(self):

        player = self.get_selected_player()

        if player is None:
            return False

        system = getattr(
            self,
            "dribble_system",
            None
        )

        if system is not None:

            return system.protect_ball(
                player
            )

        system = getattr(
            self,
            "ball_protection",
            None
        )

        if system is not None:

            return system.update()

        return False

    # ==========================================================
    # TACLE
    # ==========================================================

    def tackle(self):

        player = self.get_selected_player()

        if player is None:
            return False

        return self.tackle_system.tackle(
            player
        )

    def sliding_tackle(self):

        player = self.get_selected_player()

        if player is None:
            return False

        return self.defense.sliding_tackle(
            player
        )

    def intercept(self):

        player = self.get_selected_player()

        if player is None:
            return False

        return self.tackle_system.intercept(
            player
        )

    # ==========================================================
    # MOUVEMENT
    # ==========================================================

    def move_selected_player(
        self,
        dx,
        dy,
        sprint=False
    ):

        player = self.get_selected_player()

        if player is None:
            return False

        player.is_sprinting = bool(
            sprint
        )

        return self.action_controller.move_selected_player(
            dx,
            dy,
            sprint
        )

    # ==========================================================
    # CHARGE DE PUISSANCE
    # ==========================================================

    def start_power_action(
        self,
        action,
        pass_type="normal"
    ):

        player = self.get_selected_player()

        if player is None:
            return False

        if self.ball_owner is not player:
            return False

        if self.charging_action is not None:
            return False

        if not self.power_system.start(
            action
        ):
            return False

        self.charging_action = action

        self.charging_pass_type = (
            pass_type
        )

        return True

    def cancel_power_action(self):

        if hasattr(
            self,
            "power_system"
        ):

            self.power_system.cancel()

        self.charging_action = None

        self.charging_pass_type = (
            "normal"
        )

    def release_power_action(self):

        if self.charging_action is None:
            return

        action, power = (
            self.power_system.release()
        )

        self.charging_action = None

        if action is None:

            self.charging_pass_type = (
                "normal"
            )

            return

        if action == "pass":

            if (
                self.charging_pass_type
                == "short"
            ):

                self.short_pass(power)

            elif (
                self.charging_pass_type
                == "long"
            ):

                self.long_pass(power)

            else:

                self.pass_ball(power)

        elif action == "shoot":

            if (
                self.charging_pass_type
                == "strong"
            ):

                self.strong_shot(power)

            else:

                self.shoot(power)

        self.charging_pass_type = (
            "normal"
        )

    # ==========================================================
    # COMMANDES DE PUISSANCE
    # ==========================================================

    def handle_power_input(self):

        keys = pygame.key.get_pressed()

        # ------------------------------------------------------
        # Touches utilisées uniquement pour les variantes
        # chargées afin d'éviter les doubles commandes.
        # ------------------------------------------------------

        power_keys = {
            pygame.K_o,
            pygame.K_l,
            pygame.K_e
        }

        current = set()

        for key in power_keys:

            if keys[key]:
                current.add(key)

        pressed = (
            current
            - self.previous_power_keys
        )

        released = (
            self.previous_power_keys
            - current
        )

        # Passe courte chargée
        if pygame.K_o in pressed:

            self.start_power_action(
                "pass",
                "short"
            )

        # Passe longue chargée
        if pygame.K_l in pressed:

            self.start_power_action(
                "pass",
                "long"
            )

        # Tir puissant chargé
        if pygame.K_e in pressed:

            self.start_power_action(
                "shoot",
                "strong"
            )

        # Relâchement
        if released:

            self.release_power_action()

        # Protection ballon
        if keys[pygame.K_q]:

            self.protect_ball()

        self.previous_power_keys = current

    # ==========================================================
    # IA
    # ==========================================================

    def ai_choose_player(self):

        players = [
            p
            for p in self.away_players
            if getattr(
                p,
                "on_pitch",
                True
            )
        ]

        if not players:

            self.ai_controlled_player = None

            return

        player = self.ai.nearest_player(
            players,
            self.ball_x,
            self.ball_y
        )

        if player is not None:

            self.ai_controlled_player = (
                player
            )

    # ==========================================================
    # GARDIENS
    # ==========================================================

    def update_goalkeepers(
        self,
        delta_time
    ):

        for goalkeeper in self.goalkeepers:

            try:

                goalkeeper.update(
                    delta_time
                )

            except TypeError:

                try:

                    goalkeeper.update()

                except (
                    AttributeError,
                    TypeError
                ):

                    pass

    # ==========================================================
    # DÉTECTION DES BUTS
    # ==========================================================

    def is_ball_in_goal_mouth(self):

        goal_half_width = 55.0

        return (
            abs(
                self.ball_y
                -
                self.field.centery
            )
            <= goal_half_width
        )

    def predict_goal(self):

        if self.ball_owner is not None:
            return None

        next_x = (
            self.ball_x
            +
            self.ball_vx
        )

        # ------------------------------------------------------
        # BUT À DROITE
        # ------------------------------------------------------

        if (
            next_x > self.field.right
            and self.ball_vx > 0
            and self.is_ball_in_goal_mouth()
        ):

            return "home"

        # ------------------------------------------------------
        # BUT À GAUCHE
        # ------------------------------------------------------

        if (
            next_x < self.field.left
            and self.ball_vx < 0
            and self.is_ball_in_goal_mouth()
        ):

            return "away"

        return None

    def register_goal(self, side):

        if side == "home":

            self.home_score += 1

        elif side == "away":

            self.away_score += 1

        self.reset_positions()

        return True

    def check_goals(self):

        goal = self.predict_goal()

        if goal is None:

            # Sécurité supplémentaire si le ballon
            # se trouve déjà derrière la ligne.
            if (
                self.ball_x > self.field.right
                and self.is_ball_in_goal_mouth()
            ):

                goal = "home"

            elif (
                self.ball_x < self.field.left
                and self.is_ball_in_goal_mouth()
            ):

                goal = "away"

        if goal is None:
            return False

        return self.register_goal(
            goal
        )

    # ==========================================================
    # BALLON
    # ==========================================================

    def update_ball(self):

        if self.ball_owner is not None:

            # Le contrôle de base reste disponible
            # pour maintenir le ballon attaché au joueur.

            self.control_system.update()

            return

        self.ball_x = max(
            self.field.left - 40,
            min(
                self.field.right + 40,
                self.ball_x
            )
        )

        self.ball_y = max(
            self.field.top,
            min(
                self.field.bottom,
                self.ball_y
            )
        )

    # ==========================================================
    # POSSESSION
    # ==========================================================

    def update_possession(self):

        if self.ball_owner is not None:
            return

        self.control_system.check_recovery()

    # ==========================================================
    # ÉVÉNEMENTS
    # ==========================================================

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                self.paused = not self.paused

                return True

        return self.match_controller.handle_event(
            event
        )

    # ==========================================================
    # MISE À JOUR PRINCIPALE
    # ==========================================================

    def update(self):

        if self.finished:
            return

        if self.paused:
            return

        delta_time = (
            self.game.clock.get_time()
            / 1000.0
        )

        if delta_time <= 0:

            delta_time = 0.016

        delta_time = min(
            delta_time,
            0.1
        )

        # ------------------------------------------------------
        # HORLOGE DU MATCH
        # ------------------------------------------------------

        self.match_time += delta_time

        if self.match_time >= 45.0:

            self.match_phase = (
                "second_half"
            )

        # ------------------------------------------------------
        # VÉRIFICATION BUT AVANT PHYSIQUE
        #
        # Permet de contourner l'ancien comportement de
        # BallPhysics qui peut rebondir sur la ligne.
        # ------------------------------------------------------

        if self.predict_goal() is not None:

            self.check_goals()

            return

        # ------------------------------------------------------
        # PUISSANCE
        # ------------------------------------------------------

        self.handle_power_input()

        if self.charging_action is not None:

            self.power_system.update()

        # ------------------------------------------------------
        # ARCHITECTURE CENTRALE
        #
        # Le MatchController coordonne :
        # input
        # rôles
        # espace
        # IA
        # tactiques
        # pressing
        # marquage
        # gameplay
        # dribble
        # protection
        # physique
        # endurance
        # fatigue
        # ------------------------------------------------------

        self.match_controller.update(
            delta_time
        )

        # ------------------------------------------------------
        # GARDIENS
        # ------------------------------------------------------

        self.update_goalkeepers(
            delta_time
        )

        # ------------------------------------------------------
        # BUTS
        # ------------------------------------------------------

        if self.check_goals():

            return

        # ------------------------------------------------------
        # BALLON / POSSESSION
        # ------------------------------------------------------

        self.update_ball()

        self.update_possession()

        # ------------------------------------------------------
        # FIN DU MATCH
        # ------------------------------------------------------

        if self.match_time >= self.match_duration:

            self.match_time = (
                self.match_duration
            )

            self.finished = True

            if (
                self.home_score
                >
                self.away_score
            ):

                self.match_result = "win"

            elif (
                self.home_score
                <
                self.away_score
            ):

                self.match_result = "loss"

            else:

                self.match_result = "draw"

    # ==========================================================
    # PAUSE / REPRISE
    # ==========================================================

    def pause(self):

        self.paused = True

    def resume(self):

        self.paused = False

    def restart(self):

        self.finished = False
        self.paused = False

        self.match_time = 0.0

        self.match_phase = (
            "first_half"
        )

        self.match_result = None

        self.home_score = 0
        self.away_score = 0

        self.reset_positions()

        if hasattr(
            self,
            "match_controller"
        ):

            self.match_controller.reset()

        self.select_nearest_player()

    # ==========================================================
    # DIFFICULTÉ
    # ==========================================================

    def set_difficulty(
        self,
        difficulty
    ):

        self.difficulty = difficulty

        self.ai.set_difficulty(
            difficulty
        )

        self.game.save[
            "difficulty"
        ] = difficulty

    def get_difficulty(self):

        return self.difficulty

    # ==========================================================
    # INFORMATIONS DU MATCH
    # ==========================================================

    def get_score(self):

        return (
            self.home_score,
            self.away_score
        )

    def get_match_time(self):

        return self.match_time

    def get_exact_minute(self):

        return min(
            int(self.match_time),
            int(self.match_duration)
        )

    def is_finished(self):

        return self.finished

    def get_result(self):

        return self.match_result

    # ==========================================================
    # GARDIEN : AFFICHAGE
    # ==========================================================

    def draw_goalkeeper(
        self,
        screen,
        player
    ):

        if player.team == "blue":

            color = (
                20,
                220,
                220
            )

        else:

            color = (
                255,
                170,
                40
            )

        pygame.draw.circle(
            screen,
            color,
            (
                int(player.x),
                int(player.y)
            ),
            player.radius + 2
        )

        pygame.draw.circle(
            screen,
            (
                245,
                245,
                245
            ),
            (
                int(player.x),
                int(player.y)
            ),
            5
        )

        pygame.draw.circle(
            screen,
            (
                20,
                20,
                20
            ),
            (
                int(player.x),
                int(player.y)
            ),
            player.radius + 2,
            2
        )

        end_x = (
            player.x
            +
            player.direction_x
            * 12
        )

        end_y = (
            player.y
            +
            player.direction_y
            * 12
        )

        pygame.draw.line(
            screen,
            (
                255,
                255,
                255
            ),
            (
                int(player.x),
                int(player.y)
            ),
            (
                int(end_x),
                int(end_y)
            ),
            2
        )

    # ==========================================================
    # BARRE DE PUISSANCE
    # ==========================================================

    def draw_power_bar(
        self,
        screen
    ):

        if self.charging_action is None:
            return

        power = (
            self.power_system.get_power()
        )

        bar_x = 270
        bar_y = 555

        bar_width = 360
        bar_height = 24

        pygame.draw.rect(
            screen,
            (
                10,
                15,
                25
            ),
            (
                bar_x,
                bar_y,
                bar_width,
                bar_height
            ),
            border_radius=8
        )

        fill_width = int(
            bar_width * power
        )

        if self.charging_action == "pass":

            fill_color = (
                30,
                190,
                255
            )

        else:

            fill_color = (
                255,
                170,
                40
            )

        if fill_width > 0:

            pygame.draw.rect(
                screen,
                fill_color,
                (
                    bar_x,
                    bar_y,
                    fill_width,
                    bar_height
                ),
                border_radius=8
            )

        pygame.draw.rect(
            screen,
            (
                235,
                235,
                235
            ),
            (
                bar_x,
                bar_y,
                bar_width,
                bar_height
            ),
            2,
            border_radius=8
        )

    # ==========================================================
    # AFFICHAGE
    # ==========================================================

    def draw(self, screen):

        # ------------------------------------------------------
        # TERRAIN
        # ------------------------------------------------------

        screen.fill(
            (
                8,
                100,
                45
            )
        )

        pygame.draw.rect(
            screen,
            (
                235,
                235,
                235
            ),
            self.field,
            4
        )

        pygame.draw.line(
            screen,
            (
                235,
                235,
                235
            ),
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

        pygame.draw.circle(
            screen,
            (
                235,
                235,
                235
            ),
            self.field.center,
            70,
            3
        )

        # ------------------------------------------------------
        # SURFACES
        # ------------------------------------------------------

        pygame.draw.rect(
            screen,
            (
                235,
                235,
                235
            ),
            (
                self.field.left,
                self.field.centery - 100,
                120,
                200
            ),
            3
        )

        pygame.draw.rect(
            screen,
            (
                235,
                235,
                235
            ),
            (
                self.field.right - 120,
                self.field.centery - 100,
                120,
                200
            ),
            3
        )

        pygame.draw.rect(
            screen,
            (
                235,
                235,
                235
            ),
            (
                self.field.left,
                self.field.centery - 55,
                55,
                110
            ),
            3
        )

        pygame.draw.rect(
            screen,
            (
                235,
                235,
                235
            ),
            (
                self.field.right - 55,
                self.field.centery - 55,
                55,
                110
            ),
            3
        )

        # ------------------------------------------------------
        # JOUEURS DOMICILE
        # ------------------------------------------------------

        for player in self.home_players:

            if not getattr(
                player,
                "on_pitch",
                True
            ):
                continue

            if player.number == 1:

                self.draw_goalkeeper(
                    screen,
                    player
                )

            else:

                player.draw(
                    screen
                )

        # ------------------------------------------------------
        # JOUEURS EXTÉRIEURS
        # ------------------------------------------------------

        for player in self.away_players:

            if not getattr(
                player,
                "on_pitch",
                True
            ):
                continue

            if player.number == 1:

                self.draw_goalkeeper(
                    screen,
                    player
                )

            else:

                player.draw(
                    screen
                )

        # ------------------------------------------------------
        # JOUEUR SÉLECTIONNÉ
        # ------------------------------------------------------

        selected = (
            self.get_selected_player()
        )

        if selected is not None:

            pygame.draw.circle(
                screen,
                (
                    255,
                    230,
                    60
                ),
                (
                    int(selected.x),
                    int(selected.y)
                ),
                selected.radius + 6,
                3
            )

        # ------------------------------------------------------
        # BALLON
        # ------------------------------------------------------

        pygame.draw.circle(
            screen,
            (
                250,
                250,
                250
            ),
            (
                int(self.ball_x),
                int(self.ball_y)
            ),
            7
        )

        pygame.draw.circle(
            screen,
            (
                20,
                20,
                20
            ),
            (
                int(self.ball_x),
                int(self.ball_y)
            ),
            7,
            2
        )

        # ------------------------------------------------------
        # SCORE
        # ------------------------------------------------------

        pygame.draw.rect(
            screen,
            (
                5,
                15,
                25
            ),
            (
                340,
                10,
                220,
                45
            ),
            border_radius=10
        )

        # Points domicile

        for i in range(
            min(
                self.home_score,
                5
            )
        ):

            pygame.draw.circle(
                screen,
                (
                    30,
                    130,
                    240
                ),
                (
                    365 + i * 25,
                    32
                ),
                6
            )

        # Points extérieur

        for i in range(
            min(
                self.away_score,
                5
            )
        ):

            pygame.draw.circle(
                screen,
                (
                    220,
                    60,
                    70
                ),
                (
                    455 + i * 25,
                    32
                ),
                6
            )

        # ------------------------------------------------------
        # CONTRÔLES MOBILES
        # ------------------------------------------------------

        if hasattr(
            self,
            "mobile_controls"
        ):

            self.mobile_controls.draw(
                screen
            )

        # ------------------------------------------------------
        # BARRE DE PUISSANCE
        # ------------------------------------------------------

        self.draw_power_bar(
            screen
        )