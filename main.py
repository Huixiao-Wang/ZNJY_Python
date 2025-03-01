import time
import struct
import threading
import serial
import queue
import message
import infer
import config
import pix2cam
import rotation
import multiple
import target
import arrange
import numpy as np
import cv2

if config.PORT:
    ser = config.SER  # 串口对象

# 处理图像
def process_and_send_data(input_queue):
    
    if config.SOURCE_TYPE == 'image':
        print("静态模式")
        while True:
            # -----图片模式----- #
            # 获取欧拉角以及标志位
            if config.PORT:
                # 从队列中获取数据
                receive = input_queue.get()
                roll, pitch, flag = receive[0], receive[1], receive[2]
                print(f"Received roll: {roll}, pitch: {pitch}, flag: {flag}")
            else:
                roll, pitch, flag = 0., 0., 1
            
            # 读取图片
            frame = cv2.imread(config.SOURCE_PATH)
            frame = cv2.resize(frame, (config.WIDTH, config.HEIGHT))
            # 进行目标检测
            centers, classes, frame = infer.infer_yolo(frame, flag)
            # 如果没有检测到目标，则发送空数据
            if len(centers) == 0 or centers is None:
                if config.PORT:
                    # 构造数据包
                    packet = message.create_packet([0., 0., 0.])  # 发送空数据
                    ser.write(packet)  # 编码为字节串后发送
                    
                if config.USERNAME == 'pi':
                    cv2.imwrite("./result.jpg", frame)
                else:    
                    cv2.imshow("Result", frame)
                
                continue
        
            # 将像素坐标转换为相机坐标
            camera_coordinates = pix2cam.pixel_to_camera_coordinates(centers)
            # 将相机坐标转换为世界坐标
            vectors = rotation.rotate(camera_coordinates, -roll, -pitch, 0)
            # 将世界坐标转换为实际坐标
            vectors = multiple.mult(vectors)
            # 将检测到的目标封装成 target 对象
            targets = []
            for i in range(len(vectors)):
                targets.append(target.target(vectors[i], classes[i]))    
            # 按距离排序
            targets = arrange.sort_targets(targets)
            # 打印排序后的目标信息
            for i in range(len(targets)):
                print(targets[i])
            
            # print("检测到的ROI中心点：", centers)
            # print("检测到的ROI类别：", classes)
            # print("相机坐标：", camera_coordinates)
            # print("世界坐标：", vectors)
            
            # 在图像上标注目标信息
            for i in range(len(centers)):
                frame = cv2.putText(frame, f"({centers[i][0]}, {centers[i][1]}) -> ({camera_coordinates[i][0]:.2f}, {camera_coordinates[i][1]:.2f}, {camera_coordinates[i][2]:.2f})", (centers[i][0], centers[i][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            
            # 发送数据
            data = targets[0].vector  # 发送最近的目标数据
            print("发送的数据：", data)
            if config.PORT:
                # 构造数据包
                packet = message.create_packet(data)
                ser.write(packet)  # 编码为字节串后发送
            
            # 按 'q' 键或者 'Esc' 键退出
            if cv2.waitKey(1) & 0xFF in [ord('q'), 27]:
                break
            
            # 显示图像
            if config.USERNAME == 'pi':
                cv2.imwrite("./result.jpg", frame)
            else:
                cv2.imwrite("./result.jpg", frame)    
                cv2.imshow("Result", frame)
            # cv2.waitKey(0)
            cv2.destroyAllWindows()
    
    # -----视频流模式----- #
    cap = cv2.VideoCapture(config.SOURCE_PATH)
    # 摄像头模式设置格式
    if config.SOURCE_TYPE == 'camera':
        print("摄像头模式")
        # 设置照片格式
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.HEIGHT)
        # 设置自动曝光
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
    
    # 计算实际帧速率
    frame_count = 0
    start_time = time.time()
    
    while cap.isOpened():
        
        # 获取欧拉角与标志位
        if config.PORT:
            # 从队列中获取数据
            receive = input_queue.get()
            roll, pitch, flag = receive[0], receive[1], receive[2]
            print(f"Received roll: {roll}, pitch: {pitch}, flag: {flag}")
        else:
            roll, pitch, flag = 0., 0., 1
        
        # 读取视频流
        ret, frame = cap.read()
        frame = cv2.resize(frame, (config.WIDTH, config.HEIGHT))
        
        if not ret:
            print("无法打开流")
            if config.PORT:
                # 构造数据包
                packet = message.create_packet([-1., -1., -1.])  # 发送错误数据
                ser.write(packet)  # 编码为字节串后发送
                break
        
        # 进行目标检测
        centers, classes, frame = infer.infer_yolo(frame, flag)
        # 如果没有检测到目标，则发送空数据
        if len(centers) == 0 or centers is None:
            if config.PORT:
                # 构造数据包
                packet = message.create_packet([-1., -1., -1.])  # 发送空数据
                ser.write(packet)  # 编码为字节串后发送
            
            frame_count += 1
            # 计算并显示实际帧率
            elapsed_time = time.time() - start_time
            if elapsed_time > 0:
                fps = frame_count / elapsed_time
                print(f"Actual FPS: {fps:.2f}")
                
            if config.USERNAME == 'pi':
                cv2.imwrite("./result.jpg", frame)
            else:    
                cv2.imshow("Result", frame)
            
            continue
        
        # 将像素坐标转换为相机坐标
        camera_coordinates = pix2cam.pixel_to_camera_coordinates(centers)
        # 将相机坐标转换为世界坐标
        vectors = rotation.rotate(camera_coordinates, -roll, -pitch, 0)
        # 将世界坐标转换为实际坐标
        vectors = multiple.mult(vectors)
        # 将检测到的目标封装成 target 对象
        targets = []
        for i in range(len(vectors)):
            targets.append(target.target(vectors[i], classes[i]))    
        # 按距离排序
        targets = arrange.sort_targets(targets)
        # 打印排序后的目标信息
        for i in range(len(targets)):
            print(targets[i])
        
        # print("检测到的ROI中心点：", centers)
        # print("检测到的ROI类别：", classes)
        # print("相机坐标：", camera_coordinates)
        # print("世界坐标：", vectors)
        
        # 在图像上标注目标信息
        for i in range(len(centers)):
            frame = cv2.putText(frame, f"({centers[i][0]}, {centers[i][1]}) -> ({camera_coordinates[i][0]:.2f}, {camera_coordinates[i][1]:.2f}, {camera_coordinates[i][2]:.2f})", (centers[i][0], centers[i][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        data = targets[0].vector  # 发送最近的目标数据
        print("发送的数据：", data)
        
        # 发送数据
        if config.PORT:
            # 构造数据包
            packet = message.create_packet(data)
            ser.write(packet)  # 编码为字节串后发送
        
        # 显示图像
        if config.USERNAME == 'pi':
            cv2.imwrite("./result.jpg", frame)
        else:    
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
def read_data(input_queue):
    while True:
        if ser.in_waiting > 0:  # 如果串口缓冲区有数据
            data = ser.read(ser.in_waiting)  # 读取所有可用的数据

            # 检查接收到的数据是否包含完整的浮动数据（假设每个浮动数由4个字节组成，3个浮动数共12字节）
            if len(data) >= 9:
                # 将字节数据转换为浮动数
                roll, pitch, flag = struct.unpack('ffB', data[:9])  # 'fff' 表示三个 4 字节浮动数
                # 将接收到的三个浮动数放入队列
                input_queue.put((roll / 180 * np.pi, pitch / 180 * np.pi, flag))
                print(f"Received roll: {roll}, pitch: {pitch}, flag: {flag}")
            
            else:
                # 如果数据不完整，则放入默认值 0
                input_queue.put((0, 0, 0))
                print("Incomplete data received.")
        
        time.sleep(0.001)  # 每 1 毫秒检查一次串口是否有数据

def main():
    # 创建一个队列，用于线程间传递数据
    input_queue = queue.Queue()

    if config.PORT:
        # 创建并启动线程
        send_thread = threading.Thread(target=process_and_send_data, args=(input_queue,), daemon=True)  # 发送线程
        read_thread = threading.Thread(target=read_data, args=(input_queue,), daemon=True)  # 接收线程

        # 启动线程
        send_thread.start()
        read_thread.start()
    else:
        process_and_send_data(input_queue)
    
    # 主线程等待（实际上这段代码会阻塞主线程，直到程序退出）
    try:
        while True:
            print("---working---")
            time.sleep(1)  # 每秒打印一次，表示主线程在正常运行

    except KeyboardInterrupt:
        print("Program interrupted by user.")

    finally:
        if config.PORT:
            ser.close()  # 关闭串口
            print("Serial port closed.")
        else:
            print("Program exits.")
if __name__ == "__main__":
    main()