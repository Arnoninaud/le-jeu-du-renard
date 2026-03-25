"""
Desktop Goose - Clone Python/pygame pour Windows
Une oie qui se balade sur ton bureau, laisse des empreintes et lâche des mèmes !

Dépendances :
    pip install pygame pywin32

Utilisation :
    python desktop_goose.py

Pour quitter : clic droit sur l'oie ou ferme via le gestionnaire de tâches.
"""

import pygame
import sys
import random
import math
import time
import ctypes
import win32api
import win32con
import win32gui

# ─────────────────────────────────────────────
#  Constantes
# ─────────────────────────────────────────────
FPS          = 60
GOOSE_SPEED  = 2.5
SCARED_SPEED = 6.0
FOOT_INTERVAL   = 0.22   # secondes entre chaque empreinte
FOOT_LIFETIME   = 6.0    # secondes avant que l'empreinte disparaisse
MEME_INTERVAL   = 8.0    # secondes entre les mèmes
HONK_INTERVAL   = 4.0    # secondes entre les HONK
MEME_LIFETIME   = 5.0

MEMES = [
    "AWA",
    "AWAWAAA!",
    "Tu travailles trop.",
    "Périmètre sécurisé 🪿",
    "Fichier supprimé 😈",
    "404 : Repos introuvable",
    "Mise à jour en cours…",
    "Je suis partout.",
    "Pain au choc' ou chocolatine ??",
    "L'oie est le patron.",
    "Reboot imminent.",
    "Corruption détectée.",
    "Tu ne m'arrêteras pas.",
    "🎵 Mambo No.5",
]

# Couleurs (palette pixel-art)
WHITE      = (255, 255, 255)
BLACK      = (0,   0,   0  )
ORANGE     = (230, 130, 20 )
DARK_GRAY  = (170, 170, 170)
LIGHT_GRAY = (220, 220, 220)
SHADOW     = (100, 100, 100, 80)
FOOT_COLOR = (160, 110, 60, 160)
BG_MEME    = (255, 255, 240)
BORDER_MEME= (200, 170, 80 )
TEXT_MEME  = (60,  40,  10 )

# ─────────────────────────────────────────────
#  Palette pixel-art style "Brysia"
# ─────────────────────────────────────────────
C_R  = (210,  90,  30)   # roux principal
C_RD = (140,  50,  10)   # roux foncé / contour
C_RL = (240, 150,  70)   # roux clair
C_W  = (245, 240, 220)   # blanc cassé (ventre, museau, bout queue)
C_K  = ( 25,  15,  10)   # noir contour
C_CR = (255, 200, 150)   # crème intérieur oreilles

PX = 5   # 1 pixel logique = 5px → sprite 16×16 = 80×80

def _p(surface, x, y, c):
    pygame.draw.rect(surface, c, (x * PX, y * PX, PX, PX))

# ─────────────────────────────────────────────
#  Dessin du renard en pixel-art (Surface 80×80)
# ─────────────────────────────────────────────
def draw_fox(surface, frame, facing_left=False):
    """
    Renard pixel-art 16x16 (grossi x5 = 80x80), style Brysia.
    frame 0/1 alterne l'animation de marche.
    """
    surface.fill((0, 0, 0, 0))

    # ── Sprite frame 0 (patte droite avant) ───────────────────────
    #  Grille : chaque tuple = (col, ligne, couleur)
    #  Origine (0,0) = coin haut-gauche

    base = [
        # ── Oreilles ──────────────────────────────────
        (4,0,C_K),(5,0,C_K),(9,0,C_K),(10,0,C_K),
        (3,1,C_K),(4,1,C_R),(5,1,C_CR),(6,1,C_K),
        (9,1,C_K),(10,1,C_R),(11,1,C_CR),(12,1,C_K),
        (3,2,C_K),(4,2,C_R),(5,2,C_R),(6,2,C_K),
        (9,2,C_K),(10,2,C_R),(11,2,C_R),(12,2,C_K),

        # ── Tête ─────────────────────────────────────
        (3,3,C_K),(4,3,C_R),(5,3,C_R),(6,3,C_R),(7,3,C_R),
        (8,3,C_R),(9,3,C_R),(10,3,C_R),(11,3,C_R),(12,3,C_K),
        (3,4,C_K),(4,4,C_R),(5,4,C_K),(6,4,C_R),(7,4,C_R),
        (8,4,C_R),(9,4,C_R),(10,4,C_K),(11,4,C_R),(12,4,C_K),
        (3,5,C_K),(4,5,C_R),(5,5,C_R),(6,5,C_R),(7,5,C_W),
        (8,5,C_W),(9,5,C_W),(10,5,C_R),(11,5,C_R),(12,5,C_K),
        (3,6,C_K),(4,6,C_W),(5,6,C_W),(6,6,C_W),(7,6,C_K),
        (8,6,C_W),(9,6,C_W),(10,6,C_W),(11,6,C_R),(12,6,C_K),
        (4,7,C_K),(5,7,C_K),(7,7,C_K),(8,7,C_K),(11,7,C_K),

        # ── Cou ──────────────────────────────────────
        (5,7,C_R),(6,7,C_R),(9,7,C_R),(10,7,C_R),

        # ── Corps ────────────────────────────────────
        (2,8,C_K),(3,8,C_R),(4,8,C_R),(5,8,C_R),(6,8,C_W),
        (7,8,C_W),(8,8,C_W),(9,8,C_R),(10,8,C_R),(11,8,C_R),(12,8,C_K),
        (2,9,C_K),(3,9,C_R),(4,9,C_R),(5,9,C_W),(6,9,C_W),
        (7,9,C_W),(8,9,C_W),(9,9,C_W),(10,9,C_R),(11,9,C_R),(12,9,C_K),
        (2,10,C_K),(3,10,C_R),(4,10,C_R),(5,10,C_W),(6,10,C_W),
        (7,10,C_W),(8,10,C_W),(9,10,C_R),(10,10,C_R),(11,10,C_K),
        (2,11,C_K),(3,11,C_RD),(4,11,C_R),(5,11,C_R),(6,11,C_W),
        (7,11,C_W),(8,11,C_R),(9,11,C_R),(10,11,C_RD),(11,11,C_K),

        # ── Queue (côté gauche du sprite) ────────────
        (0,7,C_K),(1,7,C_R),(2,7,C_R),
        (0,8,C_K),(1,8,C_RL),(2,8,C_K),
        (0,9,C_K),(1,9,C_W),(2,9,C_K),
        (0,10,C_K),(1,10,C_W),(2,10,C_K),
        (0,11,C_K),(1,11,C_W),(2,11,C_K),
        (0,12,C_K),(1,12,C_R),(2,12,C_K),
        (1,13,C_K),
    ]

    # ── Pattes : 2 frames ─────────────────────────
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

    # Reflet dans les yeux
    pygame.draw.rect(surface, (255,255,255), (5*PX+1, 4*PX+1, 2, 2))
    pygame.draw.rect(surface, (255,255,255), (10*PX+1, 4*PX+1, 2, 2))

    if facing_left:
        surface = pygame.transform.flip(surface, True, False)
    return surface


def make_goose_frames():
    """Génère les 4 surfaces (2 frames × 2 directions)."""
    frames = {}
    for f in (0, 1):
        s = pygame.Surface((80, 80), pygame.SRCALPHA)
        draw_fox(s, f, facing_left=False)
        frames[("right", f)] = s
        s2 = pygame.Surface((80, 80), pygame.SRCALPHA)
        draw_fox(s2, f, facing_left=True)
        frames[("left", f)] = s2
    return frames


# ─────────────────────────────────────────────
#  Empreinte de patte
# ─────────────────────────────────────────────
def make_footprint(left_foot=True):
    s = pygame.Surface((18, 22), pygame.SRCALPHA)
    # Paume
    pygame.draw.ellipse(s, FOOT_COLOR, (3, 8, 12, 10))
    # 3 orteils
    for i, (ox, oy) in enumerate([(-1, 0), (4, -4), (9, 0)]):
        pygame.draw.ellipse(s, FOOT_COLOR, (ox + 2, oy, 5, 8))
    if not left_foot:
        s = pygame.transform.flip(s, True, False)
    return s


# ─────────────────────────────────────────────
#  Fenêtre mème flottante
# ─────────────────────────────────────────────
class MemeWindow:
    def __init__(self, text, x, y, font):
        self.text      = text
        self.font      = font
        self.born      = time.time()
        self.lifetime  = MEME_LIFETIME
        self.alpha     = 255

        tw, th = font.size(text)
        self.w  = tw + 28
        self.h  = th + 18
        self.x  = x
        self.y  = y - self.h - 10
        self.surf = self._make_surf()

    def _make_surf(self):
        s = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        pygame.draw.rect(s, (*BG_MEME, 230),    (0, 0, self.w, self.h), border_radius=8)
        pygame.draw.rect(s, (*BORDER_MEME, 200), (0, 0, self.w, self.h), 2, border_radius=8)
        txt = self.font.render(self.text, True, TEXT_MEME)
        s.blit(txt, (14, 9))
        return s

    def update(self):
        age   = time.time() - self.born
        ratio = age / self.lifetime
        self.y     -= 0.3
        self.alpha  = max(0, int(255 * (1 - ratio)))

    def is_dead(self):
        return time.time() - self.born > self.lifetime

    def draw(self, screen):
        s = self.surf.copy()
        s.set_alpha(self.alpha)
        screen.blit(s, (int(self.x - self.w // 2), int(self.y)))


# ─────────────────────────────────────────────
#  Fenêtre transparente superposée (overlay)
# ─────────────────────────────────────────────
def setup_transparent_window(hwnd):
    """Rend la fenêtre click-through et toujours au premier plan."""
    # Style étendu : transparent + sans tâche dans la barre
    ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    ex_style |= win32con.WS_EX_LAYERED
    ex_style |= win32con.WS_EX_TRANSPARENT
    ex_style |= win32con.WS_EX_TOOLWINDOW
    ex_style &= ~win32con.WS_EX_APPWINDOW
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style)

    # Couleur clé de transparence = noir pur (0,0,0)
    win32gui.SetLayeredWindowAttributes(
        hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY
    )
    # Toujours au premier plan
    win32gui.SetWindowPos(
        hwnd, win32con.HWND_TOPMOST,
        0, 0, 0, 0,
        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
    )


# ─────────────────────────────────────────────
#  Classe principale : l'oie
# ─────────────────────────────────────────────
class DesktopGoose:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Desktop Goose")

        # Taille du bureau
        self.sw = win32api.GetSystemMetrics(0)  # largeur écran
        self.sh = win32api.GetSystemMetrics(1)  # hauteur écran

        # Fenêtre plein écran transparente
        self.screen = pygame.display.set_mode(
            (self.sw, self.sh),
            pygame.NOFRAME | pygame.SHOWN
        )
        self.clock  = pygame.time.Clock()

        # Rend la fenêtre transparente via Win32
        hwnd = pygame.display.get_wm_info()["window"]
        setup_transparent_window(hwnd)

        # Ressources
        self.frames     = make_goose_frames()
        self.foot_left  = make_footprint(True)
        self.foot_right = make_footprint(False)
        self.font_meme  = pygame.font.SysFont("Segoe UI", 15, bold=False)

        # État de l'oie
        self.x      = float(self.sw // 2)
        self.y      = float(self.sh // 2)
        self.vx     = 0.0
        self.vy     = 0.0
        self.tx     = random.uniform(100, self.sw - 100)
        self.ty     = random.uniform(100, self.sh - 200)
        self.scared = False
        self.scare_timer = 0.0
        self.anim_frame  = 0
        self.anim_timer  = 0.0
        self.direction   = "right"

        # Empreintes
        self.footprints  = []   # [(surf, x, y, born, left)]
        self.last_foot   = time.time()
        self.foot_toggle = True

        # Mèmes
        self.memes       = []
        self.last_meme   = time.time()

        # Drag & drop souris
        self.dragging    = False
        self.drag_ox     = 0.0
        self.drag_oy     = 0.0

        # Timers
        self.last_honk   = time.time()

    # ── Logique de déplacement ──────────────────
    def pick_target(self):
        self.tx = random.uniform(60, self.sw - 60)
        self.ty = random.uniform(60, self.sh - 180)

    def update(self, dt):
        now = time.time()
        # ── Fuite de la souris ─────────────────────
        mx, my = win32api.GetCursorPos()

        dx_mouse = self.x - mx
        dy_mouse = self.y - my
        dist_mouse = math.hypot(dx_mouse, dy_mouse)

        if dist_mouse < 1:  # distance de détection
         self.scared = True
         self.scare_timer = 1.0

        if dist_mouse != 0:
           self.vx = self.vx * 0.7 + (dx_mouse / dist_mouse) * 3
           self.vy = self.vy * 0.7 + (dy_mouse / dist_mouse) * 3
        if self.dragging:
            mx, my = win32api.GetCursorPos()
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
            # Mème aléatoire
            if now - self.last_meme > MEME_INTERVAL and random.random() < 0.4:
                self._drop_meme()
            # Honk aléatoire
            if now - self.last_honk > HONK_INTERVAL and random.random() < 0.5:
                self._honk()
        else:
            nx = dx / dist
            ny = dy / dist
            self.vx = self.vx * 0.85 + nx * speed * 0.15
            self.vy = self.vy * 0.85 + ny * speed * 0.15

        self.x += self.vx
        self.y += self.vy

        # Garder dans les limites
        self.x = max(0, min(self.sw - 80, self.x))
        self.y = max(0, min(self.sh - 80, self.y))

        # Direction du regard
        if self.vx < -0.3:
            self.direction = "left"
        elif self.vx > 0.3:
            self.direction = "right"

        # Animation
        self.anim_timer += dt
        if self.anim_timer > 0.18:
            self.anim_frame  = 1 - self.anim_frame
            self.anim_timer  = 0.0

        # Empreintes
        if dist > 5 and now - self.last_foot > FOOT_INTERVAL:
            self.footprints.append({
                "surf" : self.foot_left if self.foot_toggle else self.foot_right,
                "x"    : self.x + 20 + (- 10 if self.foot_toggle else 30),
                "y"    : self.y + 60,
                "born" : now,
            })
            self.foot_toggle = not self.foot_toggle
            self.last_foot   = now

        # Purge vieilles empreintes
        self.footprints = [f for f in self.footprints if now - f["born"] < FOOT_LIFETIME]

        # Mise à jour mèmes
        for m in self.memes:
            m.update()
        self.memes = [m for m in self.memes if not m.is_dead()]

    # ── Mème & Honk ────────────────────────────
    def _drop_meme(self):
        txt = random.choice(MEMES)
        m   = MemeWindow(txt, self.x + 40, self.y, self.font_meme)
        self.memes.append(m)
        self.last_meme = time.time()

    def _honk(self):
        self._drop_meme()   # le honk = un mème "HONK !"
        self.last_honk = time.time()

    # ── Dessin ────────────────────────────────
    def draw(self):
        self.screen.fill((0, 0, 0))   # noir = couleur clé de transparence

        # Empreintes
        now = time.time()
        for fp in self.footprints:
            age   = now - fp["born"]
            alpha = max(0, int(220 * (1 - age / FOOT_LIFETIME)))
            s = fp["surf"].copy()
            s.set_alpha(alpha)
            self.screen.blit(s, (int(fp["x"]), int(fp["y"])))

        # Mèmes
        for m in self.memes:
            m.draw(self.screen)

        # Oie
        key = (self.direction, self.anim_frame)
        self.screen.blit(self.frames[key], (int(self.x), int(self.y)))

        pygame.display.flip()

    # ── Gestion des événements ─────────────────
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                gx, gy = int(self.x), int(self.y)

                # Clic droit → quitter
                if event.button == 3 and gx <= mx <= gx+80 and gy <= my <= gy+80:
                    return False

                # Clic gauche sur l'oie → drag
                if event.button == 1 and gx <= mx <= gx+80 and gy <= my <= gy+80:
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

        return True

    # ── Boucle principale ──────────────────────
    def run(self):
        running = True
        while running:
            dt      = self.clock.tick(FPS) / 1000.0
            running = self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()
        sys.exit()


# ─────────────────────────────────────────────
if __name__ == "__main__":
    goose = DesktopGoose()
    goose.run()