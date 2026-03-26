# ─────────────────────────────────────────────
#  fox_sprite.py — Sprite pixel-art du renard
# ─────────────────────────────────────────────

import pygame
from constants import C_R, C_RD, C_RL, C_W, C_K, C_CR, PX


def _p(surface, x, y, c):
    """Dessine un pixel logique (PX×PX) à la position (x, y) de la grille."""
    pygame.draw.rect(surface, c, (x * PX, y * PX, PX, PX))


def draw_fox(surface, frame, facing_left=False):
    """
    Renard pixel-art 16×16 (grossi ×5 = 80×80), style Brysia.
    frame 0/1 alterne l'animation de marche.
    Retourne la surface (modifiée ou retournée).
    """
    surface.fill((0, 0, 0, 0))

    # ── Pixels communs aux deux frames ────────────────────────────
    base = [
        # Oreilles
        (4,0,C_K),(5,0,C_K),(9,0,C_K),(10,0,C_K),
        (3,1,C_K),(4,1,C_R),(5,1,C_CR),(6,1,C_K),
        (9,1,C_K),(10,1,C_R),(11,1,C_CR),(12,1,C_K),
        (3,2,C_K),(4,2,C_R),(5,2,C_R),(6,2,C_K),
        (9,2,C_K),(10,2,C_R),(11,2,C_R),(12,2,C_K),

        # Tête
        (3,3,C_K),(4,3,C_R),(5,3,C_R),(6,3,C_R),(7,3,C_R),
        (8,3,C_R),(9,3,C_R),(10,3,C_R),(11,3,C_R),(12,3,C_K),
        (3,4,C_K),(4,4,C_R),(5,4,C_K),(6,4,C_R),(7,4,C_R),
        (8,4,C_R),(9,4,C_R),(10,4,C_K),(11,4,C_R),(12,4,C_K),
        (3,5,C_K),(4,5,C_R),(5,5,C_R),(6,5,C_R),(7,5,C_W),
        (8,5,C_W),(9,5,C_W),(10,5,C_R),(11,5,C_R),(12,5,C_K),
        (3,6,C_K),(4,6,C_W),(5,6,C_W),(6,6,C_W),(7,6,C_K),
        (8,6,C_W),(9,6,C_W),(10,6,C_W),(11,6,C_R),(12,6,C_K),
        (4,7,C_K),(5,7,C_K),(7,7,C_K),(8,7,C_K),(11,7,C_K),

        # Cou
        (5,7,C_R),(6,7,C_R),(9,7,C_R),(10,7,C_R),

        # Corps
        (2,8,C_K),(3,8,C_R),(4,8,C_R),(5,8,C_R),(6,8,C_W),
        (7,8,C_W),(8,8,C_W),(9,8,C_R),(10,8,C_R),(11,8,C_R),(12,8,C_K),
        (2,9,C_K),(3,9,C_R),(4,9,C_R),(5,9,C_W),(6,9,C_W),
        (7,9,C_W),(8,9,C_W),(9,9,C_W),(10,9,C_R),(11,9,C_R),(12,9,C_K),
        (2,10,C_K),(3,10,C_R),(4,10,C_R),(5,10,C_W),(6,10,C_W),
        (7,10,C_W),(8,10,C_W),(9,10,C_R),(10,10,C_R),(11,10,C_K),
        (2,11,C_K),(3,11,C_RD),(4,11,C_R),(5,11,C_R),(6,11,C_W),
        (7,11,C_W),(8,11,C_R),(9,11,C_R),(10,11,C_RD),(11,11,C_K),

        # Queue (côté gauche du sprite)
        (0,7,C_K),(1,7,C_R),(2,7,C_R),
        (0,8,C_K),(1,8,C_RL),(2,8,C_K),
        (0,9,C_K),(1,9,C_W),(2,9,C_K),
        (0,10,C_K),(1,10,C_W),(2,10,C_K),
        (0,11,C_K),(1,11,C_W),(2,11,C_K),
        (0,12,C_K),(1,12,C_R),(2,12,C_K),
        (1,13,C_K),
    ]

    # ── Pattes : 2 frames d'animation ─────────────────────────────
    if frame == 0:
        legs = [
            # patte avant gauche (reculée)
            (4,12,C_K),(5,12,C_RD),(5,13,C_K),(5,14,C_K),(6,14,C_K),
            # patte avant droite (avancée)
            (8,12,C_RD),(9,12,C_K),(9,13,C_K),(9,14,C_K),(10,14,C_K),
            # patte arrière gauche (avancée)
            (3,12,C_RD),(3,13,C_K),(3,14,C_K),(4,14,C_K),
            # patte arrière droite (reculée)
            (10,12,C_K),(11,12,C_RD),(11,13,C_K),(11,14,C_K),(12,14,C_K),
        ]
    else:
        legs = [
            # patte avant gauche (avancée)
            (4,12,C_RD),(5,12,C_K),(4,13,C_K),(4,14,C_K),(5,14,C_K),
            # patte avant droite (reculée)
            (8,12,C_K),(9,12,C_RD),(10,13,C_K),(10,14,C_K),(11,14,C_K),
            # patte arrière gauche (reculée)
            (3,12,C_K),(4,12,C_K),(4,13,C_K),(3,14,C_K),(4,14,C_K),
            # patte arrière droite (avancée)
            (10,12,C_RD),(11,12,C_K),(11,13,C_K),(10,14,C_K),(11,14,C_K),
        ]

    for (x, y, c) in base + legs:
        _p(surface, x, y, c)

    # Reflets dans les yeux
    pygame.draw.rect(surface, (255, 255, 255), (5 * PX + 1, 4 * PX + 1, 2, 2))
    pygame.draw.rect(surface, (255, 255, 255), (10 * PX + 1, 4 * PX + 1, 2, 2))

    if facing_left:
        surface = pygame.transform.flip(surface, True, False)
    return surface


def make_goose_frames():
    """Génère les 4 surfaces animées (2 frames × 2 directions)."""
    frames = {}
    for f in (0, 1):
        s = pygame.Surface((80, 80), pygame.SRCALPHA)
        draw_fox(s, f, facing_left=False)
        frames[("right", f)] = s

        s2 = pygame.Surface((80, 80), pygame.SRCALPHA)
        draw_fox(s2, f, facing_left=True)
        frames[("left", f)] = s2
    return frames
