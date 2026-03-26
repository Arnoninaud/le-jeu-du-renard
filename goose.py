# ─────────────────────────────────────────────
#  goose.py — Classe principale DesktopGoose
# ─────────────────────────────────────────────

import math
import random
import sys
import time

import pygame
import win32api

from constants import (
    FPS, GOOSE_SPEED, SCARED_SPEED,
    FOOT_INTERVAL, FOOT_LIFETIME,
    MEME_INTERVAL, HONK_INTERVAL,
    MEMES,
)
from footprint import make_footprint
from fox_sprite import make_goose_frames
from meme_window import MemeWindow
from win32_utils import setup_transparent_window


class DesktopGoose:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Desktop Goose")

        # Dimensions du bureau
        self.sw = win32api.GetSystemMetrics(0)
        self.sh = win32api.GetSystemMetrics(1)

        # Fenêtre plein-écran sans bordure
        self.screen = pygame.display.set_mode(
            (self.sw, self.sh),
            pygame.NOFRAME | pygame.SHOWN,
        )
        self.clock = pygame.time.Clock()

        # Overlay transparent Win32
        hwnd = pygame.display.get_wm_info()["window"]
        setup_transparent_window(hwnd)

        # ── Ressources ─────────────────────────────
        self.frames     = make_goose_frames()
        self.foot_left  = make_footprint(True)
        self.foot_right = make_footprint(False)
        self.font_meme  = pygame.font.SysFont("Segoe UI", 15, bold=False)

        # ── État du renard ─────────────────────────
        self.x      = float(self.sw // 2)
        self.y      = float(self.sh // 2)
        self.vx     = 0.0
        self.vy     = 0.0
        self.tx     = random.uniform(100, self.sw - 100)
        self.ty     = random.uniform(100, self.sh - 200)
        self.scared      = False
        self.scare_timer = 0.0
        self.anim_frame  = 0
        self.anim_timer  = 0.0
        self.direction   = "right"

        # ── Empreintes ─────────────────────────────
        self.footprints  = []
        self.last_foot   = time.time()
        self.foot_toggle = True

        # ── Mèmes ──────────────────────────────────
        self.memes     = []
        self.last_meme = time.time()

        # ── Drag & drop ────────────────────────────
        self.dragging = False
        self.drag_ox  = 0.0
        self.drag_oy  = 0.0

        # ── Timers divers ──────────────────────────
        self.last_honk = time.time()

    # ── Cible aléatoire ────────────────────────────
    def pick_target(self):
        self.tx = random.uniform(60, self.sw - 60)
        self.ty = random.uniform(60, self.sh - 180)

    # ── Mise à jour de la logique ──────────────────
    def update(self, dt):
        now = time.time()

        # Fuite de la souris
        mx, my     = win32api.GetCursorPos()
        dx_mouse   = self.x - mx
        dy_mouse   = self.y - my
        dist_mouse = math.hypot(dx_mouse, dy_mouse)

        if dist_mouse < 1:
            self.scared      = True
            self.scare_timer = 1.0

        if dist_mouse != 0:
            self.vx = self.vx * 0.7 + (dx_mouse / dist_mouse) * 3
            self.vy = self.vy * 0.7 + (dy_mouse / dist_mouse) * 3

        # Drag & drop
        if self.dragging:
            self.x = float(mx - self.drag_ox)
            self.y = float(my - self.drag_oy)
            return

        # Décompte de la peur
        if self.scared:
            self.scare_timer -= dt
            if self.scare_timer <= 0:
                self.scared = False

        speed = SCARED_SPEED if self.scared else GOOSE_SPEED
        dx    = self.tx - self.x
        dy    = self.ty - self.y
        dist  = math.hypot(dx, dy)

        if dist < 8:
            self.pick_target()
            if now - self.last_meme > MEME_INTERVAL and random.random() < 0.4:
                self._drop_meme()
            if now - self.last_honk > HONK_INTERVAL and random.random() < 0.5:
                self._honk()
        else:
            nx = dx / dist
            ny = dy / dist
            self.vx = self.vx * 0.85 + nx * speed * 0.15
            self.vy = self.vy * 0.85 + ny * speed * 0.15

        self.x += self.vx
        self.y += self.vy

        # Limites de l'écran
        self.x = max(0, min(self.sw - 80, self.x))
        self.y = max(0, min(self.sh - 80, self.y))

        # Direction du regard
        if self.vx < -0.3:
            self.direction = "left"
        elif self.vx > 0.3:
            self.direction = "right"

        # Animation de marche
        self.anim_timer += dt
        if self.anim_timer > 0.18:
            self.anim_frame = 1 - self.anim_frame
            self.anim_timer = 0.0

        # Dépôt d'empreintes
        if dist > 5 and now - self.last_foot > FOOT_INTERVAL:
            ox = -10 if self.foot_toggle else 30
            self.footprints.append({
                "surf": self.foot_left if self.foot_toggle else self.foot_right,
                "x"  : self.x + 20 + ox,
                "y"  : self.y + 60,
                "born": now,
            })
            self.foot_toggle = not self.foot_toggle
            self.last_foot   = now

        # Purge des vieilles empreintes
        self.footprints = [
            f for f in self.footprints if now - f["born"] < FOOT_LIFETIME
        ]

        # Mise à jour des mèmes
        for m in self.memes:
            m.update()
        self.memes = [m for m in self.memes if not m.is_dead()]

    # ── Mème & Honk ────────────────────────────────
    def _drop_meme(self):
        txt = random.choice(MEMES)
        self.memes.append(MemeWindow(txt, self.x + 40, self.y, self.font_meme))
        self.last_meme = time.time()

    def _honk(self):
        self._drop_meme()
        self.last_honk = time.time()

    # ── Dessin ─────────────────────────────────────
    def draw(self):
        self.screen.fill((0, 0, 0))   # noir = couleur clé de transparence
        now = time.time()

        # Empreintes
        for fp in self.footprints:
            age   = now - fp["born"]
            alpha = max(0, int(220 * (1 - age / FOOT_LIFETIME)))
            s = fp["surf"].copy()
            s.set_alpha(alpha)
            self.screen.blit(s, (int(fp["x"]), int(fp["y"])))

        # Mèmes
        for m in self.memes:
            m.draw(self.screen)

        # Renard
        key = (self.direction, self.anim_frame)
        self.screen.blit(self.frames[key], (int(self.x), int(self.y)))

        pygame.display.flip()

    # ── Gestion des événements ──────────────────────
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                gx, gy = int(self.x), int(self.y)

                # Clic droit sur le renard → quitter
                if event.button == 3 and gx <= mx <= gx + 80 and gy <= my <= gy + 80:
                    return False

                # Clic gauche sur le renard → drag
                if event.button == 1 and gx <= mx <= gx + 80 and gy <= my <= gy + 80:
                    self.dragging = True
                    self.drag_ox  = mx - self.x
                    self.drag_oy  = my - self.y

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.dragging:
                    self.dragging    = False
                    self.scared      = True
                    self.scare_timer = 2.5
                    self.pick_target()
                    self._honk()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False

        return True

    # ── Boucle principale ───────────────────────────
    def run(self):
        running = True
        while running:
            dt      = self.clock.tick(FPS) / 1000.0
            running = self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()
