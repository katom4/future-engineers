# ここにコードを書いてね :-)
import hub
import time
import re

time.sleep(1)

print("--device init--")
while True:
    # motor init

    light_sensor = hub.port.A.device
    port_a = hub.port.A
    if light_sensor == None:
        continue
    light_sensor.mode(5)
    for mode in port_a.info()["modes"]:
        print(mode)
        print("\n")
    break
    while True
        time.sleep(2)
        print(light_sensor.get(2))

    while True:
        time.sleep(1)
        color_label = light_sensor.get(0)[0]
        #if color_label != None and color_label != 10:
        isblue = False
        isorange = False
        if(color_label != None):
            if(color_label <= 5):
                isblue = True
            elif(color_label <= 10 and color_label > 5):
                isorange = True
        print("color: ", end="")
        print(color_label)
        if(isblue):
            print("blue")
        if(isorange):
            print("orange")
        if(isblue == False and isorange == False):
            print(" ")
