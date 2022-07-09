# ここにコードを書いてね :-)
# カラー検出及び制御量の算出と制御
import serial
import time
import color_tracking
import cv2

ser = serial.Serial('/dev/ttyAMA1', 115200)
throttle = 20

time.sleep(1)

print("--waiting SPIKE--")
threshold = 15000#回避動作を開始する画像中の物体の面積
steer = 0
cap = cv2.VideoCapture(0)
values = ""

ser.reset_input_buffer()

while True:
    ser.reset_input_buffer()
    values = ser.read(8).decode("utf-8")
    value_list = values.split("@")
    values = value_list[0].split(",")

    #When dist_sensor return None, distance is set to 0.
    print(values)
    #print(int(value_list[0]))

    time.sleep(0.1)
    distance = int(values[0])
    gyro_yaw = int(values[1])

    #print("Distance: {}[cm]".format(distance))

    #面積がthreshold以上の物体（赤、緑）を検出したとき、面積が大きい方の物体をdetect_~をTrueにする
    detect_red, detect_green = color_tracking.detect_sign(threshold, cap)
    #throttle, steer = avoid_object(detect_red, detect_green)
    throttle, steer = distance_controll(distance)
    #send operations(throttle, steer)
    cmd = "{:3d},{:3d}@".format(throttle, steer)
    print("write: {}".format(cmd))
    print("steer:{;3d}",steer)
    ser.write(cmd.encode("utf-8"))

    #運転の終了
    #if (終了条件):
    #break

ser.write("end@".encode())


