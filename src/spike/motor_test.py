# created by UNO
import hub
import time
import re

hub.motion.preset_yaw(0)

print("--device init--")
while True:
    motor = hub.port.C.motor
    motor_steer = hub.port.E.motor

    ser = hub.port.D

    if ser==None or motor == None or motor_steer == None:
        continue
    motor.mode(2)
    ser.mode(hub.port.MODE_FULL_DUPLEX)
    motor_steer.mode(2)
    time.sleep(2)
    ser.baud(115200)
    time.sleep(1)
    break
"""
def move(throttle, steer):
    motor.run_to_position(1,1)
"""
def stop():
    motor.brake()
    motor_steer.brake()

motor_steer.preset(0)# steer_motor run_to_position value reset

motor.run_for_degrees(720, 20)
while(motor_steer.get(2)[0] < 20):
    motor_steer.run_at_speed(10)

motor.run_for_degrees(720, 20)

while(motor_steer.get(2)[0] > -20):
    motor_steer.run_at_speed(-20)

motor.run_for_degrees(720,20)

while(motor_steer.get(2)[0] < 0):
    motor_steer.run_at_speed(20)

motor.brake()
motor_steer.brake()
print("ok2")

"""
if __name__ == "__main__":
    #シリアルポートに残っているデータを空にする
    motor_steer.run_to_position(0,10)
    time.sleep(3)
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
                #print("Steer: {}".format(steer))


            break
        move(throttle, steer)
        #"end"を受け取ったとき、停止して終了する
        if end_flag:
            stop()
            break
"""
