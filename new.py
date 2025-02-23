import cv2
import numpy as np
import onnxruntime as ort

# 加载ONNX模型
def load_model(model_path):
    session = ort.InferenceSession(model_path)
    return session

# 对图像进行预处理（根据模型的输入要求进行调整）
def preprocess_image(image_path, input_size=(640, 640)):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 转换为RGB
    image = cv2.resize(image, input_size)  # 调整大小
    image = np.transpose(image, (2, 0, 1))  # HWC -> CHW
    image = image.astype(np.float32)  # 转为浮点数
    image = np.expand_dims(image, axis=0)  # 添加batch维度
    image /= 255.0  # 归一化
    return image

# 获取模型的输入和输出
def get_model_input_output(session):
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    return input_name, output_name

# 进行推理
def infer(model_session, input_name, output_name, image):
    result = model_session.run([output_name], {input_name: image})
    return result[0]

# 将推理结果标注到图片上
def draw_label(image_path, label, confidence, output_image_path="output.jpg"):
    image = cv2.imread(image_path)
    label_text = f"{label}: {confidence:.2f}"
    
    # 在图像上标注
    cv2.putText(image, label_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imwrite(output_image_path, image)

def main(model_path, image_path):
    # 加载模型
    session = load_model(model_path)

    # 获取模型输入和输出
    input_name, output_name = get_model_input_output(session)

    # 预处理图像
    image = preprocess_image(image_path)

    # 进行推理
    result = infer(session, input_name, output_name, image)
    print(result)

    # 假设是分类模型，结果是类别和置信度
    predicted_class = np.argmax(result)
    confidence = result[0][predicted_class]

    # 这里你可以根据模型类别获取标签
    label = str(predicted_class)  # 如果有标签，替换为实际标签

    # 在图片上绘制结果
    draw_label(image_path, label, confidence)

    print(f"Predicted Class: {label}, Confidence: {confidence:.2f}")
    print(f"Output image saved as 'output.jpg'")

if __name__ == "__main__":
    model_path = "/home/patience/ZNJY_Python/model/ball/best_half.onnx"  # 替换为你的ONNX模型路径
    image_path = "/home/patience/ZNJY_Python/src/test.jpg"  # 替换为你要推理的图片路径
    main(model_path, image_path)
