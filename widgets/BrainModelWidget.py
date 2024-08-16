import os
import numpy as np
from OpenGL.raw.GLU import gluLookAt
from PyQt6.QtCore import QTimer
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective
import pywavefront


def calculate_normals(vertices, faces):
    normals = np.zeros((len(vertices), 3), dtype=np.float32)
    for face in faces:
        v1, v2, v3 = [vertices[i] for i in face]
        normal = np.cross(np.array(v2) - np.array(v1), np.array(v3) - np.array(v1))
        norm = np.linalg.norm(normal)
        if norm != 0:
            normal = normal / norm  # 归一化法线
        for i in face:
            normals[i] += normal
    normals = np.array([n / np.linalg.norm(n) if np.linalg.norm(n) != 0 else n for n in normals])
    return normals


class BrainModelWidget(QOpenGLWidget):
    def __init__(self, folder_path, parent=None):
        super(BrainModelWidget, self).__init__(parent)
        self.folder_path = folder_path
        self.scenes = []  # 存储每个模型的场景数据
        self.normals = []  # 存储每个模型的法线数据
        self.rotation_angle = 0  # 初始化旋转角度

        # 设置一个计时器来更新旋转角度
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_rotation)
        self.timer.start(16)  # 大约60帧每秒 (1000ms / 60 ≈ 16ms)

    def initializeGL(self):
        print("OpenGL version:", glGetString(GL_VERSION).decode("utf-8"))
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_NORMALIZE)
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)

        # 设置背景色
        glClearColor(0.1, 0.1, 0.1, 1.0)

        # 遍历文件夹中的所有.obj文件
        for filename in os.listdir(self.folder_path):
            if filename.endswith(".obj"):
                obj_file_path = os.path.join(self.folder_path, filename)
                try:
                    scene = pywavefront.Wavefront(obj_file_path, collect_faces=True)
                    print(f"Loaded {filename} with {len(scene.vertices)} vertices.")
                    vertices = np.array(scene.vertices)
                    faces = [face for mesh in scene.mesh_list for face in mesh.faces]
                    normals = calculate_normals(vertices, faces)
                    self.scenes.append(scene)
                    self.normals.append(normals)
                except Exception as e:
                    print(f"Failed to load {filename}: {e}")

        # 设置光源的位置和颜色
        glLightfv(GL_LIGHT0, GL_POSITION, [0, 0, 10, 1])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])

        # 设置材质属性
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.3, 0.3, 0.3, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.8, 0.5, 0.3, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 50.0)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect_ratio = w / h if h > 0 else 1
        gluPerspective(45, aspect_ratio, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

        glScalef(0.01, 0.01, 0.01)
        glRotatef(self.rotation_angle, 0, 1, 0)

        try:
            for scene, normals in zip(self.scenes, self.normals):
                glBegin(GL_TRIANGLES)
                for mesh in scene.mesh_list:
                    for face in mesh.faces:
                        for vertex_index in face:
                            glNormal3fv(normals[vertex_index])
                            glVertex3fv(scene.vertices[vertex_index])
                glEnd()
        except Exception as e:
            print(f"Error during rendering: {e}")

    def update_rotation(self):
        self.rotation_angle += 1
        if self.rotation_angle >= 360:
            self.rotation_angle = 0
        self.update()
