from PyQt6 import QtCore, QtMultimedia, QtMultimediaWidgets
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QApplication, QMainWindow


class VideoTabsWidget(QWidget):
    def __init__(self, parent=None):
        super(VideoTabsWidget, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 假设所有视频长度为10分钟（600000毫秒）
        self.assumed_duration = 600000

        # 创建 QTabWidget 用于在不同的标签页中显示不同的视频
        self.tabs = QTabWidget(self)
        self.layout.addWidget(self.tabs)

        # 创建两个 QVideoWidget 和 QMediaPlayer
        self.video_widgets = []
        self.media_players = []

        for i in range(2):  # 假设有两个标签页
            video_widget = QtMultimediaWidgets.QVideoWidget(self)
            video_widget.setFixedSize(277, 155)
            self.video_widgets.append(video_widget)

            media_player = QtMultimedia.QMediaPlayer(self)
            media_player.setVideoOutput(video_widget)
            media_player.durationChanged.connect(self.check_and_stop_at_end)
            self.media_players.append(media_player)

            self.tabs.addTab(video_widget, f"V{i + 1}")

        # 删除或注释掉与 QSlider 相关的代码
        # self.video_slider = QSlider(self)
        # self.video_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        # self.video_slider.setRange(0, self.assumed_duration)  # 设置时间轴范围为10分钟
        # self.layout.addWidget(self.video_slider)

        # 连接 QSlider 的滑动事件到所有的视频播放器
        # self.video_slider.sliderMoved.connect(self.set_position)

        # 每秒更新一次进度条
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_slider)
        self.timer.start(1000)

    def initialize(self, video_paths):
        """初始化方法，并为每个标签页指定不同的视频路径"""
        for i, path in enumerate(video_paths):
            url = QtCore.QUrl.fromLocalFile(path)
            self.media_players[i].setSource(url)

    def play_all_videos(self):
        """播放所有标签页的视频"""
        for player in self.media_players:
            player.play()

    def pause_all_videos(self):
        """暂停所有标签页的视频"""
        for player in self.media_players:
            player.pause()

    def set_position(self, position):
        """设置所有标签页的视频播放位置"""
        for player in self.media_players:
            player.setPosition(position)

    def update_slider(self):
        """同步更新滑块位置"""
        # 去掉滑块更新部分
        # if not self.video_slider.isSliderDown():
        #     # 使用第一个播放器的进度更新滑块
        #     current_position = self.media_players[0].position()
        #     self.video_slider.setValue(current_position)
        pass

    def check_and_stop_at_end(self, duration):
        """检查视频时长并在播放结束时停止"""
        if duration < self.assumed_duration:
            for player in self.media_players:
                if player.position() >= duration:
                    player.pause()


class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('VideoTabsWidget Test')
        self.setGeometry(100, 100, 800, 600)

        # 创建 VideoTabsWidget 实例
        self.video_tabs_widget = VideoTabsWidget(self)
        self.setCentralWidget(self.video_tabs_widget)

        # 初始化 VideoTabsWidget 并指定不同的视频路径
        video_paths = [
            "../../2024-07-21 23-02-52.mp4",  # 替换为实际的视频路径
            "../../2024-08-20 09-10-03.mp4"   # 替换为实际的视频路径
        ]
        self.video_tabs_widget.initialize(video_paths)

        # 播放所有视频
        self.video_tabs_widget.play_all_videos()

        # 在 5 秒后暂停所有视频
        # QTimer.singleShot(5000, self.pause_videos)

    def pause_videos(self):
        """测试暂停所有视频"""
        self.video_tabs_widget.pause_all_videos()
        print("所有视频已暂停")


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())
