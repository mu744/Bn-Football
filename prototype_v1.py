import pygame
import sys

# =========================
# INITIALISATION
# =========================

pygame.init()

LARGEUR = 900
HAUTEUR = 600

ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("BN-Football")

horloge = pygame.time.Clock()

# =========================
# COULEURS
# =========================

VERT = (30, 130, 60)
BLANC = (255, 255, 255)
BLEU = (30, 100, 220)
NOIR = (20, 20, 20)

# =========================
# JOUEUR
# =========================

joueur_x = 200
joueur_y = 300

vitesse = 5

# =========================
# BALLON
# =========================

ballon_x = 300
ballon_y = 300

# =========================
# BOUCLE DU JEU
# =========================

jeu = True

while jeu:

    # --- ÉVÉNEMENTS ---
    for evenement in pygame.event.get():

        if evenement.type == pygame.QUIT:
            jeu = False

    # --- TOUCHES ---
    touches = pygame.key.get_pressed()

    if touches[pygame.K_UP]:
        joueur_y -= vitesse

    if touches[pygame.K_DOWN]:
        joueur_y += vitesse

    if touches[pygame.K_LEFT]:
        joueur_x -= vitesse

    if touches[pygame.K_RIGHT]:
        joueur_x += vitesse

    # --- TERRAIN ---
    ecran.fill(VERT)

    pygame.draw.rect(
        ecran,
        BLANC,
        (50, 50, 800, 500),
        5
    )

    # Ligne centrale
    pygame.draw.line(
        ecran,
        BLANC,
        (450, 50),
        (450, 550),
        5
    )

    # Cercle central
    pygame.draw.circle(
        ecran,
        BLANC,
        (450, 300),
        80,
        5
    )

    # Point central
    pygame.draw.circle(
        ecran,
        BLANC,
        (450, 300),
        8
    )

    # --- JOUEUR ---
    pygame.draw.circle(
        ecran,
        BLEU,
        (joueur_x, joueur_y),
        20
    )

    # --- BALLON ---
    pygame.draw.circle(
        ecran,
        BLANC,
        (ballon_x, ballon_y),
        12
    )

    pygame.draw.circle(
        ecran,
        NOIR,
        (ballon_x, ballon_y),
        12,
        2
    )

    # --- AFFICHAGE ---
    pygame.display.flip()

    horloge.tick(60)

# =========================
# FIN
# =========================

pygame.quit()
sys.exit()
