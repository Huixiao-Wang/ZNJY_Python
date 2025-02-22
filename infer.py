import cv2
import numpy as np
import torch
import config
from ultralytics import YOLO

def infer_yolo(image):
    """
    使用Ultralytics YOLO进行目标检测，并返回所有识别到的ROI的中心点。
    
    :param frame: 输入图像路径
    :param model_type: 选择使用的YOLO模型类型
    :return: 检测到的ROI中心点列表 [(x1, y1), (x2, y2), ...] 以及检测结果
    """
    
    model = YOLO(config.MODEL_PATH)
    
    # 运行YOLO推理
    results = model(image)
    
    # 存储ROI中心点
    roi_centers = []
    
    # 解析ROI对应的类别
    classes = []
    
    # 解析检测结果
    for result in results:
        for box in result.boxes:
            
            x1, y1, x2, y2 = box.xyxy[0].tolist()  # 获取边界框坐标
            center_x = (x1 + x2) / 2
            # center_y = (y1 + y2) / 2
            center_y = y2
            center_x = int(center_x)
            center_y = int(center_y)
            roi_centers.append((center_x, center_y))
            classes.append(int(box.cls[0]))
            # 在图像上绘制检测框
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.circle(image, (center_x, center_y), 5, (0, 0, 255), -1)
    
    roi_centers = np.array(roi_centers)
    classes = np.array(classes)
    return roi_centers, classes, image
