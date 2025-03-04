import cv2
import numpy as np

def initialize_homography(image_path, chessboard_size=(9, 6), square_size=25.0, origin_offset=(100, 375, 0)):
    # 读取图像
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 识别棋盘格角点
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)
    if not ret:
        print("未能找到棋盘格角点")
        return None, None

    # 定义世界坐标系下的棋盘格角点
    world_points = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    world_points[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2) * square_size
    
    # 平移原点位置
    world_points -= np.array(origin_offset)
    
    # 翻转 Y 轴，使其从下到上
    world_points[:, 1] *= -1

    # 计算单应性矩阵
    H, _ = cv2.findHomography(corners, world_points[:, :2])
    return H, image

def pixel_to_world(pixel_coords, H):
    pixel_point = np.array([[pixel_coords[0], pixel_coords[1], 1]], dtype=np.float32).T
    world_point = np.dot(H, pixel_point)
    world_point /= world_point[2]  # 归一化
    return (world_point[0, 0], world_point[1, 0], 0)

def main(image_path):
    H, image = initialize_homography(image_path)
    if H is None:
        return

    # 鼠标交互回调函数
    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            world_coord = pixel_to_world((x, y), H)
            print(f"像素坐标: ({x}, {y}) -> 世界坐标: {world_coord}")

    cv2.namedWindow("Chessboard")
    cv2.setMouseCallback("Chessboard", mouse_callback)

    while True:
        cv2.imshow("Chessboard", image)
        if cv2.waitKey(1) & 0xFF == 27:  # 按ESC退出
            break

    cv2.destroyAllWindows()

# 示例调用
# main("result.jpg")
