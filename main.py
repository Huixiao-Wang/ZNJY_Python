import infer  # 导入 infer.py
import config  # 导入 config.py
import pix2cam # 导入 pix2cam.py
import time
import cv2

MODEL_TYPE = 'ball'  # 'ball' or 'zone'

def main():
    if config.SOURCE_TYPE == 'image':
        print("静态模式")
        # -----图片模式----- #
        # 读取图片
        frame = cv2.imread(config.SOURCE_PATH)
        # 进行目标检测
        centers, classes, frame = infer.infer_yolo(frame, MODEL_TYPE)
        # 将像素坐标转换为相机坐标
        camera_coordinates = pix2cam.process_centers(centers)
        print("检测到的ROI中心点：", centers)
        print("检测到的ROI类别：", classes)
        print("归一化的相机坐标：", camera_coordinates)
        
        for i in range(len(centers)):
            frame = cv2.putText(frame, f"({centers[i][0]}, {centers[i][1]}) -> ({camera_coordinates[i][0]:.2f}, {camera_coordinates[i][1]:.2f}, {camera_coordinates[i][2]:.2f})", (centers[i][0], centers[i][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        px = 0
        py = 0
        z = pix2cam.pixel_to_camera_coordinates(px, py)
        frame = cv2.circle(frame, (px, py), 5, (0, 255, 0), -1)
        frame = cv2.putText(frame, f"({px}, {py}) -> ({z[0]:.2f}, {z[1]:.2f}, {z[2]:.2f})", (px+10, py+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        cv2.imshow("Result", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return 
    
    cap = cv2.VideoCapture(config.SOURCE_PATH)
    # 摄像头模式设置格式
    if config.SOURCE_TYPE == 'camera':
        print("摄像头模式")
        # 设置照片格式
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
        # 设置自动曝光
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        
    # 计算实际帧速率
    frame_count = 0
    start_time = time.time()
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("无法打开流")
            break
        centers, frame = infer.infer_yolo(frame, MODEL_TYPE)
        print("检测到的ROI中心点：", centers)
        cv2.imshow("Result", frame)
        
        frame_count += 1            
        # 计算并显示实际帧率
        elapsed_time = time.time() - start_time
        if elapsed_time > 0:
            fps = frame_count / elapsed_time
            print(f"Actual FPS: {fps:.2f}")
        
        # 按 'q' 键或者 'Esc' 键退出
        if cv2.waitKey(1) & 0xFF in [ord('q'), 27]:
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
