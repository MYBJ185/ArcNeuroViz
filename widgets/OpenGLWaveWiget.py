from PyQt6 import QtOpenGLWidgets, QtGui, QtCore
from OpenGL.GL import *
import numpy as np


def setup_opengl():
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


def create_character_texture(character_data, width, height):

    # 将字符数据转换为OpenGL纹理
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RED, width, height, 0, GL_RED, GL_UNSIGNED_BYTE, character_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glBindTexture(GL_TEXTURE_2D, 0)

    er = glGetError()
    if er != GL_NO_ERROR:
        print(f"OpenGL error: {er}")

    return texture_id


class CustomOpenGLWidget(QtOpenGLWidgets.QOpenGLWidget):
    def __init__(self, parent=None):
        super(CustomOpenGLWidget, self).__init__(parent)
        self.gl_context = None
        self.textures = {}
        self.texture_width = 8  # 每个字符的宽度
        self.texture_height = 11  # 每个字符的高度
        self.background_width = 100  # 背景的宽度
        self.background_height = 13  # 背景的高度

    def initializeGL(self):
        # 设置背景颜色 (RGBA)
        glClearColor(0.1, 0.1, 0.1, 1.0)
        # 创建一个独立的OpenGL上下文
        self.gl_context = QtGui.QOpenGLContext()
        self.gl_context.setShareContext(self.context())
        self.gl_context.create()
        self.gl_context.makeCurrent(self.context().surface())

        # OpenGL初始化
        setup_opengl()

        # 定义每个字符的像素图案 (8x11)
        characters = {
            'A': np.array([
                0, 0, 0, 1, 0, 0, 0, 0,
                0, 0, 0, 1, 0, 0, 0, 0,
                0, 0, 0, 1, 1, 0, 0, 0,
                0, 0, 1, 0, 1, 0, 0, 0,
                0, 0, 1, 0, 1, 0, 0, 0,
                0, 0, 1, 0, 0, 1, 0, 0,
                0, 0, 1, 1, 1, 1, 0, 0,
                0, 1, 0, 0, 0, 1, 0, 0,
                0, 1, 0, 0, 0, 0, 1, 0,
                0, 1, 0, 0, 0, 0, 1, 0,
                1, 1, 1, 0, 0, 1, 1, 1
            ], dtype=np.uint8) * 255,

            '-': np.array([
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                1, 1, 1, 1, 1, 1, 1, 1,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0
            ], dtype=np.uint8) * 255,

            '0': np.array([
                0, 0, 0, 1, 1, 0, 0, 0,
                0, 0, 1, 0, 0, 1, 0, 0,
                0, 1, 0, 0, 0, 0, 1, 0,
                0, 1, 0, 0, 0, 0, 1, 0,
                0, 1, 0, 0, 0, 0, 1, 0,
                0, 1, 0, 0, 0, 0, 1, 0,
                0, 1, 0, 0, 0, 0, 1, 0,
                0, 1, 0, 0, 0, 0, 1, 0,
                0, 1, 0, 0, 0, 0, 1, 0,
                0, 0, 1, 0, 0, 1, 0, 0,
                0, 0, 0, 1, 1, 0, 0, 0
            ], dtype=np.uint8) * 255
        }

        # 为每个字符创建纹理
        for char, pattern in characters.items():
            pattern = np.flipud(pattern)
            self.textures[char] = create_character_texture(pattern, self.texture_width, self.texture_height)

    def resizeGL(self, w, h):
        # 设置视口大小
        glViewport(0, 0, w, h)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glEnable(GL_TEXTURE_2D)  # 确保启用2D纹理

        # 绘制模板（包括背景和字符）
        self.draw_template(5, 5, (0, 0, 0, 1), (1, 1, 1, 1))  # 黑色背景，红色字符

        glDisable(GL_TEXTURE_2D)  # 结束绘制后关闭2D纹理

    def draw_template(self, start_x, start_y, background_color, text_color):
        """绘制整个模板，包含背景和字符"""
        self.draw_background(start_x, start_y, background_color)
        self.draw_text("A-000", start_x, start_y, text_color)

    def draw_background(self, start_x, start_y, background_color):
        """绘制背景"""
        glColor4f(*background_color)  # 背景颜色
        glBegin(GL_QUADS)
        # 计算标准化设备坐标 (NDC)
        window_width = self.width()
        window_height = self.height()
        ndc_x = (2 * start_x / window_width) - 1
        ndc_y = 1 - (2 * start_y / window_height)
        ndc_w = self.background_width / window_width * 2
        ndc_h = self.background_height / window_height * 2

        glVertex2f(ndc_x, ndc_y - ndc_h)  # 左下角
        glVertex2f(ndc_x + ndc_w, ndc_y - ndc_h)  # 右下角
        glVertex2f(ndc_x + ndc_w, ndc_y)  # 右上角
        glVertex2f(ndc_x, ndc_y)  # 左上角
        glEnd()

    def draw_text(self, text, start_x, start_y, text_color):
        """在屏幕上绘制文本"""
        glColor4f(*text_color)  # 设置字符颜色
        for i, char in enumerate(text):
            if char in self.textures:
                char_x = start_x + 60 + i * self.texture_width  # 字符起始X位置，字体从60开始
                char_y = start_y + (self.background_height - self.texture_height) // 2  # 上下居中
                self.draw_character_texture(self.textures[char], char_x, char_y)

    def draw_character_texture(self, texture_id, pixel_x, pixel_y):
        """在屏幕上绘制单个字符纹理"""
        if texture_id:
            glBindTexture(GL_TEXTURE_2D, texture_id)

            # 假设窗口宽度和高度
            window_width = self.width()
            window_height = self.height()

            # 计算标准化设备坐标 (NDC)
            ndc_x = (2 * pixel_x / window_width) - 1
            ndc_y = 1 - (2 * pixel_y / window_height)

            # 计算纹理的NDC宽度和高度
            texture_ndc_width = self.texture_width / window_width * 2
            texture_ndc_height = self.texture_height / window_height * 2

            # 设置纹理坐标和顶点坐标以绘制纹理
            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 0.0)
            glVertex2f(ndc_x, ndc_y - texture_ndc_height)  # 左下角
            glTexCoord2f(1.0, 0.0)
            glVertex2f(ndc_x + texture_ndc_width, ndc_y - texture_ndc_height)  # 右下角
            glTexCoord2f(1.0, 1.0)
            glVertex2f(ndc_x + texture_ndc_width, ndc_y)  # 右上角
            glTexCoord2f(0.0, 1.0)
            glVertex2f(ndc_x, ndc_y)  # 左上角
            glEnd()

            glBindTexture(GL_TEXTURE_2D, 0)

    def set_rounded_corners(self, radius):
        # 使用QPainterPath创建圆角路径
        path = QtGui.QPainterPath()
        rect = QtCore.QRectF(self.rect())
        path.addRoundedRect(rect, radius, radius)

        # 使用QRegion创建遮罩区域
        mask = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(mask)


# 使用示例
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    widget = CustomOpenGLWidget()
    widget.set_rounded_corners(5)
    widget.show()
    sys.exit(app.exec())
