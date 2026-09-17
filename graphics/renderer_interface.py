class RendererInterface:

    def __init__(self):
        self.initialized = False

    def initialize(self, screen):
        self.initialized = True

    def begin_frame(self):
        pass

    def render_match(self, match):
        pass

    def render_player(self, player):
        pass

    def render_ball(self, ball):
        pass

    def render_ui(self, game):
        pass

    def end_frame(self):
        pass

    def shutdown(self):
        self.initialized = False
