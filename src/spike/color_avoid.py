# ここにコードを書いてね :-)
import hub
import time
import re

time.sleep(1)


print("--device init--")
while True:
    # motor init
    l_motor = hub.port.F.motor
    motor_steer = hub.port.E.motor

    ser = hub.port.D

    if ser == None or l_motor == None or motor_steer == None:
        continue
    ser.mode(hub.port.MODE_FULL_DUPLEX)
    motor_pair = l_motor.pair(hub.port.B.motor)
    print(motor_pair)
    time.sleep(2)
    ser.baud(115200)
    time.sleep(1)
    break

def move(throttle, steer):
    # steerが0のとき、直進する
    if steer == 0:
        motor_pair.run_at_speed(-throttle, throttle)
        motor_steer.run_to_position(steer)
    # steerが0でないとき、角度steerだけ曲がる
    else:
        motor_pair.run_at_speed(-throttle, throttle)
        motor_steer.run_to_position(steer)
        return steer

def stop():
    motor_pair.brake()
    motor_steer.brake()


if __name__ == "__main__":
    #シリアルポートに残っているデータを空にする
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

    while True:
        cmd = ""

        while True:
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

        #"end"を受け取ったとき、停止して終了する
        if end_flag:
            stop()
            break
