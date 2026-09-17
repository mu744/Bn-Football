import pygame

# Resolution interne du jeu
LOGICAL_WIDTH = 900
LOGICAL_HEIGHT = 600

# Fenetre adaptee au telephone
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 360


def create_window():
    return pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT)
    )


def scale_surface(logical_surface, screen):

    screen_width, screen_height = screen.get_size()

    ratio_x = screen_width / LOGICAL_WIDTH
    ratio_y = screen_height / LOGICAL_HEIGHT

    ratio = min(ratio_x, ratio_y)

    width = int(LOGICAL_WIDTH * ratio)
    height = int(LOGICAL_HEIGHT * ratio)

    scaled = pygame.transform.smoothscale(
        logical_surface,
        (width, height)
    )

    screen.fill((3, 8, 15))

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    screen.blit(
        scaled,
        (x, y)
    )


def to_logical_pos(pos, screen):

    screen_width, screen_height = screen.get_size()

    ratio_x = screen_width / LOGICAL_WIDTH
    ratio_y = screen_height / LOGICAL_HEIGHT

    ratio = min(ratio_x, ratio_y)

    width = LOGICAL_WIDTH * ratio
    height = LOGICAL_HEIGHT * ratio

    offset_x = (screen_width - width) / 2
    offset_y = (screen_height - height) / 2

    x = (pos[0] - offset_x) / ratio
    y = (pos[1] - offset_y) / ratio

    return (
        int(x),
        int(y)
    )


def logical_mouse_pos(screen):

    return to_logical_pos(
        pygame.mouse.get_pos(),
        screen
    )
