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

# # 缩放比率
# KKK = SIZE / 640

# 模型路径
MODEL_PATH = f"./model/{SIZE}/11n/best.pt"

# # 640
# # 相机内参矩阵
# K = np.array([
#     [KKK * 389.291907056334 , KKK * 0.       , KKK * 309.904313963805],
#     [KKK * 0.       , KKK * 524.065659268696 , KKK * 321.913286920233],
#     [KKK * 0.       , KKK * 0.       , 1.            ]
# ])

# # 畸变系数
# DISTORTION_COEFFS = np.array([0.157628688318473, -0.256514704420192, 0.0930423772352066, 0.00162845670018406, -0.00364984416697210], dtype=np.float32)

# # 1920
# # 相机内参矩阵
# K = np.array([
#     [KKK * 1086.0974 , KKK * 0.        , KKK * 941.7288],
#     [KKK * 0.        , KKK * 1468.2742 , KKK * 921.7598],
#     [KKK * 0.        , KKK * 0.        , 1.            ]
# ])

# # 畸变系数
# DISTORTION_COEFFS = np.array([0.0193, 0.3190, -1.0701, 0., 0.])

# 单应性矩阵
H = [[-1.23055770e+00, -4.40170809e-02,  4.00060160e+02],
     [-1.63041577e-02, -1.45042710e-01, -4.49403769e+02],
     [-4.22898865e-05, -5.46847576e-03,  1.00000000e+00]]

if SOURCE_TYPE == "video":
    # 视频流模式
    SOURCE_PATH = f"./src/test.mp4"
    # 显示信息
    print("视频流模式")
    print("视频路径：", SOURCE_PATH)
elif SOURCE_TYPE == "image":
    # 图片模式
    SOURCE_PATH = f"./src/rule.jpg"
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