# 智能救援视觉代码
---

### 代码结构

``` bash
.
├── config.py
├── infer.py
├── main.py
├── message.py
├── model
│   ├── ball
│   │   ├── ball_best.onnx
│   │   ├── ball_best.pt
│   │   ├── best.onnx
│   │   ├── best.pt
│   │   ├── best_quantized.onnx
│   │   └── color_best.pt
│   └── zone
│       └── best.pt
├── new.py
├── pix2cam.py
├── process.py
├── __pycache__
│   ├── config.cpython-39.pyc
│   ├── infer.cpython-39.pyc
│   └── pix2cam.cpython-39.pyc
├── PyEnv
│   └── requirements.txt
├── README.md
├── result.jpg
└── src
    └── test.jpg
```

### Python 环境配置
- 安装 miniconda
- 创建并激活虚拟环境
``` bash
conda create --name new python=3.9
conda activate new
```

- 安装 pip
- 安装所需库
- way1
``` bash
pip install -r ./PyEnv/requirements.txt
```
- way2
```bash
pip install ultralytics opencv-python numpy torch torchvision matplotlib pyserial
```


### 使用说明
- config.py 储存配置信息
- infer.py 推理模型并处理
- pix2cam.py 像素坐标系转换至相机坐标系
- message.py 读写串口
- main.py 主程序

### 待开发
- new
- process
- **无法加载量化模型**