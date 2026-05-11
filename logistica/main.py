# main.py

import os
import sys

# asegurar ruta del proyecto

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from menu.menu_principal import menu_principal

if __name__ == "__main__":
    menu_principal()
