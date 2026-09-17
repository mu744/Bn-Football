TEAMS = [
    {
        "id": "bnu",
        "name": "BN United",
        "short": "BNU",
        "color": (0, 210, 255),
        "strength": 82,
        "formation": "4-3-3"
    },
    {
        "id": "ouaga",
        "name": "Ouaga Stars",
        "short": "OUA",
        "color": (240, 200, 40),
        "strength": 78,
        "formation": "4-4-2"
    },
    {
        "id": "sahel",
        "name": "Sahel FC",
        "short": "SAH",
        "color": (60, 180, 90),
        "strength": 75,
        "formation": "4-2-3-1"
    },
    {
        "id": "falcons",
        "name": "Falcons FC",
        "short": "FAL",
        "color": (220, 70, 70),
        "strength": 73,
        "formation": "4-3-3"
    },
    {
        "id": "lions",
        "name": "Golden Lions",
        "short": "GLI",
        "color": (255, 150, 30),
        "strength": 76,
        "formation": "3-5-2"
    },
    {
        "id": "eagles",
        "name": "Blue Eagles",
        "short": "BEA",
        "color": (50, 100, 230),
        "strength": 80,
        "formation": "4-3-3"
    },
    {
        "id": "titans",
        "name": "Black Titans",
        "short": "BLA",
        "color": (120, 120, 140),
        "strength": 77,
        "formation": "4-2-3-1"
    },
    {
        "id": "phoenix",
        "name": "Phoenix FC",
        "short": "PHX",
        "color": (230, 70, 150),
        "strength": 74,
        "formation": "4-4-2"
    }
]


def get_team(team_id):
    for team in TEAMS:
        if team["id"] == team_id:
            return team

    return TEAMS[0]
