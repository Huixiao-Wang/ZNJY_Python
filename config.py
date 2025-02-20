import numpy as np
import serial
import struct

# 串口开关
PORT = False

if PORT:
    # 配置串口参数
    SER = serial.Serial(
        port='/dev/ttyACM0',        # 设置串口设备，根据你的树莓派配置可能是 /dev/ttyAMA0 或 /dev/ttyUSB0
        baudrate=115200,            # 设置波特率
        parity=serial.PARITY_NONE,  # 设置校验位
        stopbits=serial.STOPBITS_ONE,  # 设置停止位
        bytesize=8,                 # 设置数据位
        timeout=1                    # 设置读取超时
    )

# 用户名
USERNAME = "patience"

SOURCE_TYPE = "camera"  # "video" "image" "camera"
BALL_MODEL_PATH = f"/home/{USERNAME}/ZNJY_Python/model/ball/color_best.pt"
ZONE_MODEL_PATH = f"/home/{USERNAME}/ZNJY_Python/model/zone/best.pt"

# 相机内参矩阵
K = np.array([
    [337.16016297 , 0.           , 281.24908569],
    [0.           , 450.57415788 , 310.57172501],
    [0.           , 0.           , 1.          ]
])

# 畸变系数
DISTORTION_COEFFS = np.array([-1.71631273e-01, 1.42053851e+00, 1.57306392e-03, -5.69209404e-03, -2.60624378e+00])

# 相机高度
H = 150

if SOURCE_TYPE == "video":
    # 视频流模式
    SOURCE_PATH = f"/home/{USERNAME}/ZNJY_Python/src/test.mp4"
    # 显示信息
    print("视频流模式")
    print("视频路径：", SOURCE_PATH)
elif SOURCE_TYPE == "image":
    # 图片模式
    SOURCE_PATH = f"/home/{USERNAME}/ZNJY_Python/src/color_0189.jpg"
    # 显示信息
    print("图片模式")
    print("图片路径：", SOURCE_PATH)
elif SOURCE_TYPE == "camera":
    # 摄像头模式
    SOURCE_PATH = 0
    # 显示信息
    print("摄像头模式")
    print("摄像头编号：", SOURCE_PATH)

DICTIONARY = {
    0: "red",
    1: "blue",
    2: "yellow",
    3: "black",
    4: "bluezone",
    5: "redzone"
}