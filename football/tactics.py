FORMATIONS = {
    "4-3-3": {
        "GK":  [(0.50, 0.88)],
        "DF":  [(0.18, 0.68), (0.38, 0.74), (0.62, 0.74), (0.82, 0.68)],
        "MC":  [(0.28, 0.52), (0.50, 0.57), (0.72, 0.52)],
        "AT":  [(0.18, 0.30), (0.50, 0.25), (0.82, 0.30)]
    },

    "4-4-2": {
        "GK":  [(0.50, 0.88)],
        "DF":  [(0.18, 0.68), (0.38, 0.74), (0.62, 0.74), (0.82, 0.68)],
        "MC":  [(0.18, 0.48), (0.38, 0.54), (0.62, 0.54), (0.82, 0.48)],
        "AT":  [(0.40, 0.29), (0.60, 0.29)]
    },

    "4-2-3-1": {
        "GK":  [(0.50, 0.88)],
        "DF":  [(0.18, 0.68), (0.38, 0.74), (0.62, 0.74), (0.82, 0.68)],
        "MC":  [(0.38, 0.54), (0.62, 0.54), (0.22, 0.36), (0.50, 0.40), (0.78, 0.36)],
        "AT":  [(0.50, 0.22)]
    }
}


def get_positions(formation, field):
    data = FORMATIONS.get(formation, FORMATIONS["4-3-3"])

    positions = []

    for role in ["GK", "DF", "MC", "AT"]:
        for nx, ny in data[role]:
            x = int(field.left + field.width * nx)
            y = int(field.top + field.height * ny)
            positions.append((x, y))

    return positions


def get_formation_names():
    return list(FORMATIONS.keys())
