import sys

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QFileDialog
from ui_compiled.import_settings import Ui_import_settings
from data_processing.data_loader import RHDDataLoader  # 假设你已经实现了 RHDDataLoader 类


class QTextEditLogger:
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def write(self, message):
        # 去除 message 末尾的多余换行符，并在追加到 text_edit 中时使用 `strip` 方法去除空行
        if message.strip():  # 只在 message 有内容时追加
            self.text_edit.append(message.rstrip())

    def flush(self):
        # 清空文本区域
        self.text_edit.clear()


class ImportSettingsWindow(QMainWindow, Ui_import_settings):
    def __init__(self) -> None:
        super(ImportSettingsWindow, self).__init__()

        self.original_stdout = None
        self.log_output = None
        self.data_loader = RHDDataLoader()  # 初始化 RHDDataLoader 实例
        self.data_loader_thread = None
        self.setWindowIcon(QIcon('icon_512.png'))
        # 设置窗口样式表
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
        """)
        self.setupUi(self)
        self.setWindowTitle("ANV - Import data file")
        self.setFixedSize(372, 272)
        # 设置下拉菜单选项
        self.setup_comboboxes()

        # 连接按钮点击事件
        self.pushButton_browse.clicked.connect(self.open_file_dialog)
        self.pushButton.clicked.connect(self.start_data_loading)
        self.pushButton_2.clicked.connect(self.close)

        self.set_output_log()

    def set_output_log(self):
        """重定向标准输出流"""
        self.original_stdout = sys.stdout
        self.log_output = QTextEditLogger(self.textEdit_log)
        sys.stdout = self.log_output

    def setup_comboboxes(self):
        """设置下拉菜单选项"""
        self.comboBox_2.addItem(".rhd")  # 提供.rhd文件类型
        self.comboBox.addItems(["Auto Detect", "10kHz", "20kHz", "30kHz"])  # 提供三种采样率选择以及自动识别

    def open_file_dialog(self):
        # 打开文件选择对话框
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Data File", "", "RHD Files (*.rhd)")
        if file_path:
            self.lineEdit_path.setText(file_path)

    def load_data(self):
        # 从文本框获取文件路径并加载数据
        file_path = self.lineEdit_path.text()
        if file_path:
            self.log_message("Loading data form file...")
            self.data_loader.load_rhd_data(file_path)
            # self.log_message(f"Data loaded from {file_path}")
            selected_datatype = self.comboBox_2.currentText()
            selected_samplerate = self.comboBox.currentText()
            # self.log_message(f"Processing data from {file_path} with {selected_datatype} at {
            # selected_samplerate}...\n")

            # 禁用控件
            self.pushButton.setEnabled(False)
            self.pushButton_browse.setEnabled(False)
            self.comboBox.setEnabled(False)
            self.comboBox_2.setEnabled(False)
        else:
            self.log_message("No file selected.")

    def start_data_loading(self):
        # 获取文件路径和其他选项
        file_path = self.lineEdit_path.text()
        selected_samplerate = self.comboBox.currentText()

        if file_path:
            # 禁用控件
            self.pushButton.setEnabled(False)
            self.pushButton_browse.setEnabled(False)
            self.comboBox.setEnabled(False)
            self.comboBox_2.setEnabled(False)

            # 创建并启动数据加载线程，传递 data_loader 实例
            self.data_loader_thread = DataLoaderThread(self.data_loader, file_path, selected_samplerate)
            self.data_loader_thread.data_loaded.connect(self.on_data_loaded)
            self.data_loader_thread.start()
        else:
            self.log_message("No file selected.")

    def on_data_loaded(self, message):
        # 当数据加载完成后，重新启用控件并显示消息
        self.log_message(message)
        self.pushButton.setEnabled(True)
        self.pushButton_browse.setEnabled(True)
        self.comboBox.setEnabled(True)
        self.comboBox_2.setEnabled(True)

    def closeEvent(self, event) -> None:
        """窗口关闭事件，恢复标准输出流"""
        sys.stdout = self.original_stdout  # 恢复标准输出流
        event.accept()

    def log_message(self, message: str):
        self.textEdit_log.append(message)


class DataLoaderThread(QThread):
    # 创建信号用于在数据加载完成后通知主线程
    data_loaded = pyqtSignal(str)

    def __init__(self, data_loader, file_path: str, samplerate: str):
        super().__init__()
        self.data_loader = data_loader
        self.file_path = file_path
        self.samplerate = samplerate

    def run(self):
        # 在后台线程中执行耗时操作
        self.data_loader.load_rhd_data(self.file_path)

        # 数据加载完成后发送信号
        self.data_loaded.emit(f"Data loaded from {self.file_path} with sample rate {self.samplerate}")
