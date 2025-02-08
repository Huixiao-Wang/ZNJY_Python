import cv2
import torch
import numpy as np
from ultralytics import YOLO
import time


# 设置模式
# MODE = "VIDEOSTREAM" # 视频流模式
VIDEOPATH = 2

MODE = "PICTURE" # 图片模式
PICTUREPATH = "src/test.jpg"

# 用户名
USERNAME = "patience"

# 模型路径
color_model_path = f"/home/{USERNAME}/ZNJY_Python/model/ball/color_best.pt"
ball_model_path = f"/home/{USERNAME}/ZNJY_Python/model/ball/ball_best.pt"

# 加载 YOLO 模型
color_model = YOLO(color_model_path)
ball_model = YOLO(ball_model_path)

# 计算 IOU（交并比）
def compute_iou(box1, box2):
    x1, y1, x2, y2 = box1
    x1g, y1g, x2g, y2g = box2

    xi1 = max(x1, x1g)
    yi1 = max(y1, y1g)
    xi2 = min(x2, x2g)
    yi2 = min(y2, y2g)
    inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)

    box1_area = (x2 - x1) * (y2 - y1)
    box2_area = (x2g - x1g) * (y2g - y1g)
    
    union_area = box1_area + box2_area - inter_area
    return inter_area / union_area if union_area > 0 else 0

# 处理每一帧
def process_frame(frame):
    # 颜色检测
    color_results = color_model(frame)  # 直接推理
    color_detections = color_results[0].boxes.data.cpu().numpy()  # 解析结果 (x1, y1, x2, y2, conf, class)

    # 球体检测
    ball_results = ball_model(frame)  # 直接推理
    ball_detections = ball_results[0].boxes.data.cpu().numpy()  # 解析结果 (x1, y1, x2, y2, conf, class)

    # 结果匹配
    matched_results = []
    for color_box in color_detections:
        x1_c, y1_c, x2_c, y2_c, conf_c, class_c = color_box

        for ball_box in ball_detections:
            x1_b, y1_b, x2_b, y2_b, conf_b, class_b = ball_box

            iou = compute_iou((x1_c, y1_c, x2_c, y2_c), (x1_b, y1_b, x2_b, y2_b))
            
            if iou > 0.3:  # IOU 阈值（可以调整）
                matched_results.append(((x1_c, y1_c, x2_c, y2_c), (x1_b, y1_b, x2_b, y2_b), class_c))

    # 画框显示结果
    for color_box, ball_box, color_class in matched_results:
        x1, y1, x2, y2 = ball_box
        dict_color = {0: "red", 1: "blue", 2: "yellow", 3: "black"}
        color_name = f"{dict_color[int(color_class)]}-ball"
                
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.putText(frame, color_name, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return frame

if MODE == "PICTURE":
    print("Processing picture...")
    
    # 读取图片
    frame = cv2.imread(PICTUREPATH)
    frame = cv2.resize(frame, (1080, 1080))
    processed_frame = process_frame(frame)

    cv2.imshow("Result", processed_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if MODE == "VIDEOSTREAM":
    print("Processing video stream...")
    
    # 读取视频流
    cap = cv2.VideoCapture(VIDEOPATH)

    # 设置照片格式
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

    # 设置自动曝光
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)

    # 计算实际帧速率
    frame_count = 0
    start_time = time.time()

    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.resize(frame, (1080, 1080))
        
        if not ret:
            print("Can't receive frame (stream end?).")
            break
        
        frame_count += 1
        processed_frame = process_frame(frame)
        
        # 计算并显示实际帧率
        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            fps = frame_count / elapsed_time
            print(f"Actual FPS: {fps:.2f}")
        
        cv2.imshow("Result", processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
