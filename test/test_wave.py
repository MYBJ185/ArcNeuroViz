import sys
from PyQt6 import QtWidgets, QtCore
import pyqtgraph as pg
import numpy as np


def downsample(data, factor):
    original_points = np.arange(0, len(data))
    downsampled_points = np.arange(0, len(data), factor)
    downsampled_data = np.interp(downsampled_points, original_points, data)
    return downsampled_data


class WaveformPlotter(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建主窗口部件
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        # 创建布局
        self.layout = QtWidgets.QVBoxLayout(self.central_widget)

        # 创建pyqtgraph绘图窗口
        self.plot_widget = pg.GraphicsLayoutWidget()
        self.layout.addWidget(self.plot_widget)

        # 启用OpenGL以支持GPU加速
        pg.setConfigOptions(useOpenGL=True)
        pg.setConfigOptions(antialias=True)

        # 创建32个波形图
        self.num_waveforms = 32
        self.num_data_points = 30000
        self.downsample_rate = 5
        self.waveform_plots = []
        self.data = []

        self.create_waveforms()

        # 设置定时器用于更新数据
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_waveforms)
        self.timer.start(16)  # 每50ms更新一次

    def create_waveforms(self):
        for i in range(self.num_waveforms):
            # 模拟生成60000个数据点的波形数据
            waveform_data = np.random.normal(size=self.num_data_points)
            self.data.append(waveform_data)

            # 降采样到700个数据点
            downsampled_data = downsample(waveform_data, self.downsample_rate)

            # 为每个波形图创建一个PlotItem
            # noinspection PyUnresolvedReferences
            plot = self.plot_widget.addPlot()
            plot_item = plot.plot(downsampled_data, pen=pg.mkPen(color=(i * 8, 255, 255 - i * 8), width=1))
            self.waveform_plots.append(plot_item)

            # 设置波形图的基本属性
            plot.showAxis('left', False)
            plot.showAxis('bottom', False)
            plot.setMouseEnabled(x=False, y=False)

            # 增加一些间距以便显示多个波形图
            # noinspection PyUnresolvedReferences
            self.plot_widget.nextRow()

    def update_waveforms(self):
        for i in range(self.num_waveforms):
            # 模拟数据滚动：将数据向左滚动，并在右侧添加新的随机数据
            self.data[i] = np.roll(self.data[i], -1)
            self.data[i][-1] = np.random.normal()

            # 降采样
            downsampled_data = downsample(self.data[i], self.downsample_rate)

            # 更新波形图的数据
            self.waveform_plots[i].setData(downsampled_data)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = WaveformPlotter()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
