class MatchContext:

    def __init__(self, match):

        self.match = match

        self.registry = getattr(
            match,
            "system_registry",
            None
        )

    def get(self, system_name):

        if self.registry is None:
            return None

        return self.registry.get(system_name)

    def gameplay(self):
        return self.get("gameplay")

    def ai(self):
        return self.get("ai_manager")

    def roles(self):
        return self.get("roles")

    def pressing(self):
        return self.get("pressing")

    def marking(self):
        return self.get("marking")

    def space(self):
        return self.get("space")

    def statistics(self):
        return self.get("statistics")

    def referee(self):
        return self.get("referee")

    def substitutions(self):
        return self.get("substitutions")
