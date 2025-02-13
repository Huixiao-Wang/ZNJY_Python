import serial
import struct
import time
import threading


# 配置串口参数
ser = serial.Serial(
    port='/dev/ttyACM0',        # 设置串口设备，根据你的树莓派配置可能是 /dev/ttyAMA0 或 /dev/ttyUSB0
    baudrate=115200,            # 设置波特率
    parity=serial.PARITY_NONE, # 设置校验位，可以选择 serial.PARITY_NONE, serial.PARITY_EVEN, serial.PARITY_ODD
    stopbits=serial.STOPBITS_ONE, # 设置停止位，可以选择 serial.STOPBITS_ONE, serial.STOPBITS_ONE_POINT_FIVE, serial.STOPBITS_TWO
    bytesize=8,               # 设置数据位，常见的是 8 数据位
    timeout=1                 # 设置读取超时
)

# # 计算校验和（简单累加法，可以根据需要更复杂）
# def calculate_checksum(data):
#     return sum(data) & 0xFF  # 返回 8 位的校验和

# 构造数据包
def create_packet(data):
    header = 0x11
    footer = 0x33
    # checksum = calculate_checksum(data)
    
    packet = bytearray()
    packet.append(header)  # 添加包头
    packet.extend(data)    # 添加数据部分
    packet.append(footer)   # 添加包尾
    
    return packet


# 发送线程
def send_data():
    while True:
        data = 3.14
        
        # 使用 struct 将 float 转换为字节数据（'f' 表示 float 类型）
        data_bytes = struct.pack('f', data)
        
        # 构造数据包
        packet = create_packet(data_bytes)
        ser.write(packet)  # 编码为字节串后发送
        time.sleep(1)


# 创建并启动线程
send_thread = threading.Thread(target=send_data, daemon=True)

send_thread.start()

# 主线程等待（实际上这段代码会阻塞主线程，直到程序退出）
try:
    while True:
        print("---working---")
        time.sleep(1)

except KeyboardInterrupt:
    print("Program interrupted by user.")

finally:
    ser.close()
    print("Serial port closed.")
