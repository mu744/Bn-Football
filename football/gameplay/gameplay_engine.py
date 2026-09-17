import math

from football.gameplay.first_touch_system import FirstTouchSystem
from football.gameplay.ball_receiving import BallReceiving
from football.gameplay.through_ball_system import ThroughBallSystem
from football.gameplay.cross_system import CrossSystem
from football.gameplay.one_two_system import OneTwoSystem
from football.gameplay.heading_system import HeadingSystem
from football.gameplay.volley_system import VolleySystem
from football.gameplay.clearance_system import ClearanceSystem
from football.gameplay.interception_system import InterceptionSystem
from football.gameplay.ball_recovery import BallRecovery


class GameplayEngine:
    """
    Centre de coordination du gameplay.

    Toutes les mécaniques techniques passent par ce moteur.
    Le moteur graphique 2D/3D pourra utiliser ce système
    sans modifier la logique football.
    """

    def __init__(self, match):
        self.match = match
        self.enabled = True

        self.first_touch = FirstTouchSystem(match)
        self.receiving = BallReceiving(match)
        self.through_ball = ThroughBallSystem(match)
        self.cross = CrossSystem(match)
        self.one_two = OneTwoSystem(match)
        self.heading = HeadingSystem(match)
        self.volley = VolleySystem(match)
        self.clearance = ClearanceSystem(match)
        self.interception = InterceptionSystem(match)
        self.recovery = BallRecovery(match)

        self.systems = [
            self.first_touch,
            self.receiving,
            self.through_ball,
            self.cross,
            self.one_two,
            self.heading,
            self.volley,
            self.clearance,
            self.interception,
            self.recovery,
        ]

    def update(self, delta_time=0.016):
        if not self.enabled:
            return

        self._update_systems(delta_time)

    def _update_systems(self, delta_time):
        """
        Ordre contrôlé d'exécution.

        Important :
        la physique du ballon doit être traitée avant
        les décisions de récupération lorsque nécessaire.
        """

        self.receiving.update()
        self.first_touch.update()

        self.interception.update()
        self.recovery.update()

        self.through_ball.update()
        self.cross.update()
        self.one_two.update()
        self.heading.update()
        self.volley.update()
        self.clearance.update()

    def pass_through(self, player, target):
        return self.through_ball.pass_ball(player, target)

    def make_cross(self, player, target_x, target_y):
        return self.cross.cross(player, target_x, target_y)

    def start_one_two(self, player, teammate):
        return self.one_two.start(player, teammate)

    def return_one_two(self):
        return self.one_two.return_pass()

    def make_header(self, player, target_x, target_y):
        return self.heading.header(player, target_x, target_y)

    def make_volley(self, player, target_x, target_y):
        return self.volley.volley(player, target_x, target_y)

    def clear_ball(self, player):
        return self.clearance.clearance(player)

    def receive_ball(self, player):
        return self.receiving.receive(player)

    def intercept_ball(self, player):
        return self.interception.intercept(player)

    def recover_ball(self, player):
        return self.recovery.recover(player)

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def reset(self):
        for system in self.systems:
            if hasattr(system, "reset"):
                system.reset()
