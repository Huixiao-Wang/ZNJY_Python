import time
import struct
import threading
import serial
import queue
import message
import infer
import config
import pix2cam
import cv2

ser = config.SER  # 串口对象

MODEL_TYPE = 'ball'  # 'ball' or 'zone'

# 处理图像
def process_and_send_data():
    
    if config.SOURCE_TYPE == 'image':
        print("静态模式")
        while True:
            # -----图片模式----- #
            
            # 从队列中获取数据
            temp = input_queue.get()
            print("Received data from queue:", temp)
            
            # 读取图片
            frame = cv2.imread(config.SOURCE_PATH)
            # 进行目标检测
            centers, classes, frame = infer.infer_yolo(frame, MODEL_TYPE)
            # 将像素坐标转换为相机坐标
            camera_coordinates = pix2cam.pixel_to_camera_coordinates(centers)
            print("检测到的ROI中心点：", centers)
            print("检测到的ROI类别：", classes)
            print("相机坐标：", camera_coordinates)
            
            for i in range(len(centers)):
                frame = cv2.putText(frame, f"({centers[i][0]}, {centers[i][1]}) -> ({camera_coordinates[i][0]:.2f}, {camera_coordinates[i][1]:.2f}, {camera_coordinates[i][2]:.2f})", (centers[i][0], centers[i][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            
            data = [camera_coordinates[0][0], camera_coordinates[0][1], camera_coordinates[0][2]] # 从相机坐标中提取 x, y, z
            
            # 构造数据包
            packet = message.create_packet(data)
            ser.write(packet)  # 编码为字节串后发送
            
            cv2.imshow("Result", frame)
            cv2.destroyAllWindows()
    
    # -----视频流模式----- #
    cap = cv2.VideoCapture(config.SOURCE_PATH)
    # 摄像头模式设置格式
    if config.SOURCE_TYPE == 'camera':
        print("摄像头模式")
        # 设置照片格式
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
        # 设置自动曝光
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
        
    # 计算实际帧速率
    frame_count = 0
    start_time = time.time()
    
    while cap.isOpened():
        
        # 从队列中获取数据
        temp = input_queue.get()
        print("Received data from queue:", temp)
        
        # 读取视频流
        ret, frame = cap.read()
        frame = cv2.resize(frame, (640, 640))
        
        if not ret:
            print("无法打开流")
            
            # 构造数据包
            packet = message.create_packet([-1., -1., -1.])  # 发送错误数据
            ser.write(packet)  # 编码为字节串后发送
            break
        
        # 进行目标检测
        centers, classes, frame = infer.infer_yolo(frame, MODEL_TYPE)
        if len(centers) == 0 or centers is None:
            # 构造数据包
            packet = message.create_packet([0., 0., 0.])  # 发送空数据
            ser.write(packet)  # 编码为字节串后发送
            
            frame_count += 1
            # 计算并显示实际帧率
            elapsed_time = time.time() - start_time
            if elapsed_time > 0:
                fps = frame_count / elapsed_time
                print(f"Actual FPS: {fps:.2f}")
            cv2.imshow("Result", frame)
            continue
        
        # 将像素坐标转换为相机坐标
        camera_coordinates = pix2cam.pixel_to_camera_coordinates(centers)
        print("检测到的ROI中心点：", centers)
        print("检测到的ROI类别：", classes)
        print("相机坐标：", camera_coordinates)
        
        for i in range(len(centers)):
            frame = cv2.putText(frame, f"({centers[i][0]}, {centers[i][1]}) -> ({camera_coordinates[i][0]:.2f}, {camera_coordinates[i][1]:.2f}, {camera_coordinates[i][2]:.2f})", (centers[i][0], centers[i][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        data = [camera_coordinates[0][0], camera_coordinates[0][1], camera_coordinates[0][2]] # 从相机坐标中提取 x, y, z
        
        # 构造数据包
        packet = message.create_packet(data)
        ser.write(packet)  # 编码为字节串后发送
        
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

# 接收线程
def read_data():
    while True:
        if ser.in_waiting > 0:  # 如果串口缓冲区有数据
            data = ser.read(ser.in_waiting)  # 读取所有可用的数据
            # 检查接收到的数据是否包含完整的浮动数据（假设每个浮动数由4个字节组成）
            if len(data) >= 4:
                # 将字节数据转换为浮动数
                received_float = struct.unpack('f', data[:4])[0]  # 'f' 表示 4 字节浮动数
                # 将接收到的数据放入队列
                input_queue.put(received_float)
                print(f"Received float: {received_float}")
            
            else:
                # 将 0 放入队列
                input_queue.put(0)
                print("Incomplete data received.")
        time.sleep(0.001)  # 每 0.1 秒检查一次串口是否有数据

def main():
    # 创建一个队列，用于线程间传递数据
    input_queue = queue.Queue()

    # 创建并启动线程
    send_thread = threading.Thread(target=process_and_send_data, args=(input_queue,), daemon=True)  # 发送线程
    read_thread = threading.Thread(target=read_data, args=(input_queue,), daemon=True)  # 接收线程

    # 启动线程
    send_thread.start()
    read_thread.start()

    # 主线程等待（实际上这段代码会阻塞主线程，直到程序退出）
    try:
        while True:
            print("---working---")
            time.sleep(1)  # 每秒打印一次，表示主线程在正常运行

    except KeyboardInterrupt:
        print("Program interrupted by user.")

    finally:
        ser.close()  # 关闭串口
        print("Serial port closed.")

if __name__ == "__main__":
    main()