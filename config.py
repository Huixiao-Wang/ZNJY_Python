import numpy as np
import serial
import struct

# 队伍颜色
COLOR = 0  # 0: red 1: blue

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

SOURCE_TYPE = "image"  # "video" "image" "camera"

# 设置分辨率
SIZE = 640

# 相机分辨率
WIDTH = SIZE
HEIGHT = SIZE

# 缩放比率
K = SIZE / 640

# 模型路径
MODEL_PATH = f"/home/{USERNAME}/ZNJY_Python/model/{SIZE}/11n/best.pt"

# 长线相机
# 相机内参矩阵
K = np.array([
    [K * 337.16016297 , K * 0.           , K * 281.24908569],
    [K * 0.           , K * 450.57415788 , K * 310.57172501],
    [K * 0.           , K * 0.           , 1.              ]
])

# 畸变系数
DISTORTION_COEFFS = np.array([-1.71631273e-01, 1.42053851e+00, 1.57306392e-03, -5.69209404e-03, -2.60624378e+00])

# 短线相机
# # 相机内参矩阵
# K = np.array([
#     [676.25954191 , 0.           , 321.04263929],
#     [0.           , 919.68532853 , 322.36998648],
#     [0.           , 0.           , 1.          ]
# ])

# # 畸变系数
# DISTORTION_COEFFS = np.array([-0.57196834,  -0.5764982, 0.01623252,  -0.0201935, 3.87492286])


# 相机高度
H = 165

if SOURCE_TYPE == "video":
    # 视频流模式
    SOURCE_PATH = f"/home/{USERNAME}/ZNJY_Python/src/test.mp4"
    # 显示信息
    print("视频流模式")
    print("视频路径：", SOURCE_PATH)
elif SOURCE_TYPE == "image":
    # 图片模式
    SOURCE_PATH = f"/home/{USERNAME}/ZNJY_Python/src/rule.jpg"
    # 显示信息
    print("图片模式")
    print("图片路径：", SOURCE_PATH)
elif SOURCE_TYPE == "camera":
    # 摄像头模式
    SOURCE_PATH = 2
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