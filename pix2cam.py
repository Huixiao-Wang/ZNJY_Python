import numpy as np
import cv2
import config


# 相机内参矩阵
K = config.K

distortion_coeffs = config.DISTORTION_COEFFS

# 相机高度
h = config.H

def pixel_to_camera_coordinates(pixel_coords):
    """
    将像素坐标系转换为相机坐标系。
    
    参数:
    - pixel_coords: (N, 2) 或 (N, 1, 2) 像素坐标数组 (u, v)，单位是像素
    - K: 相机内参矩阵 (3x3)
    - distortion_coeffs: 畸变参数，包含 [k1, k2, p1, p2, k3]
    
    返回:
    - camera_coords: (N, 3) 相机坐标系坐标 (X, Y, Z)
    """
    # 检查输入是否为空
    if pixel_coords is None or len(pixel_coords) == 0:
        return np.array([])
    
    # 反畸变（去畸变）
    pixel_coords = np.array(pixel_coords, dtype=np.float32)
    
    # OpenCV的去畸变函数要求是 (N, 1, 2) 形状，或者 (1, 2)
    if pixel_coords.ndim == 2:
        pixel_coords = pixel_coords.reshape(-1, 1, 2)
    
    undistorted_points = cv2.undistortPoints(pixel_coords, K, distortion_coeffs)
    
    # 去畸变后像素坐标是归一化的 (u', v')，可以直接用于相机坐标系的变换
    # 归一化像素坐标 -> 相机坐标系坐标
    # u' = X / Z, v' = Y / Z

    # 去畸变后的像素坐标是 (u', v')
    normalized_coords = undistorted_points.reshape(-1, 2)

    # 反求相机坐标系的 X, Y, Z
    # 假设 Z=1，因为相机坐标系中没有给定深度信息。需要根据实际情况调整深度。
    Z = np.ones(normalized_coords.shape[0])
    X = normalized_coords[:, 0]
    Y = normalized_coords[:, 1]
    for i in range(len(Z)):
        k = h / Y[i]
        X[i] = X[i] * k
        Y[i] = h
        Z[i] = Z[i] * k  

    camera_coords = np.column_stack((X, Y, Z))
    
    return camera_coords
