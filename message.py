import serial
import struct
import time
import threading

# 配置串口参数
ser = serial.Serial(
    port='/dev/ttyACM0',        # 设置串口设备，根据你的树莓派配置可能是 /dev/ttyAMA0 或 /dev/ttyUSB0
    baudrate=115200,            # 设置波特率
    parity=serial.PARITY_NONE,  # 设置校验位
    stopbits=serial.STOPBITS_ONE,  # 设置停止位
    bytesize=8,                 # 设置数据位
    timeout=1                    # 设置读取超时
)

# 构造数据包
def create_packet(data):
    header = 0x11
    footer = 0x33
    packet = bytearray()
    packet.append(header)  # 添加包头
    packet.extend(data)    # 添加数据部分
    packet.append(footer)  # 添加包尾
    return packet


# 发送线程
def send_data():
    while True:
        data = 1145.14  # 发送的数据，这里是一个 float 类型的值
        
        # 使用 struct 将 float 转换为字节数据（'f' 表示 float 类型）
        data_bytes = struct.pack('f', data)
        
        # 构造数据包
        packet = create_packet(data_bytes)
        
        # 发送数据包
        ser.write(packet)  # 编码为字节串后发送
        print("每个字节的十六进制表示：", [hex(b) for b in data_bytes])
        
        time.sleep(0.001)  # 每秒发送一次数据


# 接收线程
def read_data():
    while True:
        if ser.in_waiting > 0:  # 如果串口缓冲区有数据
            data = ser.read(ser.in_waiting)  # 读取所有可用的数据
            # 检查接收到的数据是否包含完整的浮动数据（假设每个浮动数由4个字节组成）
            if len(data) >= 4:
                # 将字节数据转换为浮动数
                received_float = struct.unpack('f', data[:4])[0]  # 'f' 表示 4 字节浮动数
                
                print(f"Received float: {received_float}")
            
            else:
                print("Incomplete data received.")
        time.sleep(0.001)  # 每 0.1 秒检查一次串口是否有数据


# 创建并启动线程
send_thread = threading.Thread(target=send_data, daemon=True)  # 发送线程
read_thread = threading.Thread(target=read_data, daemon=True)  # 接收线程

# 启动线程
send_thread.start()
read_thread.start()

# 主线程等待（实际上这段代码会阻塞主线程，直到程序退出）
try:
    while True:
        print("---working---")
        time.sleep(0.001)  # 每秒打印一次，表示主线程在正常运行

except KeyboardInterrupt:
    print("Program interrupted by user.")

finally:
    ser.close()  # 关闭串口
    print("Serial port closed.")
