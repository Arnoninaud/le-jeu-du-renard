# ─────────────────────────────────────────────
#  footprint.py — Empreintes de pattes
# ─────────────────────────────────────────────

import pygame
from constants import FOOT_COLOR


def make_footprint(left_foot=True):
    """Crée une surface d'empreinte de patte (gauche ou droite)."""
    s = pygame.Surface((18, 22), pygame.SRCALPHA)

    # Paume
    pygame.draw.ellipse(s, FOOT_COLOR, (3, 8, 12, 10))

    # 3 orteils
    for ox, oy in [(-1, 0), (4, -4), (9, 0)]:
        pygame.draw.ellipse(s, FOOT_COLOR, (ox + 2, oy, 5, 8))

    if not left_foot:
        s = pygame.transform.flip(s, True, False)
    return s
