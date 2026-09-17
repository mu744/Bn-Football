import json
import os


SAVE_FILE = "saves/player_save.json"


DEFAULT_SAVE = {
    "club": "BN United",
    "team_id": "bnu",

    "season": 1,
    "match": 1,

    "wins": 0,
    "draws": 0,
    "losses": 0,
    "points": 0,

    "formation": "4-3-3",

"difficulty": "normal",

    "lineup": [
        1, 2, 3, 4, 5,
        6, 7, 8,
        9, 10, 11
    ]
}


def load_game():

    if not os.path.exists(SAVE_FILE):

        return DEFAULT_SAVE.copy()

    try:

        with open(
            SAVE_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        result = DEFAULT_SAVE.copy()

        result.update(data)

        return result

    except Exception:

        return DEFAULT_SAVE.copy()


def save_game(data):

    os.makedirs(
        "saves",
        exist_ok=True
    )

    with open(
        SAVE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )
