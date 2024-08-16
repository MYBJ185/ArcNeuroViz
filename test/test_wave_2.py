import sys
from PyQt6 import QtWidgets, QtCore
import pyqtgraph as pg
import numpy as np


def dynamic_downsample(data, target_points):
    """
    根据目标点数对数据进行动态降采样。
    :param data: 原始数据
    :param target_points: 目标点数
    :return: 降采样后的数据
    """
    if len(data) <= target_points:
        return data
    factor = len(data) // target_points
    downsampled_data = downsample(data, factor)
    return downsampled_data


def downsample(data, factor):
    original_points = np.arange(0, len(data))
    downsampled_points = np.arange(0, len(data), factor)
    downsampled_data = np.interp(downsampled_points, original_points, data)
    return downsampled_data


class CustomViewBox(pg.ViewBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 重载初始化方法，不创建自动缩放按钮
        self.menu = None
        self.autoBtn = None
        self.buttonsHidden = True  # 不显示任何按钮

    def raiseContextMenu(self, ev):
        pass  # 禁用右键菜单


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

        # 创建一个PlotItem，绘制32个波形图
        self.num_waveforms = 32
        self.num_data_points = 3000  # 数据点数量
        self.target_points = 3000  # 显示范围内的目标点数
        self.step_size = 3  # 每次移动10个坐标点
        self.amplitude = 250  # 调整幅度
        self.sin_period = 750  # 正弦波周期
        self.sin_amplitude = 5500  # 正弦波幅度
        self.phase_shift = 0  # 相位偏移
        self.waveform_plots = []
        self.data = []
        self.plot = self.plot_widget.addPlot()

        # 配置PlotItem
        self.plot.setXRange(-120, 1000, padding=0)
        self.plot.setYRange(-5000 - 10000 * self.num_waveforms, 5000, padding=0)  # 设置Y轴范围
        self.plot.setLimits(xMin=-150, xMax=1000, yMin=-5000 - 10000 * self.num_waveforms, yMax=5000)
        self.plot.showAxis('left', True)
        self.plot.showAxis('bottom', True)

        # 隐藏 Y 轴的刻度数字，但保留网格线
        self.plot.getAxis('left').setStyle(showValues=False)
        self.plot.getAxis('bottom').setStyle(showValues=False)
        self.plot.setMenuEnabled(False)
        self.plot.setMouseEnabled(x=False, y=True)
        self.plot.showGrid(x=True, y=True)

        # 禁用自动缩放按钮
        view_box = self.plot.getViewBox()

        # 访问并隐藏 autoBtn 按钮
        if hasattr(view_box, 'autoBtn'):
            view_box.autoBtn.hide()

        self.create_waveforms()
        self.plot.hideButtons()
        # 设置定时器用于更新数据
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_waveforms)
        self.timer.start(20)  # 每10ms更新一次

    def create_waveforms(self):
        for i in range(self.num_waveforms):
            # 初始生成20000个数据点的波形数据
            waveform_data = np.random.normal(size=self.num_data_points) * self.amplitude
            self.data.append(waveform_data)

            # 在波形图中为每个波形创建一个plot
            color = ((i * 16) % 255, (255 - i * 16) % 255, (255 - i * 16) % 255)
            plot_item = self.plot.plot(pen=pg.mkPen(color=color, width=1))
            plot_item.hoverEvent = lambda ev: None  # 取消鼠标悬停事件
            self.waveform_plots.append(plot_item)

            # 在左侧绘制对应的标签，从上往下递增
            text = f"A-{i:03d}"
            text_item = pg.TextItem(text, color=color, anchor=(1, 0.5))  # 右对齐，anchor的x值设置为1
            self.plot.addItem(text_item)
            text_item.setPos(-10, -i * 10000)  # 将每个标签的位置设置为从 y=0 开始逐步向下偏移

    def update_waveforms(self):
        self.phase_shift += self.step_size  # 更新相位偏移，确保正弦波随数据流动
        for i in range(self.num_waveforms):
            # 使用缓冲区中的随机数据进行更新
            self.data[i] = np.roll(self.data[i], -self.step_size)
            self.data[i][-self.step_size:] = np.random.normal(size=self.step_size) * self.amplitude

            # 为每个数据点添加正弦波动，并且让相位随数据流动
            x = np.arange(len(self.data[i]))
            sin_offset = np.sin(2 * np.pi * (x + self.phase_shift) / self.sin_period) * self.sin_amplitude

            waveform_with_offset = self.data[i] + sin_offset

            # 计算 Y 轴偏移，将 A-000 放在 y=0，依次向下
            y_offset = -i * 10000

            # 将偏移应用到波形数据
            waveform_with_offset += y_offset

            # 动态降采样，确保在当前视图范围内显示目标点数
            downsampled_data = dynamic_downsample(waveform_with_offset, self.target_points)

            # 绘制带有 Y 轴偏移的波形数据
            self.waveform_plots[i].setData(downsampled_data)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_window = WaveformPlotter()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
