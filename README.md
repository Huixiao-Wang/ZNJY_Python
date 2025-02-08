# 智能救援视觉代码
---

### 代码结构

``` bash
.
├── main.py
├── model
│   ├── ball
│   │   ├── ball_best.pt
│   │   └── color_best.pt
│   └── zone
├── process.py
├── PyEnv
│   └── requirements.txt
├── README.md
├── serial.py
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
``` bash
pip install -r ./PyEnv/requirements.txt
```


### 使用说明
- process.py 推理模型并处理
    - MODE 视频或者图片模式
    - USERNAME 改成设备的名称
- serial.py 读写串口
- main.py 主程序