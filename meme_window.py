# ─────────────────────────────────────────────
#  meme_window.py — Fenêtres mèmes flottantes
# ─────────────────────────────────────────────

import time
import pygame
from constants import BG_MEME, BORDER_MEME, TEXT_MEME, MEME_LIFETIME


class MemeWindow:
    def __init__(self, text, x, y, font):
        self.text     = text
        self.font     = font
        self.born     = time.time()
        self.lifetime = MEME_LIFETIME
        self.alpha    = 255

        tw, th    = font.size(text)
        self.w    = tw + 28
        self.h    = th + 18
        self.x    = x
        self.y    = y - self.h - 10
        self.surf = self._make_surf()

    def _make_surf(self):
        s = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        pygame.draw.rect(s, (*BG_MEME, 230),     (0, 0, self.w, self.h), border_radius=8)
        pygame.draw.rect(s, (*BORDER_MEME, 200),  (0, 0, self.w, self.h), 2, border_radius=8)
        txt = self.font.render(self.text, True, TEXT_MEME)
        s.blit(txt, (14, 9))
        return s

    def update(self):
        age        = time.time() - self.born
        ratio      = age / self.lifetime
        self.y    -= 0.3
        self.alpha = max(0, int(255 * (1 - ratio)))

    def is_dead(self):
        return time.time() - self.born > self.lifetime

    def draw(self, screen):
        s = self.surf.copy()
        s.set_alpha(self.alpha)
        screen.blit(s, (int(self.x - self.w // 2), int(self.y)))
