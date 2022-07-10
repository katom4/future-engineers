# ここにコードを書いてね :-)
import cv2
import time

cap = cv2.VideoCapture(0)

while True:
    start = time.perf_counter()
    ret, frame = cap.read()
    end = time.perf_counter()
    print("elapsed_time: {}[us]\n".format((end-start)*1000000))
    time.sleep(1)
