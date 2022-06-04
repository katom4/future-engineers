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


# prev_steerで直前にどう動いていたかを受け取り、右（もしくは左） に動いていた場合に逆に動いて進行方向を修正する
# prev_steer=0: 通常通りの動作 prev_steer!=0: time秒だけに-steerで動く


def move(throttle, steer, prev_steer):
    time = 1000
    # steer を反時計回り（左に曲がる）させたいとき、ステアリングモータのスピードを負にする必要がある
    if not prev_steer:
        if not steer:
            motor_pair.run_at_speed(-throttle, throttle)
            motor_steer.run_to_position(0)
            return 0
        else:
            motor_pair.run_at_speed(-throttle, throttle)
            motor_steer.run_for_time(time, steer)
            return steer
    else:
        motor_pair.run_at_speed(-throttle, throttle)
        motor_steer.run_for_time(time, -prev_steer)
        return 0


def stop():
    motor_pair.brake()
    motor_steer.brake()


if __name__ == "__main__":
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
            # time.sleep(100/1000)

            if len(cmd) >= 8 and cmd[-1:] == "@":
                cmd_list = cmd.split("@")
                if len(cmd_list) != 2:
                    print(len(cmd_list))
                    cmd = ""
                    continue

                if cmd_list[0] == "end":
                    print(" -- end")
                    end_flag = True
                    break

                throttle = int(cmd_list[0].split(",")[0])
                steer = int(cmd_list[0].split(",")[1])
                print(steer)
                break

        prev_steer = move(throttle, steer, prev_steer)
        # break

        if end_flag:
            stop()
            break
