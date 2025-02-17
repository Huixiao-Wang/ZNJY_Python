import numpy as np

def rotate(vectors, roll, pitch, yaw):
    """
    根据 Roll、Pitch、Yaw 角度，计算旋转矩阵（采用 ZYX 顺序）
    
    参数：
    roll (float): 绕 x 轴的旋转角度 (单位：弧度)
    pitch (float): 绕 y 轴的旋转角度 (单位：弧度)
    yaw (float): 绕 z 轴的旋转角度 (单位：弧度)
    
    返回：
    numpy.ndarray: 3x3 的旋转矩阵
    """
    
    # 绕 x 轴的旋转矩阵
    R_x = np.array([
        [1, 0, 0],
        [0, np.cos(roll), -np.sin(roll)],
        [0, np.sin(roll), np.cos(roll)]
    ])
    
    # 绕 y 轴的旋转矩阵
    R_y = np.array([
        [np.cos(pitch), 0, np.sin(pitch)],
        [0, 1, 0],
        [-np.sin(pitch), 0, np.cos(pitch)]
    ])
    
    # 绕 z 轴的旋转矩阵
    R_z = np.array([
        [np.cos(yaw), -np.sin(yaw), 0],
        [np.sin(yaw), np.cos(yaw), 0],
        [0, 0, 1]
    ])
    
    # 总旋转矩阵，按照 ZYX 顺序相乘
    R = np.dot(R_z, np.dot(R_y, R_x))
    
    # 旋转矩阵与每个向量相乘
    rotated_vectors = np.dot(vectors, R.T)  # 这里旋转矩阵是转置的
    return rotated_vectors
