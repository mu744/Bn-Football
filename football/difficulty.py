# ==========================================
# BN-FOOTBALL
# SYSTEME DE DIFFICULTE DE L'IA
# ==========================================

DIFFICULTIES = {

    "beginner": {
        "name": "Debutant",
        "level": 0,

        # Prise de decision
        "reaction": 0.45,
        "decision_speed": 0.45,

        # Technique
        "pass_accuracy": 0.55,
        "shot_accuracy": 0.55,

        # Intelligence defensive
        "marking": 0.40,
        "positioning": 0.40,
        "interception": 0.35,

        # Pressing
        "pressing": 0.25,

        # Erreurs
        "error_rate": 0.45,

        # Vitesse de poursuite
        "chase_speed": 0.75,
    },

    "normal": {
        "name": "Normal",
        "level": 1,

        "reaction": 0.60,
        "decision_speed": 0.60,

        "pass_accuracy": 0.68,
        "shot_accuracy": 0.65,

        "marking": 0.55,
        "positioning": 0.55,
        "interception": 0.50,

        "pressing": 0.40,

        "error_rate": 0.32,

        "chase_speed": 0.85,
    },

    "high": {
        "name": "Haut niveau",
        "level": 2,

        "reaction": 0.72,
        "decision_speed": 0.70,

        "pass_accuracy": 0.76,
        "shot_accuracy": 0.73,

        "marking": 0.68,
        "positioning": 0.68,
        "interception": 0.63,

        "pressing": 0.55,

        "error_rate": 0.24,

        "chase_speed": 0.95,
    },

    "pro": {
        "name": "Pro",
        "level": 3,

        "reaction": 0.82,
        "decision_speed": 0.80,

        "pass_accuracy": 0.83,
        "shot_accuracy": 0.80,

        "marking": 0.78,
        "positioning": 0.77,
        "interception": 0.73,

        "pressing": 0.68,

        "error_rate": 0.17,

        "chase_speed": 1.00,
    },

    "superstar": {
        "name": "Superstar",
        "level": 4,

        "reaction": 0.91,
        "decision_speed": 0.90,

        "pass_accuracy": 0.89,
        "shot_accuracy": 0.87,

        "marking": 0.87,
        "positioning": 0.86,
        "interception": 0.84,

        "pressing": 0.82,

        "error_rate": 0.10,

        "chase_speed": 1.05,
    },

    "legend": {
        "name": "Legende",
        "level": 5,

        "reaction": 1.00,
        "decision_speed": 1.00,

        "pass_accuracy": 0.95,
        "shot_accuracy": 0.93,

        "marking": 0.94,
        "positioning": 0.94,
        "interception": 0.92,

        "pressing": 0.95,

        "error_rate": 0.05,

        "chase_speed": 1.10,
    }
}


DEFAULT_DIFFICULTY = "normal"


def get_difficulty(name):
    """
    Retourne les parametres du niveau choisi.
    """

    return DIFFICULTIES.get(
        name,
        DIFFICULTIES[DEFAULT_DIFFICULTY]
    )


def get_difficulty_names():
    """
    Retourne les noms internes des niveaux.
    """

    return list(DIFFICULTIES.keys())


def get_difficulty_display_names():
    """
    Retourne les noms affichables dans le jeu.
    """

    return [
        data["name"]
        for data in DIFFICULTIES.values()
    ]


def get_next_difficulty(current):
    """
    Passe au niveau suivant.
    """

    names = get_difficulty_names()

    if current not in names:
        return names[0]

    index = names.index(current)

    if index >= len(names) - 1:
        return names[-1]

    return names[index + 1]


def get_previous_difficulty(current):
    """
    Passe au niveau precedent.
    """

    names = get_difficulty_names()

    if current not in names:
        return names[0]

    index = names.index(current)

    if index <= 0:
        return names[0]

    return names[index - 1]
