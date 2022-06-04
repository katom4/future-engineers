# ここにコードを書いてね :-)
# カラー検出及び制御量の算出と制御
import serial
import time
import color_tracking
import cv2

ser = serial.Serial('/dev/ttyAMA1', 115200)

#this function calculate throttle and steering using color detection.
#If object is detected, turn left
def avoid_object(detect_red, detect_green):
    if detect_red:
        throttle = 30
        steer = 100
    elif detect_green:
        throttle = 30
        steer = -99
    else:
        throttle = 30
        steer = 0
    return throttle, steer

print("--waiting SPIKE--")
threshold = 30000#回避動作を開始する画像中の物体の面積

while True:

    detect_red, detect_green = color_tracking.detect_sign(threshold)
    throttle, steer = avoid_object(detect_red, detect_green)

    cmd = "{:3d},{:3d}@".format(throttle, steer)
    print("write: {}".format(cmd))
    ser.write(cmd.encode("utf-8"))
    #time.sleep(100/1000)

ser.write("end@".encode())

