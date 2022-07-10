# check gyro_sensor
import hub
import time

#Reset yaw angle to 0.
hub.motion.yaw_pitch_roll(0)

print("--device init--")
while True:
    ser = hub.port.D

    if ser == None:
        continue
    ser.mode(hub.port.MODE_FULL_DUPLEX)
    time.sleep(2)
    ser.baud(115200)
    time.sleep(1)
    break

while True:
    yaw_angle, _, _ = hub.motion.yaw_pitch_roll()
    print("yaw: {}".format(yaw_angle))
    ser.write("{:3d}@".format(yaw_angle))
    time.sleep(30/1000)
    break








