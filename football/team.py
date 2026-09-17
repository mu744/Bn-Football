from data.teams import get_team
from data.players import get_players


class Team:

    def __init__(self, team_id):

        data = get_team(team_id)

        self.id = data["id"]
        self.name = data["name"]
        self.short = data["short"]
        self.color = data["color"]
        self.strength = data["strength"]
        self.formation = data["formation"]

        self.players = get_players(team_id)

    def get_starting_eleven(self):

        return self.players[:11]

    def get_bench(self):

        return self.players[11:]

    def get_average_rating(self):

        if not self.players:
            return 0

        total = sum(
            player["rating"]
            for player in self.players
        )

        return round(
            total / len(self.players)
        )
