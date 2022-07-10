# ここにコードを書いてね :-
import time
import math
import hub

print("--setup start--")
time.sleep(1)
while True:
    light_sensor = hub.port.A.device
    serial = hub.port.D
    motor_throttle = hub.port.F.motor
    motor_steering = hub.port.E.motor

    if (
        light_sensor == None
        or serial == None
        or motor_throttle == None
        or motor_steering == None
    ):
        continue

    serial.mode(hub.port.MODE_FULL_DUPLEX)
    light_sensor.mode(6)
    motor_steering.mode(3)
    motor_throttle.mode(2)

    time.sleep(1)
    serial.baud(115200)
    break

print("--setup finished--")

hub.motion.yaw_pitch_roll(0)
motor_steering.preset(0)
print("Set Yaw")
time.sleep(5)


def line_detect_light():
    is_blue = False
    is_orange = False
    blue_min = [253, 377, 542]
    blue_max = [916, 1015, 1008]

    orange_min = [0, 753, 731]
    orange_max = [1024, 920, 915]

    values = light_sensor.get(2)[0:3]
    print("values: {}".format(values))
    #time.sleep(30/1000)

    if sum(values) > 2700:
        return is_blue, is_orange
    if values[0] > 900:
        is_orange = True
        return is_blue, is_orange
    elif values[2] > 800:
        is_blue = True
        return is_blue, is_orange
    return is_blue, is_orange

speed = 10
#motor_throttle.run_at_speed(speed)
is_blue = False
is_orange = False

move_steering = 50

def line_detect():
    h = light_sensor.get(2)[0]
    s = light_sensor.get(2)[1]
    v = light_sensor.get(2)[2]
    #print(light_sensor.get(2)[0:3])
    #time.sleep(100/1000)
    if h > 340 or h < 10:
        print("orange")
        return "orange"
    elif s > 400:
        print("blue")
        return "blue"
    else:
        return ""


def flow_control():
    start = time.ticks_us()
    for i in range(1, 20):
        serial.write("req@req@".encode("utf-8"))
    print("--request send")

    avoid_red = 0
    avoid_green = 0
    cmd = ""
    start = time.ticks_us()

    while True:
        reply = serial.read(4 - len(cmd))
        reply = reply.decode("utf-8")
        cmd = cmd + reply

        if len(cmd) >= 4 and cmd[-1:] == "@":
            cmd_list = cmd.split("@")

            if len(cmd_list) != 2:
                print(cmd_list)
                continue

            #"end"を受け取ったとき、終了する
            if cmd_list[0] == "q":
                motor_stop()
                print("--end")

            is_red = int(cmd_list[0].split(",")[0])
            is_green = int(cmd_list[0].split(",")[1])
            cmd = "{},{}@".format(avoid_red, avoid_green)
            print("recieve: {}".format(cmd))
            break

    reset_input_buffer()
    end = time.ticks_us()
    #print("elapsed_time: {}".format(end-start))
    return is_red, is_green

def reset_input_buffer():

    reply = serial.read(10000)
    while reply != b"":
        reply = serial.read(10000)
    #print("--reset completed--")

def move_paralell():
    while abs(hub.motion.yaw_pitch_roll()[0])>2:
        yaw = hub.motion.yaw_pitch_roll()[0]
        coef = -1*math.sin(math.radians(yaw))
        while True:
            if motor_steering.busy(type=1):
                continue #何かしらのモータコマンドを実行しているなら戻る．
            elif yaw != 0:
                motor_steering.run_to_position(coef*move_steering*4, 100, 100, 0)
            break

def avoid_sign(avoid_steering, color):

    hub.motion.yaw_pitch_roll(-1*avoid_steering)
    start = time.ticks_us()
    while True:
        #start_r = time.ticks_us()
        reset_input_buffer()
        #end_r = time.ticks_us()
        #print("elapsed_time: {}".format(end_r-start_r))
        is_red, is_green = cmd_read()
        move_paralell()
        print("--direction changed--")

        end = time.ticks_us()
        elapsed_time = (end - start)/1000 #[ms]
        if color=="red" and elapsed_time > 0:
            if not is_red:
                print("--passed red sign--")
                break
        if color=="green" and elapsed_time > 0:
            if not is_green:
                print("--passed green sign--")
                break

    # correct steering to paralell against the wall
    hub.motion.yaw_pitch_roll(avoid_steering)
    move_paralell()
    print("--avoid finished--")


def motor_stop():
    motor_steering.brake()
    motor_throttle.brake()

def cmd_read():
    is_red = 0
    is_green = 0
    cmd = ""
    reply = serial.read(4 - len(cmd))
    reply = reply.decode("utf-8")
    cmd = cmd + reply

    if len(cmd) >= 4 and cmd[-1:] == "@":
        cmd_list = cmd.split("@")

        #"end"を受け取ったとき、終了する
        if cmd_list[0] == "q":
            motor_stop()
            print("--end")
        is_red = int(cmd_list[0].split(",")[0])
        is_green = int(cmd_list[0].split(",")[1])
        cmd = "{},{}@".format(is_red, is_green)
        #print("recieve: {}".format(cmd))

    return is_red, is_green

def main():
    motor_throttle.run_at_speed(30)
    print("--waiting raspi")
    while True:
        line =""

        #start = time.ticks_us()
        reset_input_buffer()
        is_red, is_green = cmd_read()
        line = line_detect()
        if line == "blue":
            hub.motion.yaw_pitch_roll(90)
            move_paralell()
        if is_red:
            print("--detcted red sign--")
            avoid_sign(30 ,color="red")
        if is_green:
            print("--detected green sign--")
            avoid_sign(-30, color="green")

    #end = time.ticks_us()
main()
    #print("elapsed_time: {}".format(end-start))
    #time.sleep(50/1000)













