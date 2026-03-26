# ─────────────────────────────────────────────
#  constants.py — Constantes & palettes de couleurs
# ─────────────────────────────────────────────

FPS           = 60
GOOSE_SPEED   = 2.5
SCARED_SPEED  = 6.0
FOOT_INTERVAL = 0.22   # secondes entre chaque empreinte
FOOT_LIFETIME = 6.0    # secondes avant que l'empreinte disparaisse
MEME_INTERVAL = 8.0    # secondes entre les mèmes
HONK_INTERVAL = 4.0    # secondes entre les HONK
MEME_LIFETIME = 5.0

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

# ── Couleurs générales ────────────────────────
WHITE      = (255, 255, 255)
BLACK      = (0,   0,   0  )
ORANGE     = (230, 130, 20 )
DARK_GRAY  = (170, 170, 170)
LIGHT_GRAY = (220, 220, 220)
SHADOW     = (100, 100, 100, 80)

# ── Empreintes ────────────────────────────────
FOOT_COLOR = (160, 110, 60, 160)

# ── Fenêtres mèmes ────────────────────────────
BG_MEME    = (255, 255, 240)
BORDER_MEME= (200, 170, 80 )
TEXT_MEME  = (60,  40,  10 )

# ── Palette pixel-art du renard (style "Brysia") ──
C_R  = (210,  90,  30)   # roux principal
C_RD = (140,  50,  10)   # roux foncé / contour
C_RL = (240, 150,  70)   # roux clair
C_W  = (245, 240, 220)   # blanc cassé (ventre, museau, bout queue)
C_K  = ( 25,  15,  10)   # noir contour
C_CR = (255, 200, 150)   # crème intérieur oreilles

PX = 5   # 1 pixel logique = 5 px → sprite 16×16 affiché en 80×80
