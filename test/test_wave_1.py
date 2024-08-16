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
        self.num_data_points = 4000
        self.downsample_rate = 1
        self.step_size = 1  # 每次移动3个坐标点
        self.waveform_plots = []
        self.data = []
        self.buffer_size = 10000  # 缓冲区大小
        self.random_buffer = np.random.normal(size=(self.num_waveforms, self.buffer_size)) * 5000
        self.buffer_index = 0

        self.create_waveforms()

        # 设置定时器用于更新数据
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_waveforms)
        self.timer.start(10)  # 每16ms更新一次

    def create_waveforms(self):
        for i in range(self.num_waveforms):
            # 初始生成300000个数据点的波形数据
            waveform_data = np.random.normal(size=self.num_data_points) * 5000
            self.data.append(waveform_data)

            # 降采样到3000个数据点
            downsampled_data = downsample(waveform_data, self.downsample_rate)

            # 为每个波形图创建一个PlotItem
            color = (i * 8, 255, 255 - i * 8)
            # noinspection PyUnresolvedReferences
            plot = self.plot_widget.addPlot()
            plot_item = plot.plot(downsampled_data, pen=pg.mkPen(color=color, width=1))
            self.waveform_plots.append(plot_item)

            # 在绘图区内显示标签
            text = f"A-{i + 1:03d}"
            text_item = pg.TextItem(text, color=color, anchor=(0, 0.5))
            plot.addItem(text_item)
            text_item.setPos(-120, 0)  # 设置标签位置，紧贴左侧

            # 关闭鼠标靠近时显示的 "A" 标签
            plot.hideButtons()

            # 固定坐标轴范围
            plot.setXRange(-120, 3000, padding=0)
            plot.setYRange(-20000, 20000, padding=0)
            plot.setLimits(xMin=-120, xMax=3000, yMin=-20000, yMax=20000)

            # 设置波形图的基本属性
            plot.showAxis('left', False)
            plot.showAxis('bottom', False)
            plot.setMouseEnabled(x=False, y=True)

            # 增加一些间距以便显示多个波形图
            # noinspection PyUnresolvedReferences
            self.plot_widget.nextRow()

    def update_waveforms(self):
        for i in range(self.num_waveforms):
            # 使用缓冲区中的随机数据进行更新
            self.data[i] = np.roll(self.data[i], -self.step_size)
            if self.buffer_index + self.step_size < self.buffer_size:
                self.data[i][-self.step_size:] = self.random_buffer[
                                                 i,
                                                 self.buffer_index:self.buffer_index + self.step_size]
            else:
                # 如果缓冲区耗尽，重新生成缓冲区
                self.random_buffer = np.random.normal(size=(self.num_waveforms, self.buffer_size)) * 5000
                self.buffer_index = 0
                self.data[i][-self.step_size:] = self.random_buffer[
                                                 i,
                                                 self.buffer_index:self.buffer_index + self.step_size]

        self.buffer_index += self.step_size

        # 降采样
        for i in range(self.num_waveforms):
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
