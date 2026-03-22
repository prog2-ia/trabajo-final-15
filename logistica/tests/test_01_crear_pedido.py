import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import utiles.utils as utils

if __name__ == "__main__":

    print("=== CREAR PEDIDO ===")

    utils.test_crear_pedido()
