PLAYER_NAMES = [
    "Kader", "Moussa", "Ibrahim", "Adama",
    "Saidou", "Yacouba", "Oumar", "Issa",
    "Salif", "Amadou", "Karim",

    "Nabi", "Mika", "Souleymane", "Bakary", "Yoro",

    "Fadil", "Boubacar", "Nassir", "Rachid",
    "Madi", "Hamza", "Daouda", "Ali",
    "Sory", "Abdou", "Zakaria", "Hamidou",
    "Issouf", "Mahamadou"
]

POSITIONS = [
    "GK",
    "DF", "DF", "DF", "DF",
    "MC", "MC", "MC",
    "AT", "AT", "AT",

    "GK",
    "DF", "MC", "AT", "AT"
]


TEAM_RATINGS = {
    "bnu": [
        84, 81, 83, 80, 79,
        84, 82, 80,
        86, 83, 85,
        78, 76, 79, 80, 77
    ],

    "ouaga": [
        80, 78, 81, 77, 76,
        82, 79, 80,
        82, 80, 81,
        75, 74, 77, 79, 76
    ],

    "sahel": [
        78, 76, 78, 75, 74,
        79, 77, 76,
        81, 78, 80,
        73, 72, 75, 77, 74
    ],

    "falcons": [
        77, 75, 79, 74, 76,
        80, 78, 77,
        82, 79, 81,
        72, 73, 76, 78, 74
    ],

    "lions": [
        81, 79, 80, 78, 77,
        83, 81, 79,
        84, 82, 83,
        76, 75, 78, 80, 77
    ],

    "eagles": [
        83, 80, 82, 79, 78,
        84, 82, 81,
        85, 84, 84,
        77, 76, 79, 81, 78
    ],

    "titans": [
        81, 78, 80, 77, 76,
        82, 80, 79,
        83, 81, 82,
        76, 74, 78, 79, 76
    ],

    "phoenix": [
        79, 77, 78, 75, 74,
        81, 79, 78,
        83, 80, 82,
        74, 73, 76, 78, 75
    ]
}


def make_stats(rating, position):

    if position == "GK":
        return {
            "pace": max(45, rating - 20),
            "shooting": max(30, rating - 30),
            "passing": rating - 5,
            "defense": rating + 2,
            "physical": rating,
            "goalkeeping": rating + 4
        }

    if position == "DF":
        return {
            "pace": rating - 2,
            "shooting": rating - 15,
            "passing": rating - 3,
            "defense": rating + 5,
            "physical": rating + 3,
            "goalkeeping": 10
        }

    if position == "MC":
        return {
            "pace": rating + 1,
            "shooting": rating - 3,
            "passing": rating + 5,
            "defense": rating - 5,
            "physical": rating,
            "goalkeeping": 10
        }

    return {
        "pace": rating + 5,
        "shooting": rating + 6,
        "passing": rating,
        "defense": rating - 12,
        "physical": rating - 1,
        "goalkeeping": 10
    }


def get_players(team_id):

    ratings = TEAM_RATINGS.get(
        team_id,
        TEAM_RATINGS["bnu"]
    )

    players = []

    for index in range(16):

        rating = ratings[index]
        position = POSITIONS[index]

        players.append({
            "name": PLAYER_NAMES[index],
            "number": index + 1,
            "position": position,
            "rating": rating,
            "stats": make_stats(
                rating,
                position
            )
        })

    return players
