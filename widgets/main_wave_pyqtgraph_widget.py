import time
import pyqtgraph as pg
import numpy as np
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QSizePolicy


class WaveformWidget(QWidget):
    def __init__(self, parent=None):
        super(WaveformWidget, self).__init__(parent)
        self.scan_position = None
        self.time_duration = 2000  # 时间轴的最大值（2000ms）
        self.start_time = time.time()  # 记录起始时间
        self.update_speed = 10  # 更新扫描线的时间单位（ms）
        self.setStyleSheet("background-color: #000000;")

        # 创建时间轴
        self.time_axis_widget = pg.PlotWidget()
        self.time_axis_widget.setFixedHeight(50)
        self.time_axis_widget.setYRange(-1, 1)  # 设置Y轴范围，以确保时间轴是平的
        self.time_axis_widget.setXRange(0, self.time_duration)  # 设置X轴范围
        self.time_axis_widget.setMouseEnabled(x=False, y=False)
        self.time_axis_widget.showAxis('left', False)  # 隐藏左侧轴

        # 显示顶部轴
        self.time_axis_widget.showAxis('top', True)
        top_axis = self.time_axis_widget.getAxis('top')
        top_axis.setTicks([[(0, '0 ms'), (2000, '2000 ms')]])  # 自定义刻度
        top_axis.setZValue(1)  # 确保轴在线条上方显示

        # 隐藏底部轴
        self.time_axis_widget.showAxis('bottom', False)

        self.time_axis_widget.getPlotItem().getViewBox().setBackgroundColor('k')  # 设置背景色为黑色

        # 绘制不可见的辅助线
        self.time_axis_widget.plot([0, self.time_duration], [0, 0], pen=pg.mkPen((0, 0, 0, 0), width=0))

        # 添加扫描线到时间轴
        self.time_axis_scan_line = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('r', width=2))
        self.time_axis_widget.addItem(self.time_axis_scan_line)

        # 创建一个滚动区域
        scroll_area = QScrollArea(self)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # 禁用水平滚动条

        # 创建一个大波形图
        large_plot_widget = pg.PlotWidget()
        large_plot_widget.setFixedHeight(1600)  # 设置大图的高度，根据需要调整
        large_plot_widget.setXRange(0, self.time_duration)  # 设置X轴范围，确保与时间轴一致
        large_plot_widget.setFixedWidth(670 + 35)  # 设置大图的宽度

        # 隐藏坐标轴
        large_plot_widget.showAxis('left', False)  # 可以显示左侧轴，方便查看
        large_plot_widget.showAxis('bottom', False)

        # 禁用鼠标交互
        large_plot_widget.setMouseEnabled(x=False, y=False)

        # 绘制多条示例波形数据
        for i in range(32):  # 示例：32条曲线
            x = np.linspace(0, self.time_duration, 1000)
            y = 5000 * i * (x+1) / (x+1)
            large_plot_widget.plot(x, y)

        # 为大图添加扫描线
        large_scan_line = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('r', width=2))
        large_plot_widget.addItem(large_scan_line)
        self.scan_lines = [large_scan_line]  # 只有一个扫描线

        # 设置滚动区域的widget
        scroll_area.setWidget(large_plot_widget)
        scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        scroll_area.setWidgetResizable(False)  # 防止自动调整大小

        # 创建主布局，将时间轴和滚动区域分开
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)  # 设置时间轴和波形图之间的间距为0
        main_layout.setContentsMargins(0, 0, 0, -30)  # 设置右边距为-30，以使时间轴延伸出 30 像素
        main_layout.addWidget(self.time_axis_widget)
        main_layout.addWidget(scroll_area)

        # 创建一个定时器，用于更新扫描线的位置
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_scan_line)
        self.timer.start(self.update_speed)  # 每10ms更新一次

    def update_scan_line(self):
        """更新扫描线的位置"""
        elapsed_time = (time.time() - self.start_time) * 1000  # 计算经过的时间（ms）
        self.scan_position = elapsed_time % self.time_duration  # 扫描线位置在[0, time_duration]之间循环

        # 更新时间轴上的扫描线位置
        self.time_axis_scan_line.setPos(self.scan_position)

        # 更新大图中的扫描线位置
        for scan_line in self.scan_lines:
            scan_line.setPos(self.scan_position)
