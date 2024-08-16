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

        # 创建一个PlotItem，绘制4个波形图
        self.num_waveforms = 4
        self.num_data_points = 1000  # 数据点数量
        self.downsample_rate = 1
        self.step_size = 3  # 每次移动3个坐标点
        self.amplitude = 8  # 调整幅度，使得波形更加明显
        self.sin_period = 1000  # 调整周期，使得正弦波的变化更加明显
        self.waveform_plots = []
        self.data = []
        self.plot = self.plot_widget.addPlot()

        # 配置PlotItem
        self.plot.setXRange(-120, 1000, padding=0)
        self.plot.setYRange(-20000, 20000, padding=0)  # 保证所有波形都在视图中
        self.plot.setLimits(xMin=-120, xMax=1000, yMin=-20000, yMax=20000)
        self.plot.showAxis('left', False)
        self.plot.showAxis('bottom', False)
        self.plot.setMouseEnabled(x=False, y=True)

        self.create_waveforms()

        # 设置定时器用于更新数据
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_waveforms)
        self.timer.start(33)  # 每33ms更新一次

    def create_waveforms(self):
        for i in range(self.num_waveforms):
            # 初始生成1000个数据点的波形数据
            waveform_data = np.random.normal(size=self.num_data_points) * self.amplitude
            self.data.append(waveform_data)

            # 在波形图中为每个波形创建一个plot
            color = (i * 8, 255, 255 - i * 8)
            plot_item = self.plot.plot(pen=pg.mkPen(color=color, width=1))
            self.waveform_plots.append(plot_item)

            # 在左侧绘制对应的标签，避免被波形线条覆盖
            text = f"A-{i + 1:03d}"
            text_item = pg.TextItem(text, color=color, anchor=(0, 0.5))
            self.plot.addItem(text_item)
            text_item.setPos(-120, (i - self.num_waveforms / 2) * 20000 / self.num_waveforms)

    def update_waveforms(self):
        for i in range(self.num_waveforms):
            # 使用缓冲区中的随机数据进行更新
            self.data[i] = np.roll(self.data[i], -self.step_size)
            self.data[i][-self.step_size:] = np.random.normal(size=self.step_size) * self.amplitude

            # 添加正弦波的偏移
            sin_offset = (np.sin(
                np.linspace(0, 2 * np.pi, self.num_data_points, endpoint=False) * (2 * np.pi / self.sin_period))
                          * self.amplitude * 0.5)

            waveform_with_offset = self.data[i] + sin_offset

            # 计算 Y 轴偏移
            y_offset = (i - self.num_waveforms / 2) * 20000 / self.num_waveforms

            # 将偏移应用到波形数据
            waveform_with_offset += y_offset

            # 暂时取消降采样，直接绘制波形数据
            downsampled_data = waveform_with_offset  # 不进行降采样，直接使用原始数据

            # 绘制带有 Y 轴偏移的波形数据
            self.waveform_plots[i].setData(downsampled_data)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = WaveformPlotter()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
