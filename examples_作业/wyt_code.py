#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author zhouhuawei time:2024/6/17
import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtCore import Qt

class ImageStitchingApp(QWidget):
    def __init__(self):
        super().__init__()

        self.image1 = None
        self.image2 = None

        self.initUI()

    def initUI(self):
        self.setWindowTitle('图像处理应用')
        self.setGeometry(100, 100, 800, 600)

        # 设置背景图片
        background = QPixmap("background.jpg")  # 替换为您的背景图片路径
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(background))
        self.setPalette(palette)

        # 创建布局
        layout = QVBoxLayout()

        # 小组成员信息
        members_label = QLabel('小组成员: 吴玉堂, 周华威, 王娜, 聂欣宇')
        members_label.setStyleSheet("color: red; font-size: 16px;")
        members_label.setAlignment(Qt.AlignCenter)

        # 图片上传和显示区域
        image_layout = QHBoxLayout()
        self.label1 = QLabel('原始图像1')
        self.label1.setFixedSize(200, 200)
        self.label1.setStyleSheet("background-color: white;")
        self.button1 = QPushButton('上传图像')
        self.button1.clicked.connect(self.loadImage1)

        self.label2 = QLabel('原始图像2')
        self.label2.setFixedSize(200, 200)
        self.label2.setStyleSheet("background-color: white;")
        self.button2 = QPushButton('上传图像')
        self.button2.clicked.connect(self.loadImage2)

        image_layout.addWidget(self.label1)
        image_layout.addWidget(self.button1)
        image_layout.addWidget(self.label2)
        image_layout.addWidget(self.button2)

        # 功能按钮区域
        button_layout = QHBoxLayout()
        self.stitchButton = QPushButton('图像拼接')
        self.stitchButton.clicked.connect(self.stitchImages)

        self.calibrateButton = QPushButton('摄像机标定')
        self.calibrateButton.clicked.connect(self.calibrateCamera)

        self.reconstructButton = QPushButton('单视图重构')
        self.reconstructButton.clicked.connect(self.reconstruct3D)

        button_layout.addWidget(self.stitchButton)
        button_layout.addWidget(self.calibrateButton)
        button_layout.addWidget(self.reconstructButton)

        # 结果显示区域布局
        result_layout = QGridLayout()
        self.stitchResultLabel = QLabel('拼接结果')
        self.stitchResultLabel.setFixedSize(300, 300)
        self.stitchResultLabel.setStyleSheet("background-color: white;")

        self.calibrateResultLabel = QLabel('标定结果')
        self.calibrateResultLabel.setFixedSize(300, 300)
        self.calibrateResultLabel.setStyleSheet("background-color: white;")

        self.reconstructResultLabel = QLabel('重构结果')
        self.reconstructResultLabel.setFixedSize(300, 300)
        self.reconstructResultLabel.setStyleSheet("background-color: white;")

        result_layout.addWidget(self.stitchResultLabel, 0, 0)
        result_layout.addWidget(self.calibrateResultLabel, 0, 1)
        result_layout.addWidget(self.reconstructResultLabel, 0, 2)

        # 添加组件到主布局
        layout.addWidget(members_label)
        layout.addLayout(image_layout)
        layout.addLayout(button_layout)
        layout.addLayout(result_layout)

        self.setLayout(layout)

    def loadImage1(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "选择图像", "", "Images (*.png *.xpm *.jpg);;All Files (*)", options=options)
        if fileName:
            print(f"Loading image 1 from {fileName}")
            self.image1 = cv2.imread(fileName)
            if self.image1 is None:
                print("Error: Unable to load image 1. Check file path and integrity.")
            else:
                pixmap = QPixmap(fileName)
                self.label1.setPixmap(pixmap.scaled(self.label1.size(), aspectRatioMode=True))

    def loadImage2(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "选择图像", "", "Images (*.png *.xpm *.jpg);;All Files (*)", options=options)
        if fileName:
            print(f"Loading image 2 from {fileName}")
            self.image2 = cv2.imread(fileName)
            if self.image2 is None:
                print("Error: Unable to load image 2. Check file path and integrity.")
            else:
                pixmap = QPixmap(fileName)
                self.label2.setPixmap(pixmap.scaled(self.label2.size(), aspectRatioMode=True))

    def stitchImages(self):
        if self.image1 is not None and self.image2 is not None:
            stitcher = cv2.Stitcher_create()
            (status, stitched) = stitcher.stitch([self.image1, self.image2])
            if status == 0:
                stitched = cv2.cvtColor(stitched, cv2.COLOR_BGR2RGB)
                height, width, channel = stitched.shape
                bytesPerLine = 3 * width
                qImg = QImage(stitched.data, width, height, bytesPerLine, QImage.Format_RGB888)
                self.stitchResultLabel.setPixmap(QPixmap.fromImage(qImg).scaled(self.stitchResultLabel.size(), Qt.KeepAspectRatio))
            else:
                self.stitchResultLabel.setText('拼接失败')
        else:
            print("Error: Both images must be loaded before stitching.")
    def calibrateCamera(self):
        # 这里看看填充下这部分的代码
        print("摄像机标定功能尚未实现")
        self.resultLabel.setText('摄像机标定功能尚未实现')

    def reconstruct3D(self):
        # 这里看看填充下这部分的代码
        print("单视图重构功能尚未实现")
        self.resultLabel.setText('单视图重构功能尚未实现')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageStitchingApp()
    ex.show()
    sys.exit(app.exec_())