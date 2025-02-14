import serial
import struct
import time
import threading

# 构造数据包
def create_packet(data = [0. , 0. , 0.]):
    header = 0x11
    footer = 0x33
    packet = bytearray()
    
    packet.append(header)  # 添加包头
    # 使用 struct 将 float 转换为字节数据（'f' 表示 float 类型）
    data_bytes = struct.pack('fff', *data)
    print("每个字节的十六进制表示：", [hex(b) for b in data_bytes])
    packet.extend(data_bytes)    # 添加数据部分
    packet.append(footer)  # 添加包尾
    return packet