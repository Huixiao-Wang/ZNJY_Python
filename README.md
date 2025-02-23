# 智能救援视觉代码
---

### Python 环境配置
- 安装 miniconda
- 创建并激活虚拟环境
``` bash
conda create --name new python=3.9
conda activate new
```

- 安装 pip
- 安装所需库
```bash
pip install ultralytics opencv-python numpy torch torchvision matplotlib pyserial ncnn
```


### 使用说明
- arrange.py 按距离排序
- config.py 储存配置信息
- infer.py 推理模型并处理
- main.py 主程序，双线程
- message.py 读写串口
- multiple.py 相机坐标系转换乘法
- pix2cam.py 像素坐标系转换至相机坐标系
- rotation.py 坐标系转换旋转矩阵
- target.py 目标类，包含坐标以及距离
