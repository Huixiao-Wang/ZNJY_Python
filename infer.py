import cv2
import numpy as np
import torch
import config
import time
from ultralytics import YOLO

def infer_yolo(image, flag = 1):
    """
    使用Ultralytics YOLO进行目标检测, 并返回所有识别到的ROI的中心点。
    
    :param image: 输入图像路径
    :param flag: 1表示检测ball, 0表示检测zone
    :return: 检测到的ROI中心点列表 [(x1, y1), (x2, y2), ...] 以及检测结果
    """
    
    model = YOLO(config.MODEL_PATH, task='detect')
    # 运行YOLO推理
    results = model(image)
    # 储存ball的中心点
    ball_centers = []
    ball_classes = []
    # 储存zone的中心点
    zone_centers = []
    zone_classes = []
    zone_xy=[]
    
    # 解析zone
    for result in results:
        for box in result.boxes:
            # 过滤掉置信度较低的检测结果
            if box.conf < 0.5:
                continue
            if box.cls[0] > 3:
                # 获取坐标
                x1, y1, x2, y2 = box.xyxy[0].tolist()  # 获取边界框坐标
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2
                # center_y = y2
                center_x = int(center_x)
                center_y = int(center_y)
                zone_centers.append((center_x, center_y))
                zone_classes.append(int(box.cls[0]))
                zone_xy.append((x1,y1,x2,y2))
                # 在图像上绘制检测框
                cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.circle(image, (center_x, center_y), 5, (0, 0, 255), -1)
    # 解析ball
    for result in results:
        for box in result.boxes:
            # 过滤掉置信度较低的检测结果
            if box.conf < 0.5:
                continue
            if box.cls[0] <= 3 and box.cls[0] != (1-config.COLOR):
                # 获取坐标
                x1, y1, x2, y2 = box.xyxy[0].tolist()  # 获取边界框坐标
                # ball in zone?
                flag_ = False
                for (ax1,ay1,ax2,ay2) in zone_xy:
                    if x1 >= ax1 and y1 >= ay1 and x2 <= ax2 and y2 <= ay2:
                        flag_ = True
                        break
                if flag_:
                    continue
                center_x = (x1 + x2) / 2
                # center_y = (y1 + y2) / 2
                center_y = y2
                center_x = int(center_x)
                center_y = int(center_y)
                ball_centers.append((center_x, center_y))
                ball_classes.append(int(box.cls[0]))
                # 在图像上绘制检测框
                cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.circle(image, (center_x, center_y), 5, (0, 0, 255), -1)
    
    # ball
    if flag == 1:
        print("ball mode")
        roi_centers = np.array(ball_centers)
        classes = np.array(ball_classes)
        return roi_centers, classes, image
    
    print("zone mode")
    # zone
    # 存储ROI中心点
    roi_centers = []
    # 解析ROI对应的类别
    classes = []
    for i in range(len(zone_centers)):
        if zone_classes[i] == 5 - config.COLOR:
            roi_centers.append(zone_centers[i])
            classes.append(zone_classes[i])
    roi_centers = np.array(roi_centers)
    classes = np.array(classes)
    return roi_centers, classes, image
