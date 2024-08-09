import sys
import os
from PyQt6.QtWidgets import QApplication
from pages.main_page import MainWindow
from pages.import_settings_page import ImportSettingsWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # anotherWindow = ImportSettingsWindow()
    # anotherWindow.show()
    sys.exit(app.exec())
