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

    light_sensor = hub.port.A.device

    ser = hub.port.D
    if ser==None or motor == None or motor_steer == None or light_sensor == None:
        print("Please check port!!")
        time.sleep(1)
        continue
    motor.mode(2)
    ser.mode(hub.port.MODE_FULL_DUPLEX)
    motor_steer.mode(2)

    light_sensor.mode(5)

    time.sleep(2)
    ser.baud(115200)
    time.sleep(1)
    break

def move(throttle, steer):
    # steerが0のとき、直進する
    if steer == 0:
        motor.run_at_speed(throttle)
        motor_steer.run_to_position(steer)
    # steerが0でないとき、角度steerだけ曲がる
    else:
        motor.run_at_speed(throttle)
        motor_steer.run_to_position(steer)

#move関数をbusyを用いた制御にするテスト
#そもそものmove関数が動いていたのはmain関数の遅延のおかげ？
def move2(throttle, steer):
    # steerが0のとき、直進する
    while True:
        if(motor_steer.busy(type=1)):
            continue
        if steer == 0:
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
        difference_steer = int(-4*hub.motion.yaw_pitch_roll()[0]) #steer's value difinition by hub.motion.position
        if (difference_steer < -110):
            difference_steer = -110
        elif (difference_steer > 110):
            difference_steer = 110

        check = 0
        steer_speed = abs(difference_steer)
        if (steer_speed > 40):
            steer_speed = 40
        if (steer_speed < 8):
            steer_speed = 8
        
        if(motor_steer.busy(type=1)): #if motor_steer is moving
            continue
        else:
            motor_steer.run_to_position(difference_steer)
        

        if (motor_steer.get(2)[0] == 0):
            motor_steer.run_to_position(0)
            motor_steer.brake
            break

#straighteningを、ループにせず行うテスト
#標識の検出などに対応することを目的としている
#main関数の中のフラグで制御する
def straightening2():
    once = False
    while True:
        difference_steer = int(-4*hub.motion.yaw_pitch_roll()[0]) #steer's value difinition by hub.motion.position
        if (difference_steer < -110):
            difference_steer = -110
        elif (difference_steer > 110):
            difference_steer = 110

        check = 0
        steer_speed = abs(difference_steer)
        if (steer_speed > 40):
            steer_speed = 40
        if (steer_speed < 8):
            steer_speed = 8
        
        if(motor_steer.busy(type=1)): #if motor_steer is moving
            continue
        elif once: #最初は弾かれてrun_to_positionが実行される。その後、busyがfalseになるまで実行され、trueになったらwhile文を抜ける
            break
        else:
            motor_steer.run_to_position(difference_steer)
            once = True
        

        """if (motor_steer.get(2)[0] == 0):
            motor_steer.run_to_position(0)
            motor_steer.brake
            break"""

#光センサで青色検出のhsv値バージョン（modeの設定と閾値は要検証）
def detectBlue(h,s,v):
    if(h > 90 and h < 270 and s > 256 and s < 1023 and v >= 0 and v <= 1024):
        return True
    else:
        return False


#光センサの値取得（hsv）を簡単にする関数
def getLightsensor_hsv():
    h = light_sensor.get(2)[0]
    s = light_sensor.get(2)[1]
    v = light_sensor.get(2)[2]
    return h,s,v
    
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

    isFinishcurve = True

    while True:
        cmd = ""

        while True:
            reply = ser.read(4 - len(cmd))
            reply = reply.decode("utf-8")
            cmd = cmd + reply
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
                h,s,v = getLightsensor_hsv()

                if cmd_list[0].split(",")[0] == "1":# red
                    throttle = 20
                    steer = 120
                elif cmd_list[0].split(",")[1] == "1" :# green
                    throttle = 20
                    steer = -120
                elif detectBlue(h,s,v) and isFinishcurve: #青色の検出、1回だけでいいので、フラグを追加
                    hub.motion.yaw_pitch_roll(90)
                    isFinishcurve = False
                elif False: #オレンジ色の検出
                    hub.motion.yaw_pitch_roll(-90)

                print("throttle: {}, steer: {}".format(throttle, steer))
                break
        if steer ==0:
            motor.run_at_speed(20)
            straightening()
        else:
            move(throttle,steer)
        
        
        if int(-4*hub.motion.yaw_pitch_roll()[0]) == 0: #ジャイロセンサが0のとき、車体は曲がりきっている
            isFinishcurve = True
        
        if steer != 0:
            resetSerialBuffer()
