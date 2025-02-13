import cv2
import numpy as np
import torch
import config
from ultralytics import YOLO

def infer_yolo(image, model_type: str = 'ball'):
    """
    使用Ultralytics YOLO进行目标检测，并返回所有识别到的ROI的中心点。
    
    :param frame: 输入图像路径
    :param model_type: 选择使用的YOLO模型类型
    :return: 检测到的ROI中心点列表 [(x1, y1), (x2, y2), ...] 以及检测结果
    """
    # 根据传入参数加载不同的YOLO模型
    model_paths = {
        'ball': config.BALL_MODEL_PATH,  # 替换为你的第一个YOLO模型路径
        'zone': config.ZONE_MODEL_PATH   # 替换为你的第二个YOLO模型路径
    }
    
    if model_type not in model_paths:
        raise ValueError("Invalid model type.")
    
    model = YOLO(model_paths[model_type])
    
    # 运行YOLO推理
    results = model(image)
    
    # 存储ROI中心点
    roi_centers = []
    
    # 解析检测结果
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()  # 获取边界框坐标
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            center_x = int(center_x)
            center_y = int(center_y)
            roi_centers.append((center_x, center_y))
            
            # 在图像上绘制检测框
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.circle(image, (center_x, center_y), 5, (0, 0, 255), -1)
    
    roi_centers = np.array(roi_centers)
    return roi_centers, image
