import serial
import time
import threading

# 设置串口参数
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# 发送线程
def send_data():
    while True:
        ser.write(b"Heartbeat: Raspberry Pi is alive\n")
        time.sleep(1)

# 接收线程
def receive_data():
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').strip()
            print(f"Received: {data}")
            if data == 'ping':
                ser.write(b'pong\n')

# 创建并启动线程
send_thread = threading.Thread(target=send_data, daemon=True)
receive_thread = threading.Thread(target=receive_data, daemon=True)

send_thread.start()
receive_thread.start()

# 主线程等待（实际上这段代码会阻塞主线程，直到程序退出）
try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Program interrupted by user.")

finally:
    ser.close()
    print("Serial port closed.")
