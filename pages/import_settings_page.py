from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow
from ui_compiled.import_settings import Ui_import_settings


class ImportSettingsWindow(QMainWindow, Ui_import_settings):
    def __init__(self) -> None:
        super(ImportSettingsWindow, self).__init__()

        self.iren = None
        self.setWindowIcon(QIcon('icon_512.png'))
        # 设置窗口样式表
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
        """)
        self.setupUi(self)
        self.setWindowTitle("ANV - Import Settings")
        self.setFixedSize(372, 128)
