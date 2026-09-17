from football.gameplay.gameplay_engine import GameplayEngine

from football.team_ai import TeamAI
from football.ai_manager import AIManager
from football.dynamic_strategy import DynamicStrategy

from football.substitution_system import SubstitutionSystem
from football.referee_system import RefereeSystem
from football.set_piece_system import SetPieceSystem
from football.match_statistics import MatchStatistics
from football.extra_time_system import ExtraTimeSystem

from football.roles.role_manager import RoleManager
from football.pressing_system import PressingSystem
from football.marking_system import MarkingSystem
from football.space_system import SpaceSystem

from football.gameplay.player_collision import PlayerCollision
from football.gameplay.dribble_system import DribbleSystem
from football.gameplay.ball_protection import BallProtection
from football.gameplay.stamina_system import StaminaSystem
from football.gameplay.fatigue_effects import FatigueEffects

from football.physics_manager import PhysicsManager


class SystemRegistry:
    """
    Registre central de BN-Football.

    Tous les systèmes du moteur sont créés ici et exposés
    au reste du jeu.

    Principe :
        Match
          ↓
        SystemRegistry
          ↓
        Gameplay / IA / Physique / Tactique / Contrôles

    Cette architecture permet d'ajouter de nouveaux systèmes
    sans reconstruire toute l'application.
    """

    def __init__(self, match):
        self.match = match

        # --------------------------------------------------
        # SYSTEMES PRINCIPAUX
        # --------------------------------------------------

        self.gameplay = None
        self.team_ai = None
        self.ai_manager = None
        self.dynamic_strategy = None

        # --------------------------------------------------
        # ORGANISATION TACTIQUE
        # --------------------------------------------------

        self.roles = None
        self.pressing = None
        self.marking = None
        self.space = None

        # --------------------------------------------------
        # PHYSIQUE
        # --------------------------------------------------

        self.player_collision = None
        self.physics = None

        # --------------------------------------------------
        # GAMEPLAY AVANCE
        # --------------------------------------------------

        self.dribble = None
        self.ball_protection = None
        self.stamina = None
        self.fatigue = None

        # --------------------------------------------------
        # GESTION DU MATCH
        # --------------------------------------------------

        self.substitutions = None
        self.referee = None
        self.set_pieces = None
        self.statistics = None
        self.extra_time = None

        self.initialized = False

    # ======================================================
    # INITIALISATION
    # ======================================================

    def initialize(self):
        if self.initialized:
            return

        self.create_roles()

        self.create_gameplay()

        self.create_team_ai()
        self.create_ai_manager()
        self.create_dynamic_strategy()

        self.create_pressing()
        self.create_marking()
        self.create_space()

        self.create_player_collision()
        self.create_physics()

        self.create_dribble()
        self.create_ball_protection()
        self.create_stamina()
        self.create_fatigue()

        self.create_substitution_system()
        self.create_referee_system()
        self.create_set_piece_system()
        self.create_statistics()
        self.create_extra_time()

        self.attach_to_match()

        self.initialized = True

    # ======================================================
    # CREATION DES SYSTEMES
    # ======================================================

    def create_roles(self):
        self.roles = RoleManager(self.match)

    def create_gameplay(self):
        self.gameplay = GameplayEngine(self.match)

    def create_team_ai(self):
        self.team_ai = TeamAI(self.match)

    def create_ai_manager(self):
        self.ai_manager = AIManager(self.match)

    def create_dynamic_strategy(self):
        tactics = getattr(
            self.match,
            "tactics_system",
            None
        )

        if tactics is not None:
            self.dynamic_strategy = DynamicStrategy(tactics)
        else:
            self.dynamic_strategy = None

    def create_pressing(self):
        self.pressing = PressingSystem(self.match)

    def create_marking(self):
        self.marking = MarkingSystem(self.match)

    def create_space(self):
        self.space = SpaceSystem(self.match)

    def create_player_collision(self):
        self.player_collision = PlayerCollision(self.match)

    def create_physics(self):
        self.physics = PhysicsManager(self.match)

        if self.player_collision is not None:
            self.physics.attach_player_collision(
                self.player_collision
            )

        self.physics.attach_ball()

    # ======================================================
    # GAMEPLAY AVANCE
    # ======================================================

    def create_dribble(self):
        self.dribble = DribbleSystem(self.match)

    def create_ball_protection(self):
        self.ball_protection = BallProtection(self.match)

    def create_stamina(self):
        self.stamina = StaminaSystem(self.match)

    def create_fatigue(self):
        self.fatigue = FatigueEffects(self.match)

    # ======================================================
    # GESTION DU MATCH
    # ======================================================

    def create_substitution_system(self):
        self.substitutions = SubstitutionSystem(self.match)

    def create_referee_system(self):
        self.referee = RefereeSystem(self.match)

    def create_set_piece_system(self):
        self.set_pieces = SetPieceSystem(self.match)

    def create_statistics(self):
        self.statistics = MatchStatistics(self.match)

    def create_extra_time(self):
        self.extra_time = ExtraTimeSystem(self.match)

    # ======================================================
    # CONNEXION AU MATCH
    # ======================================================

    def attach_to_match(self):
        """
        Rend les systèmes accessibles directement depuis Match.
        """

        self.match.system_registry = self

        self.match.gameplay_engine = self.gameplay

        self.match.team_ai = self.team_ai
        self.match.ai_manager = self.ai_manager
        self.match.dynamic_strategy = self.dynamic_strategy

        self.match.role_manager = self.roles

        self.match.pressing_system = self.pressing
        self.match.marking_system = self.marking
        self.match.space_system = self.space

        self.match.player_collision = self.player_collision
        self.match.physics_manager = self.physics

        self.match.dribble_system = self.dribble
        self.match.ball_protection = self.ball_protection
        self.match.stamina_system = self.stamina
        self.match.fatigue_effects = self.fatigue

        self.match.substitution_system = self.substitutions
        self.match.referee_system = self.referee
        self.match.set_piece_system = self.set_pieces
        self.match.statistics = self.statistics
        self.match.extra_time_system = self.extra_time

    # ======================================================
    # ACCES A UN SYSTEME
    # ======================================================

    def get(self, name):
        systems = {
            "gameplay": self.gameplay,

            "team_ai": self.team_ai,
            "ai_manager": self.ai_manager,
            "dynamic_strategy": self.dynamic_strategy,

            "roles": self.roles,
            "pressing": self.pressing,
            "marking": self.marking,
            "space": self.space,

            "player_collision": self.player_collision,
            "physics": self.physics,

            "dribble": self.dribble,
            "ball_protection": self.ball_protection,
            "stamina": self.stamina,
            "fatigue": self.fatigue,

            "substitutions": self.substitutions,
            "referee": self.referee,
            "set_pieces": self.set_pieces,
            "statistics": self.statistics,
            "extra_time": self.extra_time,
        }

        return systems.get(name)

    # ======================================================
    # TOUS LES SYSTEMES
    # ======================================================

    def get_all(self):
        return {
            "gameplay": self.gameplay,

            "team_ai": self.team_ai,
            "ai_manager": self.ai_manager,
            "dynamic_strategy": self.dynamic_strategy,

            "roles": self.roles,
            "pressing": self.pressing,
            "marking": self.marking,
            "space": self.space,

            "player_collision": self.player_collision,
            "physics": self.physics,

            "dribble": self.dribble,
            "ball_protection": self.ball_protection,
            "stamina": self.stamina,
            "fatigue": self.fatigue,

            "substitutions": self.substitutions,
            "referee": self.referee,
            "set_pieces": self.set_pieces,
            "statistics": self.statistics,
            "extra_time": self.extra_time,
        }

    # ======================================================
    # RESET
    # ======================================================

    def reset(self):
        for system in self.get_all().values():

            if system is None:
                continue

            if hasattr(system, "reset"):
                system.reset()

    # ======================================================
    # ETAT
    # ======================================================

    def is_initialized(self):
        return self.initialized
