# 用户名
USERNAME = "patience"

SOURCE_TYPE = "image"  # "video" "image" "camera"
BALL_MODEL_PATH = f"/home/{USERNAME}/ZNJY_Python/model/ball/color_best.pt"
ZONE_MODEL_PATH = f"/home/{USERNAME}/ZNJY_Python/model/zone/best.pt"

# 相机内参
F_X = 800  # 水平焦距
F_Y = 800  # 垂直焦距
C_X = 320  # 图像中心 x
C_Y = 240  # 图像中心 y
H = 150  # 相机高度

if SOURCE_TYPE == "video":
    # 视频流模式
    SOURCE_PATH = f"/home/{USERNAME}/ZNJY_Python/src/test.mp4"
    # 显示信息
    print("视频流模式")
    print("视频路径：", SOURCE_PATH)
elif SOURCE_TYPE == "image":
    # 图片模式
    SOURCE_PATH = f"/home/{USERNAME}/ZNJY_Python/src/test.jpg"
    # 显示信息
    print("图片模式")
    print("图片路径：", SOURCE_PATH)
elif SOURCE_TYPE == "camera":
    # 摄像头模式
    SOURCE_PATH = 2
    # 显示信息
    print("摄像头模式")
    print("摄像头编号：", SOURCE_PATH)