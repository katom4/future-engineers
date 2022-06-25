# check gyro_sensor
import hub
import time

#Reset yaw angle to 0.
hub.motion.yaw_pitch_roll(0)

while True:
    yaw_angle, pitch_angle, roll_angle = hub.motion.yaw_pitch_roll()
    print("yaw: {}, pitch: {}, roll: {}".format(yaw_angle, pitch_angle, roll_angle))
    time.sleep(30/1000)





