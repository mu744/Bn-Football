class PhysicsManager:
    """
    Gestionnaire central de la physique du match.

    Il coordonne :
    - physique de la balle
    - collisions entre joueurs

    Le gestionnaire possède une seule responsabilité :
    appeler chaque système physique une seule fois par frame.
    """

    def __init__(self, match):
        self.match = match

        self.enabled = True

        self.ball = None
        self.player_collision = None

        self.initialized = False

        self.attach()

    # ---------------------------------------------------------
    # INITIALISATION
    # ---------------------------------------------------------

    def attach(self):
        self.attach_ball()

        collision = getattr(
            self.match,
            "player_collision",
            None
        )

        if collision is not None:
            self.attach_player_collision(collision)

        self.initialized = True

    # ---------------------------------------------------------
    # BALLE
    # ---------------------------------------------------------

    def attach_ball(self):
        self.ball = getattr(
            self.match,
            "ball_physics",
            None
        )

    # ---------------------------------------------------------
    # JOUEURS
    # ---------------------------------------------------------

    def attach_player_collision(self, collision_system):
        self.player_collision = collision_system

    # ---------------------------------------------------------
    # UPDATE
    # ---------------------------------------------------------

    def update(self):
        if not self.enabled:
            return

        # Une seule mise à jour de la physique de la balle.
        if self.ball is not None:
            self.ball.update()

        # Puis résolution des collisions joueurs.
        if self.player_collision is not None:
            self.player_collision.update()

    # ---------------------------------------------------------
    # CONTROLE
    # ---------------------------------------------------------

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    # ---------------------------------------------------------
    # RESET
    # ---------------------------------------------------------

    def reset(self):
        if self.ball is not None:
            self.ball.reset()

        if self.player_collision is not None:
            self.player_collision.reset()

        self.enabled = True

    # ---------------------------------------------------------
    # ETAT
    # ---------------------------------------------------------

    def is_initialized(self):
        return self.initialized

    def get_ball_physics(self):
        return self.ball

    def get_player_collision(self):
        return self.player_collision
