# ─────────────────────────────────────────────
#  win32_utils.py — Fenêtre overlay transparente (Win32)
# ─────────────────────────────────────────────

import win32api
import win32con
import win32gui


def setup_transparent_window(hwnd):
    """
    Rend la fenêtre pygame :
      - Click-through (les clics passent à travers)
      - Toujours au premier plan (topmost)
      - Invisible dans la barre des tâches
      - Couleur-clé noire (0,0,0) = transparence
    """
    ex_style  = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    ex_style |= win32con.WS_EX_LAYERED
    ex_style |= win32con.WS_EX_TRANSPARENT
    ex_style |= win32con.WS_EX_TOOLWINDOW
    ex_style &= ~win32con.WS_EX_APPWINDOW
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, ex_style)

    # Noir pur = couleur clé de transparence
    win32gui.SetLayeredWindowAttributes(
        hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY
    )

    # Toujours au premier plan
    win32gui.SetWindowPos(
        hwnd, win32con.HWND_TOPMOST,
        0, 0, 0, 0,
        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE,
    )
