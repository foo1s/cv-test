#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author zhouhuawei time:2024/6/17
import customtkinter
import os
from PIL import Image, ImageTk
import cv2 as cv
from turtle import width
import numpy as np
from tkinter import filedialog

class Test:
    def __init__(self):
        super().__init__()

    def sift_keypoints_detect(self,image):
        # 处理图像一般很少用到彩色信息，通常直接将图像转换为灰度图
        gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        # 获取图像特征sift-SIFT特征点,实例化对象sift
        sift = cv.xfeatures2d.SIFT_create()

        # keypoints:特征点向量,向量内的每一个元素是一个KeyPoint对象，包含了特征点的各种属性信息(角度、关键特征点坐标等)
        # features:表示输出的sift特征向量，通常是128维的
        keypoints, features = sift.detectAndCompute(image, None)

        # cv.drawKeyPoints():在图像的关键特征点部位绘制一个小圆圈
        # 如果传递标志flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,它将绘制一个大小为keypoint的圆圈并显示它的方向
        # 这种方法同时显示图像的坐标，大小和方向，是最能显示特征的一种绘制方式
        keypoints_image = cv.drawKeypoints(
            gray_image, keypoints, None, flags=cv.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)

        # 返回带关键特征点的图像、关键特征点和sift的特征向量
        return keypoints_image, keypoints, features

    # 使用KNN检测来自左右图像的SIFT特征，随后进行匹配
    def get_feature_point_ensemble(self, features_right, features_left):
        # 创建BFMatcher对象解决匹配
        bf = cv.BFMatcher()
        # knnMatch()函数：返回每个特征点的最佳匹配k个匹配点
        # features_right为模板图，features_left为匹配图
        matches = bf.knnMatch(features_right, features_left, k=2)
        # 利用sorted()函数对matches对象进行升序(默认)操作
        matches = sorted(matches, key=lambda x: x[0].distance / x[1].distance)
        # x:x[]字母可以随意修改，排序方式按照中括号[]里面的维度进行排序，[0]按照第一维排序，[2]按照第三维排序

        # 建立列表good用于存储匹配的点集
        good = []
        for m, n in matches:
            # ratio的值越大，匹配的线条越密集，但错误匹配点也会增多
            ratio = 0.6
            if m.distance < ratio * n.distance:
                good.append(m)

        # 返回匹配的关键特征点集
        return good

    # 计算视角变换矩阵H，用H对右图进行变换并返回全景拼接图像
    def Panorama_stitching(self, image_right, image_left):
        _, keypoints_right, features_right = Test.sift_keypoints_detect(image_right)
        _, keypoints_left, features_left = Test.sift_keypoints_detect(image_left)
        goodMatch = Test.get_feature_point_ensemble(features_right, features_left)

        # 当筛选项的匹配对大于4对(因为homography单应性矩阵的计算需要至少四个点)时,计算视角变换矩阵
        if len(goodMatch) > 4:
            # 获取匹配对的点坐标
            ptsR = np.float32(
                [keypoints_right[m.queryIdx].pt for m in goodMatch]).reshape(-1, 1, 2)
            ptsL = np.float32(
                [keypoints_left[m.trainIdx].pt for m in goodMatch]).reshape(-1, 1, 2)

            # ransacReprojThreshold：将点对视为内点的最大允许重投影错误阈值(仅用于RANSAC和RHO方法时),若srcPoints和dstPoints是以像素为单位的，该参数通常设置在1到10的范围内
            ransacReprojThreshold = 4

            # cv.findHomography():计算多个二维点对之间的最优单映射变换矩阵 H(3行x3列),使用最小均方误差或者RANSAC方法
            # 函数作用:利用基于RANSAC的鲁棒算法选择最优的四组配对点，再计算转换矩阵H(3*3)并返回,以便于反向投影错误率达到最小
            Homography, status = cv.findHomography(
                ptsR, ptsL, cv.RANSAC, ransacReprojThreshold)

            # cv.warpPerspective()：透视变换函数，用于解决cv2.warpAffine()不能处理视场和图像不平行的问题
            # 作用：就是对图像进行透视变换，可保持直线不变形，但是平行线可能不再平行
            Panorama = cv.warpPerspective(
                image_right, Homography, (image_right.shape[1] + image_left.shape[1], image_right.shape[0]))

            cv.imshow("扭曲变换后的右图", Panorama)
            cv.waitKey(0)
            cv.destroyAllWindows()
            # 将左图加入到变换后的右图像的左端即获得最终图像
            Panorama[0:image_left.shape[0], 0:image_left.shape[1]] = image_left

            # 返回全景拼接的图像
            return Panorama
