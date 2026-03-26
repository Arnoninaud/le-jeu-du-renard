# ─────────────────────────────────────────────
#  main.py — Point d'entrée
#
#  Desktop Goose — clone Python/pygame pour Windows
#  Un renard pixel-art qui se balade sur ton bureau,
#  laisse des empreintes et lâche des mèmes !
#
#  Dépendances :
#      pip install pygame pywin32
#
#  Utilisation :
#      python main.py
#
#  Pour quitter : clic droit sur le renard, ou Échap.
# ─────────────────────────────────────────────

from goose import DesktopGoose

if __name__ == "__main__":
    DesktopGoose().run()
