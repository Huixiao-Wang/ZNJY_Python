import cv2
import numpy as np
import config

# 计算单应性矩阵
H = config.H

def pixel_to_world(pixel_coords):
    world_coords_list = []
    for pixel_coord in pixel_coords:
        pixel_point = np.array([[pixel_coord[0], pixel_coord[1], 1]], dtype=np.float32).T
        world_point = np.dot(H, pixel_point)
        world_point /= world_point[2]  # 归一化
        world_coords_list.append((world_point[0, 0], world_point[1, 0], 0))
    return world_coords_list
