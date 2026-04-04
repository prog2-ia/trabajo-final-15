# main.py

import sys
import os

# asegurar ruta del proyecto
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from menu.menu_principal import menu_principal

if __name__ == "__main__":
    menu_principal()
