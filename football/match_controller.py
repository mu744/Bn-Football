class MatchController:
    """
    Contrôleur central du match.

    Coordonne les systèmes de gameplay, IA, tactiques,
    physique, contrôles et gestion des joueurs.

    Architecture prévue pour évoluer vers une version
    complète 11v11 et Android.
    """

    def __init__(self, match):
        self.match = match
        self.enabled = True

        self.registry = getattr(match, "system_registry", None)

        self.mobile_controls = None
        self.player_controller = None
        self.input_manager = None
        self.action_controller = None

    # ---------------------------------------------------------
    # ATTACHEMENT DES CONTRÔLES
    # ---------------------------------------------------------

    def attach_controls(self, mobile_controls=None, player_controller=None):
        self.mobile_controls = mobile_controls
        self.player_controller = player_controller

        if self.input_manager is None:
            self.input_manager = getattr(self.match, "input_manager", None)

        if self.input_manager is not None:
            self.input_manager.set_mobile_controls(mobile_controls)

    def attach_action_controller(self, action_controller):
        self.action_controller = action_controller

    def attach_input_manager(self, input_manager):
        self.input_manager = input_manager

        if self.mobile_controls is not None:
            self.input_manager.set_mobile_controls(
                self.mobile_controls
            )

    # ---------------------------------------------------------
    # REGISTRE
    # ---------------------------------------------------------

    def set_registry(self, registry):
        self.registry = registry

    def get_system(self, name):
        if self.registry is None:
            return None

        return self.registry.get(name)

    # ---------------------------------------------------------
    # INPUT
    # ---------------------------------------------------------

    def update_input(self, delta_time=0.016):
        if self.input_manager is None:
            return

        self.input_manager.update()

        if self.player_controller is not None:
            dx, dy = self.input_manager.get_movement()
            sprint = self.input_manager.is_sprinting()

            self.player_controller.set_direction(dx, dy)
            self.player_controller.set_sprint(sprint)

            self.player_controller.update()

            player = self.player_controller.get_player()

            if player is not None:
                player.is_sprinting = sprint

        if self.action_controller is None:
            return

        if self.input_manager.action_pressed("pass"):
            self.action_controller.pass_ball()

        if self.input_manager.action_pressed("shoot"):
            self.action_controller.shoot()

        if self.input_manager.action_pressed("tackle"):
            self.action_controller.tackle()

        if self.input_manager.action_pressed("switch"):
            self.action_controller.switch_player()

    # ---------------------------------------------------------
    # SYSTEMES DE JEU
    # ---------------------------------------------------------

    def update_roles(self):
        roles = self.get_system("roles")

        if roles is not None and hasattr(roles, "update"):
            roles.update()

    def update_space(self):
        space = self.get_system("space")

        if space is not None and hasattr(space, "update"):
            space.update()

    def update_ai(self, delta_time):
        ai = self.get_system("ai_manager")

        if ai is not None and hasattr(ai, "update"):
            ai.update(delta_time)

    def update_team_ai(self):
        team_ai = self.get_system("team_ai")

        if team_ai is not None and hasattr(team_ai, "update"):
            team_ai.update()

    def update_tactics(self):
        strategy = self.get_system("dynamic_strategy")

        if strategy is not None and hasattr(strategy, "update"):
            strategy.update()

    def update_pressing(self):
        pressing = self.get_system("pressing")

        if pressing is not None and hasattr(pressing, "update"):
            pressing.update()

    def update_marking(self):
        marking = self.get_system("marking")

        if marking is not None and hasattr(marking, "update"):
            marking.update()

    def update_gameplay(self, delta_time):
        gameplay = self.get_system("gameplay")

        if gameplay is not None and hasattr(gameplay, "update"):
            gameplay.update(delta_time)

    def update_physics(self):
        physics = self.get_system("physics")

        if physics is not None and hasattr(physics, "update"):
            physics.update()

    # ---------------------------------------------------------
    # SYSTEMES SUPPLEMENTAIRES
    # ---------------------------------------------------------

    def update_stamina(self, delta_time):
        stamina = self.get_system("stamina")

        if stamina is not None and hasattr(stamina, "update"):
            stamina.update(delta_time)

    def update_fatigue(self, delta_time):
        fatigue = self.get_system("fatigue")

        if fatigue is not None and hasattr(fatigue, "update"):
            fatigue.update(delta_time)

    def update_dribble(self, delta_time):
        dribble = self.get_system("dribble")

        if dribble is not None and hasattr(dribble, "update"):
            sprint = False

            if self.input_manager is not None:
                sprint = self.input_manager.is_sprinting()

            dribble.update(delta_time, sprint)

    def update_ball_protection(self):
        protection = self.get_system("ball_protection")

        if protection is not None and hasattr(protection, "update"):
            protection.update()

    # ---------------------------------------------------------
    # CONTROLE GENERAL
    # ---------------------------------------------------------

    def update(self, delta_time=0.016):
        if not self.enabled:
            return

        # 1. Commandes joueur
        self.update_input(delta_time)

        # 2. Organisation collective
        self.update_roles()
        self.update_space()

        # 3. IA
        self.update_ai(delta_time)
        self.update_team_ai()

        # 4. Tactiques
        self.update_tactics()
        self.update_pressing()
        self.update_marking()

        # 5. Gameplay
        self.update_gameplay(delta_time)

        # 6. Dribble / protection
        self.update_dribble(delta_time)
        self.update_ball_protection()

        # 7. Physique
        self.update_physics()

        # 8. Condition physique
        self.update_stamina(delta_time)
        self.update_fatigue(delta_time)

    # ---------------------------------------------------------
    # EVENEMENTS
    # ---------------------------------------------------------

    def handle_event(self, event):
        if not self.enabled:
            return False

        if self.input_manager is not None:
            return self.input_manager.handle_event(event)

        if self.mobile_controls is not None:
            return self.mobile_controls.handle_event(event)

        return False

    # ---------------------------------------------------------
    # CONTROLE
    # ---------------------------------------------------------

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

        if self.player_controller is not None:
            self.player_controller.stop()

    def reset(self):
        self.enabled = True

        if self.input_manager is not None:
            self.input_manager.reset()

        if self.player_controller is not None:
            self.player_controller.reset()

        if self.action_controller is not None:
            self.action_controller.reset()

    def is_enabled(self):
        return self.enabled
