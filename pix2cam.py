import numpy as np
import config

# 相机内参矩阵
f_x = config.F_X  # 水平焦距
f_y = config.F_Y  # 垂直焦距
c_x = config.C_X  # 图像中心 x
c_y = config.C_Y  # 图像中心 y

# 相机内参矩阵
K = np.array([
    [f_x, 0, c_x],
    [0, f_y, c_y],
    [0, 0, 1]
])

# 相机高度
h = config.H

def pixel_to_camera_coordinates(x_pixel, y_pixel):
    """
    将像素坐标转换为归一化的相机坐标系坐标
    :param x_pixel: 像素坐标 x
    :param y_pixel: 像素坐标 y
    :param K: 相机内参矩阵 (3x3)
    :return: 归一化的相机坐标 (x_cam, y_cam, 1)
    """
    # 将像素坐标转为齐次坐标 (x_pixel, y_pixel, 1)
    pixel_coordinates = np.array([x_pixel, y_pixel, 1])
    
    # 计算相机坐标系下的归一化坐标
    # 使用内参矩阵的逆矩阵来转换
    K_inv = np.linalg.inv(K)
    camera_coordinates = K_inv @ pixel_coordinates
    camera_coordinates = -h * camera_coordinates
    return camera_coordinates

def process_centers(centers):
    """
    处理多个像素坐标，并返回相机坐标系下的归一化坐标
    :param centers: 像素坐标数组，形状为 (N, 2)，其中 N 是像素点的数量
    :return: 相机坐标系下的归一化坐标数组，形状为 (N, 3)
    """
    camera_coords = []
    
    for center in centers:
        x_pixel, y_pixel = center
        camera_coords.append(pixel_to_camera_coordinates(x_pixel, y_pixel))
    
    # 返回一个 (N, 3) 的数组，表示 N 个像素点在相机坐标系下的归一化坐标
    return np.array(camera_coords)
