import pygame

from core.settings import FPS, TITLE

from core.states import (
    MENU,
    MATCH,
    CHAMPIONSHIP,
    CALENDAR,
    STANDINGS,
    SQUAD,
    SETTINGS,
    TEAM_SELECTION
)

from core.save_manager import load_game, save_game

from core.display import (
    LOGICAL_WIDTH,
    LOGICAL_HEIGHT,
    create_window,
    scale_surface,
    to_logical_pos
)

from screens.main_menu import MainMenu, PlaceholderScreen
from screens.match_screen import MatchScreen
from screens.team_selection import TeamSelection
from screens.squad import SquadScreen


class Game:

    def __init__(self):

        pygame.init()

        self.screen = create_window()

        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()

        self.running = True

        self.state = MENU

        self.save = load_game()

        self.main_menu = MainMenu(self)

        self.match_screen = MatchScreen(self)

        self.team_selection = TeamSelection(self)

        self.squad_screen = SquadScreen(self)

        self.screens = {

            CHAMPIONSHIP:
                PlaceholderScreen(
                    self,
                    CHAMPIONSHIP
                ),

            CALENDAR:
                PlaceholderScreen(
                    self,
                    CALENDAR
                ),

            STANDINGS:
                PlaceholderScreen(
                    self,
                    STANDINGS
                ),

            SQUAD:
                self.squad_screen,

            SETTINGS:
                PlaceholderScreen(
                    self,
                    SETTINGS
                )
        }

    def save_game(self):

        save_game(self.save)

    def toggle_fullscreen(self):

        current_flags = pygame.display.get_surface().get_flags()

        if current_flags & pygame.FULLSCREEN:

            self.screen = create_window()

        else:

            self.screen = pygame.display.set_mode(
                (0, 0),
                pygame.FULLSCREEN
            )

    def run(self):

        while self.running:

            self.handle_events()

            self.update()

            self.draw()

            self.clock.tick(FPS)

        self.save_game()

        pygame.quit()

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                self.running = False
                continue

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_F11:

                    self.toggle_fullscreen()
                    continue

                if event.key == pygame.K_f:

                    self.toggle_fullscreen()
                    continue

            # Conversion des coordonnées physiques
            # vers notre résolution interne 900x600
            if event.type in (
                pygame.MOUSEBUTTONDOWN,
                pygame.MOUSEBUTTONUP,
                pygame.MOUSEMOTION
            ):

                if hasattr(event, "pos"):

                    logical_pos = to_logical_pos(
                        event.pos,
                        self.screen
                    )

                    event = pygame.event.Event(
                        event.type,
                        {
                            **event.__dict__,
                            "pos": logical_pos
                        }
                    )

            if self.state == MENU:

                self.main_menu.handle_event(event)

            elif self.state == TEAM_SELECTION:

                self.team_selection.handle_event(event)

            elif self.state == SQUAD:

                self.squad_screen.handle_event(event)

            elif self.state == MATCH:

                self.match_screen.handle_event(event)

            elif self.state in self.screens:

                self.screens[
                    self.state
                ].handle_event(event)

    def update(self):

        if self.state == MATCH:

            self.match_screen.update()

    def draw(self):

        # Surface interne 900x600
        logical_surface = pygame.Surface(
            (LOGICAL_WIDTH, LOGICAL_HEIGHT)
        )

        if self.state == MENU:

            self.main_menu.draw(
                logical_surface
            )

        elif self.state == TEAM_SELECTION:

            self.team_selection.draw(
                logical_surface
            )

        elif self.state == SQUAD:

            self.squad_screen.draw(
                logical_surface
            )

        elif self.state == MATCH:

            self.match_screen.draw(
                logical_surface
            )

        elif self.state in self.screens:

            self.screens[
                self.state
            ].draw(
                logical_surface
            )

        # Adaptation automatique à X11
        scale_surface(
            logical_surface,
            self.screen
        )

        pygame.display.flip()
