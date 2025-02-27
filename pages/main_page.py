import os
import h5py

from PyQt6.QtGui import QIcon
from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from collections import defaultdict
from data_processing.data_loader import load_data_from_h5, sort_key
from widgets.main_window.video_tabs_widget import VideoTabsWidget
from widgets.main_window.wave_widget import load_data_generators, WaveformPlotter

from ui_compiled.main_window import Ui_ArcNeuroViz

from pages.import_settings_page import ImportSettingsWindow
from pages.rhd2avzproject_page import Rhd2AVZ
from pages.import_from_folder_page import ImportFromFolder

from widgets.main_window.VTK_model_viewer import VTKModelViewer


class MainWindow(QMainWindow, Ui_ArcNeuroViz):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        self.video_tabs_widget = None
        self.waveform_widget = None
        self.waveform_container = None
        self.vtk_viewer = None
        self.model_window = None

        self.setupUi(self)

        # 初始化模型
        self.model = QtGui.QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["no working dir set:"])
        self.treeView.setModel(self.model)

        # 初始化时创建抽象的结构
        self.initialize_abstract_tree_structure()

        self.settings_window = None
        self.rhd2avz_window = None
        self.import_from_folder_window = None

        self.actionAbout = None
        self.actionExit = None
        self.actionOpen = None
        self.actionOpenFromFolder = None
        self.actionSave = None

        self.working_dir = None
        self.setWindowIcon(QIcon('assets\\mainIcon.png'))
        self.init_actions()

        # 设置窗口样式表
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
        """)
        self.setFixedSize(1325, 720)
        self.initialize_vtk_viewer()
        self.initialize_waveform_plot()
        self.initialize_video_tabs_widget()

    def initialize_video_tabs_widget(self):
        """初始化视频标签小部件"""
        # 实例化 VideoTabsWidget
        self.video_tabs_widget = VideoTabsWidget(self)

        # 设置位置和大小
        self.video_tabs_widget.setGeometry(1020, -5, 300, 200)

        # 调用初始化方法
        self.video_tabs_widget.initialize(["../../2024-07-21 23-02-52.mp4", "../../2024-08-20 09-10-03.mp4"])
        self.video_tabs_widget.play_all_videos()

    def initialize_waveform_plot(self):
        """初始化波形图"""
        # 创建一个新的 QWidget 作为波形图容器
        self.waveform_container = QWidget(self)

        # 指定波形图容器的位置和大小（例如在窗口的右侧）
        self.waveform_container.setGeometry(310, 30, 705, 680)  # (x, y, width, height)
        self.waveform_container.setStyleSheet("background-color: #1e1e1e;")

        # 创建一个垂直布局并将其添加到波形图容器
        waveform_layout = QVBoxLayout(self.waveform_container)
        waveform_layout.setContentsMargins(0, 0, 0, 0)

        # 加载数据生成器
        data_generators = load_data_generators()

        # 创建波形图对象，并添加到波形图容器的布局中
        self.waveform_widget = WaveformPlotter(data_generators)
        waveform_layout.addWidget(self.waveform_widget)

    def initialize_vtk_viewer(self):
        """初始化 VTK 模型查看器"""
        self.vtk_viewer = VTKModelViewer(self.BrainWidget)
        self.vtk_viewer.initialize()

    def initialize_abstract_tree_structure(self):
        """初始化树结构"""
        port_a_item = QtGui.QStandardItem("Port example")
        hardware_item = QtGui.QStandardItem("Hardware example")
        channel_item = QtGui.QStandardItem("Channel example")

        hardware_item.appendRow(channel_item)
        port_a_item.appendRow(hardware_item)
        self.model.appendRow(port_a_item)

        self.treeView.expandAll()

    def init_actions(self):
        """初始化菜单栏动作"""
        self.actionOpen = QtGui.QAction("Import data from Raw Data(slow)", self)
        self.actionOpenFromFolder = QtGui.QAction("Import data from ANZ project(fast)", self)
        self.actionSave = QtGui.QAction("Save data to ANZ project", self)

        self.actionExit = QtGui.QAction("Exit", self)
        self.actionAbout = QtGui.QAction("About", self)

        # 绑定动作到菜单栏
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionOpenFromFolder)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionExit)

        self.menuHelp.addAction(self.actionAbout)

        # 绑定动作到槽函数
        # noinspection PyUnresolvedReferences
        self.actionOpen.triggered.connect(self.open_settings_window)  # 打开导入窗口
        # noinspection PyUnresolvedReferences
        self.actionOpenFromFolder.triggered.connect(self.open_from_folder_window)
        # noinspection PyUnresolvedReferences
        self.actionSave.triggered.connect(self.open_rhd2avz_window)  # 打开导入窗口
        # noinspection PyUnresolvedReferences
        self.actionExit.triggered.connect(self.close)  # 点击Exit退出应用

    def open_from_folder_window(self):
        """打开设置窗口"""
        if not self.import_from_folder_window:
            print("Opening from_folder_window window...")
            self.import_from_folder_window = ImportFromFolder()
            self.import_from_folder_window.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)  # 设置模态窗口
            self.import_from_folder_window.mainWindow = self
        self.import_from_folder_window.show()
        self.import_from_folder_window.set_output_log()

    def open_settings_window(self):
        """打开设置窗口"""
        if not self.settings_window:
            print("Opening settings window...")
            self.settings_window = ImportSettingsWindow()
            self.settings_window.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)  # 设置模态窗口
            self.settings_window.mainWindow = self
        self.settings_window.show()
        self.settings_window.set_output_log()

    def open_rhd2avz_window(self):
        if not self.rhd2avz_window:
            print("Opening .rhd to avz window...")
            self.rhd2avz_window = Rhd2AVZ()
            self.rhd2avz_window.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)  # 设置模态窗口
            self.rhd2avz_window.mainWindow = self
        self.rhd2avz_window.show()
        self.rhd2avz_window.set_output_log()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """窗口关闭事件"""
        # 确保窗口正常关闭
        # 如果有的话关闭其余打开的窗口
        if self.settings_window:
            self.settings_window.close()
        if self.rhd2avz_window:
            self.rhd2avz_window.close()
        if self.import_from_folder_window:
            self.import_from_folder_window.close()
        if self.model_window:
            self.model_window.close()
        event.accept()

    def check_working_dir(self):
        """检查工作目录配置文件是否存在"""
        if self.working_dir:
            self.model.setHorizontalHeaderLabels([f"{self.working_dir}"])
            working_dir_config_file = self.working_dir + '\\amplifier_channels.txt'
            if not os.path.exists(working_dir_config_file):
                print(f"Amplifier config file found at {working_dir_config_file}")
                port_channel_mapping = parse_amplifier_channels(self.working_dir)
                rename_amplifier_files(self.working_dir, port_channel_mapping)
                self.populate_tree_view(port_channel_mapping)  # 调用 populate_tree_view 来填充树视图
            else:
                print(f"Amplifier config file found at {working_dir_config_file}")
                port_channel_mapping = parse_amplifier_channels(self.working_dir)
                rename_amplifier_files(self.working_dir, port_channel_mapping)
                self.populate_tree_view(port_channel_mapping)  # 调用 populate_tree_view 来填充树视图

    def populate_tree_view(self, port_channel_mapping):
        """
        Populate the QTreeView with the parsed amplifier channel information.
        :param port_channel_mapping: dict, the parsed amplifier channel mapping from parse_amplifier_channels.
        """
        # 清空当前模型的所有项
        self.model.clear()
        self.model.setHorizontalHeaderLabels([f"{self.working_dir}"])
        # 遍历端口和硬件的结构来填充树视图
        for port, hardware_data in port_channel_mapping.items():
            # 创建端口项
            port_item = QtGui.QStandardItem(f"电极:{port}")
            self.model.appendRow(port_item)

            # 创建一个字典来跟踪硬件节点
            hardware_items = {}

            # Channel编号从1开始刷新
            channel_counter = 1

            # 遍历硬件信息
            for _, board_stream, chip_channel in hardware_data:
                hardware_key = f"board_stream {board_stream + 1}"

                # 如果该硬件项已经存在，则获取它，否则创建新的硬件项
                if hardware_key not in hardware_items:
                    hardware_item = QtGui.QStandardItem(hardware_key)
                    hardware_items[hardware_key] = hardware_item
                    port_item.appendRow(hardware_item)
                else:
                    hardware_item = hardware_items[hardware_key]

                # 创建通道项，通道编号从1开始
                channel_item_text = f"Channel {channel_counter} (Chip {chip_channel + 1})"
                channel_item = QtGui.QStandardItem(channel_item_text)
                hardware_item.appendRow(channel_item)

                # 增加通道计数器
                channel_counter += 1

        # 展开所有项
        self.treeView.expandAll()


# 解析amplifier_channels.h5文件
def parse_amplifier_channels(working_dir):
    config_file = os.path.join(working_dir, 'amplifier_channels.h5')
    data_config = load_data_from_h5(config_file)
    data_config = sorted(data_config, key=sort_key)
    # 初始化数据结构
    port_hardware_channel_count = defaultdict(lambda: defaultdict(int))
    pcm = defaultdict(list)
    # 打印正在解析文件的消息
    print(f"Parsing {config_file}...")
    # 遍历每个通道的配置信息
    for idx, channel_info in enumerate(data_config):
        port_name = channel_info['port_name'].decode()  # 转换字节字符串为普通字符串
        board_stream = channel_info['board_stream']  # 获取硬件编号
        chip_channel = channel_info['chip_channel']  # 获取芯片通道号

        port_hardware_channel_count[port_name][board_stream] += 1
        # 将通道索引和芯片通道号一起存储
        pcm[port_name].append((idx + 1, board_stream, chip_channel))
    # 输出统计结果
    for port, hardware_dict in port_hardware_channel_count.items():
        print(f"Port {port}:")
        for hardware, channel_count in hardware_dict.items():
            print(f"  Hardware {hardware}: {channel_count} channels")
            pass
    return pcm


def rename_amplifier_files(working_dir, port_channel_mapping):
    processed_data_dir = os.path.join(working_dir, 'processed_amplifier_data')

    if not os.path.exists(processed_data_dir):
        # print(f"Processed data directory {processed_data_dir} does not exist.")
        return

    for port, channel_data in port_channel_mapping.items():
        for i, (channel_idx, board_stream, chip_channel) in enumerate(channel_data):
            old_filename = f'amplifier_channel{channel_idx}.h5'
            new_filename = f'{port}_channel{i + 1}_board_stream{board_stream+1}_chip{chip_channel+1}.h5'
            old_filepath = os.path.join(processed_data_dir, old_filename)
            new_filepath = os.path.join(processed_data_dir, new_filename)

            if os.path.exists(old_filepath):
                os.rename(old_filepath, new_filepath)
                # print(f"Renamed {old_filename} to {new_filename}")
            else:
                # print(f"{old_filename} does not exist, skipping.")
                pass


if __name__ == "__main__":
    # port_channel_mapping = parse_amplifier_channels('D:\\Dev\\LNZN\\test_ANV_project')
    # rename_amplifier_files('D:\\Dev\\LNZN\\test_ANV_project', port_channel_mapping)
    with h5py.File("D:\Dev\LNZN\\test_ANV_project\processed_amplifier_data"
                   "\Port A_channel1_board_stream1_chip1.h5", 'r') as f:
        dataset = f['dataset_name'][:]
        print(dataset)
