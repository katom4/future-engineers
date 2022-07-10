# ここにコードを書いてね :-)
import hub
import time
import re

time.sleep(1)

print("--device init--")
while True:
    # motor init
    motor = hub.port.F.motor
    motor_steer = hub.port.E.motor


    ser = hub.port.D

    if ser==None or motor == None or motor_steer == None :
        continue
    ser.mode(hub.port.MODE_FULL_DUPLEX)
    motor_steer.mode(2)
    time.sleep(2)
    ser.baud(115200)
    time.sleep(1)
    break

def move(throttle, steer):
    while True:
        if steer >= 0:
            if motor_steer.get(2)[0] < steer:
                #print(motor_steer.get(2)[0],steer)
                #time.sleep(0.1)
                motor.run_at_speed(-throttle)
                motor_steer.run_at_speed(30)
            else:
                break
        elif steer < 0:
            if motor_steer.get(2)[0] > steer:
                #time.sleep(0.1)
                motor.run_at_speed(-throttle)
                motor_steer.run_at_speed(-30)
            else:
                break


def stop():
    motor.brake()
    motor_steer.brake()


if __name__ == "__main__":
    #シリアルポートに残っているデータを空にする
    motor_steer.run_to_position(0,10)
    time.sleep(10)
    while True:
        reply = ser.read(10000)
        print(reply)
        if reply == b"":
            break

    print("--waiting RasPi--")
    end_flag = False
    prev_steer = 0
    throttle = 0
    steer = 0
    flag = False

    while True:
        cmd = ""

        while True:
            #receive operations(throttle, steer)
            reply = ser.read(8 - len(cmd))
            reply = reply.decode("utf-8")
            cmd = cmd + reply

            if len(cmd) >= 8 and cmd[-1:] == "@":
                cmd_list = cmd.split("@")
                if len(cmd_list) != 2:
                    print(len(cmd_list))
                    cmd = ""
                    continue

                #"end"を受け取ったとき、終了する
                if cmd_list[0] == "end":
                    print(" -- end")
                    end_flag = True
                    break

                throttle = int(cmd_list[0].split(",")[0])
                steer = int(cmd_list[0].split(",")[1])
                print(steer)
                break
            move(throttle, steer)


            #send distance
            time.sleep(100/1000)
            #print("Distance: {}[cm]".format(distance))
            #time.sleep(1)
            if distance:
                ser.write("{:3d}@".format(distance))
            else:
                ser.write("{:3d}@".format(0))

            break
        move(throttle, steer)
        #"end"を受け取ったとき、停止して終了する
        if end_flag:
            stop()
            break
