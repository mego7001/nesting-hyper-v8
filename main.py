# main.py

import sys
import os
import json

from PyQt6.QtWidgets import QApplication
from ui.components import MainWindow

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config', 'settings.json')


def load_settings(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    # Load configuration
    settings = load_settings(CONFIG_PATH)

    # Initialize application
    app = QApplication(sys.argv)
    window = MainWindow(settings)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
