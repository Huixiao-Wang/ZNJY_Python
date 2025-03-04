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
KKK = SIZE / 640

# 模型路径
MODEL_PATH = f"/home/{USERNAME}/ZNJY_Python/model/{SIZE}/11n/best.pt"

# 640
# 相机内参矩阵
K = np.array([
    [KKK * 389.1407 , KKK * 0.       , KKK * 308.8042],
    [KKK * 0.       , KKK * 529.1912 , KKK * 307.8955],
    [KKK * 0.       , KKK * 0.       , 1.            ]
])

# 畸变系数
DISTORTION_COEFFS = np.array([0.0510, 0.3860, -0.8809, 0., 0.])

# # 1920
# # 相机内参矩阵
# K = np.array([
#     [KKK * 1086.0974 , KKK * 0.        , KKK * 941.7288],
#     [KKK * 0.        , KKK * 1468.2742 , KKK * 921.7598],
#     [KKK * 0.        , KKK * 0.        , 1.            ]
# ])

# # 畸变系数
# DISTORTION_COEFFS = np.array([0.0193, 0.3190, -1.0701, 0., 0.])


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