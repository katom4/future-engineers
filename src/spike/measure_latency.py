
import time
import hub

print("--setup start--")
time.sleep(1)
while True:
    distance_sensor = hub.port.B.device
    light_sensor = hub.port.A.device
    serial = hub.port.D
    motor_throttle = hub.port.F.motor
    motor_steering = hub.port.E.motor

    if distance_sensor == None or light_sensor == None or serial == None or motor_throttle == None or motor_steering == None:
        continue

    serial.mode(hub.port.MODE_FULL_DUPLEX)
    light_sensor.mode(5)
    motor_steering.mode(3)
    motor_throttle.mode(2)

    time.sleep(1)
    serial.baud(115200)
    break

print("--setup finished--")

hub.motion.yaw_pitch_roll(0)
motor_steering.preset(0)

#motor_throttle.run_at_speed(10)

while True:
    start = time.ticks_us()

    #distance = distance_sensor.get()[0]
    #yaw = hub.motion.yaw_pitch_roll()[0]
    #color = light_sensor.get(2)

    #reply = serial.read(8)
    #code = "hello world".encode("utf-8")
    #serial.write(code)

    #moving_distance = motor_throttle.get(2)[0]
    #steering_position = motor_steering.get(2)[0]

    end = time.ticks_us()
    print("elapsed_time: {}[us]".format(end-start))
    #print("distance: {}[cm]".format(distance))
    #print("yaw: {}".format(yaw))
    #print("color: {}".format(color))

    #print("moving_distance: {}".format(moving_distance))
    #print("steering_position: {}".format(steering_position))

    time.sleep(1000/1000)
