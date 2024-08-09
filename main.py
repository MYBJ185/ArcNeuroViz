import sys
from PyQt6.QtWidgets import QApplication
from pages.main_page import MainWindow
from pages.import_settings_page import ImportSettingsWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImportSettingsWindow()
    window.show()
    sys.exit(app.exec())
