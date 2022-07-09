# ここにコードを書いてね :-)
import hub
import time
import re
start = time.ticks_us()
#proces
end = time.ticks_us()
print("elapse_time: {}[ms]".format((end-start)/1000))
#hub.motion.preset_yaw(0)
print("--device init--")

while True:
    motor = hub.port.F.motor
    motor_steer = hub.port.E.motor

    ser = hub.port.D
    if ser==None or motor == None or motor_steer == None:
        print("Please check port!!")
        time.sleep(1)
        continue
    motor.mode(2)
    ser.mode(hub.port.MODE_FULL_DUPLEX)
    motor_steer.mode(2)
    time.sleep(2)
    ser.baud(115200)
    time.sleep(1)
    break
print("t")
def move(throttle, steer):
    # steerが0のとき、直進する
    if steer == 0:
        motor.run_at_speed(throttle)
        motor_steer.run_to_position(steer)
    # steerが0でないとき、角度steerだけ曲がる
    else:
        motor.run_at_speed(throttle)
        motor_steer.run_to_position(steer)


def stop():
    motor.brake()
    motor_steer.brake()

def resetSerialBuffer():
    while True:
        reply = ser.read(10000)
        print(reply)
        if reply == b"":
            break

def straightening():
    while True:
        difference_steer = int(-3*hub.motion.yaw_pitch_roll()[0])#steer's value difinition by hub.motion.position
        if (difference_steer < -100):
            difference_steer = -100
        elif (difference_steer > 100):
            difference_steer = 100
        check = 0
        steer_speed = abs(difference_steer)
        if (steer_speed > 40):
            steer_speed = 40
        if (steer_speed < 8):
            steer_speed = 8

        while(motor_steer.get(2)[0] <= difference_steer):
            motor_steer.run_at_speed(steer_speed)
            check = 1

        while(motor_steer.get(2)[0] > difference_steer):
            motor_steer.run_at_speed(-steer_speed)
            check = 1

        if (check == 1):
            print(motor_steer.get(2)[0] , difference_steer)
            check = 0

        if (motor_steer.get(2)[0] == 0) and (difference_steer == 0):
            motor_steer.run_to_position(0,speed = 5)
            motor_steer.brake
            break
if __name__ == "__main__":
    time.sleep(1)
    start = time.ticks_us()

    while True:
        reply = ser.read(10000)
        print(reply)
        if reply == b"":
            break

    end = time.ticks_us()
    print("elapse_time: {}[ms]".format((end-start)/1000))
    print("--waiting RasPi--")
    end_flag = False
    prev_steer = 0
    throttle = 0
    steer = 0
    count = 0

    while True:
        cmd = ""

        while True:
            reply = ser.read(4 - len(cmd))
            reply = reply.decode("utf-8")
            cmd = cmd + reply
            #send distance
            '''distance = dist_sensor.get(2)[0]
            time.sleep(1/1000)
            #print("Distance: {}[cm]".format(distance))
            #time.sleep(1)
            if distance:
                ser.write("{:3d}@".format(distance))
            else:
                ser.write("{:3d}@".format(0))'''
            if len(cmd) >= 4 and cmd[-1:] == "@":
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
                throttle = 20
                steer = 0
                if cmd_list[0].split(",")[0] == "1":# red
                    throttle = 20
                    steer = 120
                elif cmd_list[0].split(",")[1] == "1" :# green
                    throttle = 20
                    steer = -120

                print("throttle: {}, steer: {}".format(throttle, steer))
                break

        if steer ==0:
            motor.run_at_speed(20)
            straightening()
        else:
            move(throttle,steer)
        if steer != 0:
            resetSerialBuffer()
