import sys
import h5py
from PyQt6 import QtWidgets, QtCore
import pyqtgraph as pg
import numpy as np
import colorsys  # 用于HSV到RGB的转换
from PyQt6.QtWidgets import QGraphicsRectItem


class CustomViewBox(pg.ViewBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.menu = None
        self.autoBtn = None
        self.buttonsHidden = True

    def raiseContextMenu(self, ev):
        pass


class WaveformPlotter(QtWidgets.QMainWindow):
    def __init__(self, data_generators, num_points=10000, step_size=200):
        super().__init__()

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        # 创建一个水平布局
        self.horizontal_layout = QtWidgets.QHBoxLayout(self.central_widget)

        # 创建pyqtgraph绘图窗口
        self.plot_widget = pg.GraphicsLayoutWidget()
        self.horizontal_layout.addWidget(self.plot_widget)

        pg.setConfigOptions(useOpenGL=True)
        pg.setConfigOptions(antialias=True)

        self.num_waveforms = len(data_generators)
        self.data_generators = data_generators
        self.num_points = num_points  # 同屏显示的点数
        self.step_size = step_size
        self.phase_shift = 0
        self.waveform_plots = []
        self.plot = self.plot_widget.addPlot()

        self.y_range = 100000  # Y轴显示范围
        self.total_data_range = -10000 * (self.num_waveforms - 1)
        self.plot.setYRange(self.total_data_range, self.total_data_range + self.y_range)  # 初始化Y轴显示范围
        self.plot.setLimits(xMin=-2200, xMax=num_points, yMin=self.total_data_range - 10000, yMax=10000)
        self.plot.showAxis('left', True)
        self.plot.showAxis('bottom', True)

        self.plot.getAxis('left').setStyle(showValues=False)
        self.plot.getAxis('bottom').setStyle(showValues=False)
        self.plot.setMenuEnabled(False)
        self.plot.setMouseEnabled(x=False, y=True)
        self.plot.showGrid(x=True, y=True)

        view_box = self.plot.getViewBox()

        if hasattr(view_box, 'autoBtn'):
            view_box.autoBtn.hide()

        self.data_cache = [np.zeros(self.num_points) for _ in range(self.num_waveforms)]  # 初始化缓存

        self.create_waveforms()
        self.plot.hideButtons()

        # 添加滚动条
        self.scroll_bar = QtWidgets.QScrollBar(QtCore.Qt.Orientation.Vertical)
        self.scroll_bar.setRange(0, abs(self.total_data_range) + 20000 - self.y_range)
        self.scroll_bar.setPageStep(self.y_range)
        self.scroll_bar.valueChanged.connect(self.update_y_range)
        self.horizontal_layout.addWidget(self.scroll_bar)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_waveforms)
        self.timer.start(20)  # 每20ms更新一次，即50帧每秒

    def create_waveforms(self):
        for i in range(self.num_waveforms):
            # 使用HSV颜色模型生成彩虹色，并降低明度
            hue = i / self.num_waveforms  # 生成色调
            rgb = colorsys.hsv_to_rgb(hue, 1.0, 0.75)  # 转换为RGB, V值降低到0.5（即降低明度）
            color = tuple(int(c * 255) for c in rgb)  # 转换为0-255范围的整数值

            # 恢复连线但设置较细的线宽，以减少视觉上的影响
            plot_item = self.plot.plot(
                pen=pg.mkPen(color=color, width=0.5),  # 恢复连线，宽度为0.5
                symbol=None  # 禁用符号
            )
            plot_item.hoverEvent = lambda ev: None
            self.waveform_plots.append(plot_item)

            # 创建彩色矩形作为标签背景
            rect_item = QGraphicsRectItem(-50, -9, 55, 18)
            rect_item.setBrush(pg.mkBrush(color))
            rect_item.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIgnoresTransformations)  # 保持大小不变
            self.plot.addItem(rect_item)
            rect_item.setPos(-60, -i * 10000)  # 设置矩形的位置

            # 在矩形上添加白色的文本
            text = f"A-{i:03d}"
            text_item = pg.TextItem(text, color=(255, 255, 255), anchor=(1, 0.5))
            self.plot.addItem(text_item)
            text_item.setPos(-40, -i * 10000)  # 设置文本的位置

    def update_y_range(self, value):
        adjusted_value = -value + 10000
        self.plot.setYRange(adjusted_value - self.y_range, adjusted_value, padding=0)

    def update_waveforms(self):
        self.phase_shift += self.step_size
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

            self.waveform_plots[i].setData(x, self.data_cache[i] + y_offset)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Space:
            if self.timer.isActive():
                self.timer.stop()  # 暂停
            else:
                self.timer.start(16)  # 继续

        super().keyPressEvent(event)


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
    app = QtWidgets.QApplication(sys.argv)
    data_generators = load_data_generators()
    main_window = WaveformPlotter(data_generators)
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
