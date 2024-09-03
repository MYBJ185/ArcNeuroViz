import sys
import h5py
from vispy import app, scene
from vispy.scene import visuals
import numpy as np
import colorsys
from PyQt6.QtWidgets import QApplication, QMainWindow, QScrollBar, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt


class WaveformPlotter(QMainWindow):
    def __init__(self, data_generators, num_points=60000, step_size=30):
        super().__init__()
        self.canvas = scene.SceneCanvas(keys='interactive', size=(1000, 600), show=True)
        self.num_waveforms = len(data_generators)
        self.data_generators = data_generators
        self.num_points = num_points
        self.step_size = step_size
        self.data_cache = [np.zeros(self.num_points) for _ in range(self.num_waveforms)]
        self.view_height = 600  # 视图窗口高度，像素值

        # 创建ViewBox并设置自定义摄像机
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = scene.cameras.PanZoomCamera(rect=(0, -8 * 10000, self.num_points, 80000))
        self.view.camera.set_range(x=(0, num_points), y=(-8 * 10000, 0))
        self.view.camera.interactive = True  # 启用交互以支持缩放

        self.lines = []

        for i in range(self.num_waveforms):
            hue = i / self.num_waveforms
            rgb = colorsys.hsv_to_rgb(hue, 1.0, 0.75)
            color = tuple(c for c in rgb)

            # 绘制波形线条
            line = visuals.Line(color=color, method='gl', width=1)
            self.lines.append(line)
            self.view.add(line)

            # 创建文本标签和背景矩形
            text_pos = (-40, -i * 10000)
            rect_pos = (-40, -i * 10000)
            rect = visuals.Rectangle(center=rect_pos, width=80, height=20, color=color, parent=self.view.scene)
            rect.transform = scene.STTransform(scale=(1, 1))  # 固定矩形大小
            text = visuals.Text(f"A-{i:03d}", color='white', pos=text_pos,
                                font_size=6, anchor_x='left', anchor_y='center', parent=self.view.scene)
            text.transform = scene.STTransform(scale=(1, 1))  # 固定文本大小

            self.view.add(rect)
            self.view.add(text)

        # 创建滚动条
        self.scroll_bar = QScrollBar(Qt.Orientation.Vertical)
        self.scroll_bar.setRange(0, 80000)
        self.scroll_bar.setValue(0)
        self.update_scroll_bar()
        self.scroll_bar.valueChanged.connect(self.on_scroll)

        # 创建布局并添加到窗口
        layout = QHBoxLayout()
        layout.addWidget(self.canvas.native)
        layout.addWidget(self.scroll_bar)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 设置窗口标题和大小
        self.setWindowTitle("Waveform Plotter")
        self.resize(1200, 600)

        # 将 keyPressEvent 添加到 SceneCanvas 的 native 对象
        self.canvas.native.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.canvas.native.keyPressEvent = self.keyPressEvent

        # 启动定时器更新波形
        self.timer = app.Timer(interval=0.01, connect=self.update_waveforms, start=True)
        self.show()

    def update_waveforms(self, event):
        for i, gen in enumerate(self.data_generators):
            self.data_cache[i] = np.roll(self.data_cache[i], -self.step_size)

            try:
                new_data = next(gen)
                if len(new_data) < self.step_size:
                    continue
                self.data_cache[i][-self.step_size:] = new_data[:self.step_size]
            except StopIteration:
                continue

            x = np.arange(self.num_points)
            y_offset = -i * 10000
            self.lines[i].set_data(pos=np.column_stack((x, self.data_cache[i] + y_offset)))

        self.canvas.update()

    def on_scroll(self, value):
        y_offset = -value
        # 根据滚动条的值移动相机
        self.view.camera.set_range(y=(y_offset - self.view.camera.rect.height, y_offset))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Space:
            # 切换定时器状态
            if self.timer.running:
                self.timer.stop()
            else:
                self.timer.start()
        else:
            super().keyPressEvent(event)

    def update_scroll_bar(self):
        # 计算滚动条滑块长度，使其适应视图窗口大小
        content_height = 80000
        page_size = int((self.view_height / content_height) * content_height)
        self.scroll_bar.setPageStep(page_size)
        self.scroll_bar.setSingleStep(1000)

    def wheelEvent(self, event):
        # Y轴缩放
        delta = event.angleDelta().y()
        if delta != 0:
            scale_factor = 1.1 if delta > 0 else 0.9
            self.view.camera.zoom((1.0, scale_factor))
        super().wheelEvent(event)


def load_data_generators():
    generators = []
    base_path = "D:/Dev/LNZN/test_ANV_project/processed_amplifier_data/"
    for i in range(1, 33):
        file_name = f"Port A_channel{i}_board_stream1_chip{i}.h5"
        file_path = base_path + file_name
        f = h5py.File(file_path, 'r')
        dataset = f['dataset_name']

        def data_generator(ds):
            start = 0
            while start + 30000 <= len(ds):
                while start + 30000 <= len(ds):
                    yield ds[start:start + 30000]
                    start += 30000
                if start < len(ds):
                    yield ds[start:]
                start = 0

        generators.append(data_generator(dataset))
    return generators


def main():
    app_qt = QApplication(sys.argv)
    data_generators = load_data_generators()
    wave_plotter = WaveformPlotter(data_generators)
    sys.exit(app_qt.exec())


if __name__ == "__main__":
    main()
