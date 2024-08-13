import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QFileDialog

from data_processing.data_loader import RHDDataLoader

from ui_compiled.import_from_folder import Ui_import_from_folder


class QTextEditLogger:
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def write(self, message):
        # 去除 message 末尾的多余换行符，并在追加到 text_edit 中时使用 `strip` 方法去除空行
        if message.strip():  # 只在 message 有内容时追加
            message = message.replace('\t', '\\t').replace('\n', '\\n').replace('\r', '\\r')
            self.text_edit.append(message.rstrip())

    def flush(self):
        # 清空文本区域
        # self.text_edit.clear()
        pass


class ImportFromFolder(QMainWindow, Ui_import_from_folder):
    def __init__(self) -> None:
        super(ImportFromFolder, self).__init__()
        self.mainWindow = None  # 添加一个属性来存储主窗口的实例
        self.original_stdout = None
        self.log_output = None
        self.data_loader = RHDDataLoader()  # 初始化 RHDDataLoader 实例
        self.data_loader_thread = None
        self.setWindowIcon(QIcon('mainIcon.png'))
        # 设置窗口样式表
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
        """)
        self.setupUi(self)
        self.setWindowTitle("ANV - Import data file")
        self.setFixedSize(372, 317)

        # 连接按钮点击事件
        self.pushButton_browse.clicked.connect(self.open_files_dialog)
        self.pushButton.clicked.connect(self.set_working_place)
        self.set_output_log()

    def set_output_log(self):
        """重定向标准输出流"""
        self.original_stdout = sys.stdout
        self.log_output = QTextEditLogger(self.textEdit_log)
        sys.stdout = self.log_output

    def open_files_dialog(self):
        # 打开文件夹选择对话框
        folder_path = QFileDialog.getExistingDirectory(self, "Select Data Directory", "")
        if folder_path:
            self.lineEdit_path.setText(folder_path)

    def closeEvent(self, event) -> None:
        """窗口关闭事件，恢复标准输出流"""
        sys.stdout = self.original_stdout  # 恢复标准输出流
        event.accept()

    def log_message(self, message: str):
        self.textEdit_log.append(message)

    def set_working_place(self):
        """设置工作目录"""
        if self.lineEdit_path.text():
            self.mainWindow.working_dir = self.lineEdit_path.text().replace("/", "\\")
            print(f"Working directory set to {self.data_loader.working_dir}")
        # 检查工作目录配置文件是否存在
        self.mainWindow.check_working_dir()
