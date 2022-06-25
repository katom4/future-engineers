# カラー検出及び制御量の算出と制御
import serial
import time
import color_tracking
import cv2

ser = serial.Serial('/dev/ttyAMA1', 115200)
throttle = 20

def avoid_object(detect_red, detect_green):
    if detect_red:
        steer = 20
    elif detect_green:
        steer = -20
    else:
        steer = 0
    return throttle, steer

print("--waiting SPIKE--")
threshold = 15000#回避動作を開始する画像中の物体の面積
steer = 0
cap = cv2.VideoCapture(0)

while True:

    #面積がthreshold以上の物体（赤、緑）を検出したとき、面積が大きい方の物体をdetect_~をTrueにする
    detect_red, detect_green = color_tracking.detect_sign(threshold, cap)
    throttle, steer = avoid_object(detect_red, detect_green)

    cmd = "{:3d},{:3d}@".format(throttle, steer)
    print("write: {}".format(cmd))
    ser.write(cmd.encode("utf-8"))

    #運転の終了
    #if (終了条件):
        #break

ser.write("end@".encode())

