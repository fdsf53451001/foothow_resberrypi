# -*- coding:utf-8 -*-
import smbus
import RPi.GPIO as GPIO
from mlx90614 import MLX90614

import time
from random import shuffle

#outside, inside
angle = [
    (135,81),
    (122,75),
    (36,91),
    (131,78),
    (42,94),
    (24,105),
    (52,95),
    (147,67)
]

# setup thermo
temp1_address = 0x5a
thermo1 = MLX90614(temp1_address)

# setup servo motor
GPIO.setmode(GPIO.BCM)
servo1_pin = 12     # 外側
servo2_pin = 13     # 內側
servo3_pin = 18     # 微絲
GPIO.setup(servo1_pin, GPIO.OUT)
GPIO.setup(servo2_pin, GPIO.OUT)
GPIO.setup(servo3_pin, GPIO.OUT)
motor1 = GPIO.PWM(servo1_pin, 50) # PWM with 50Hz
motor2 = GPIO.PWM(servo2_pin, 50) # PWM with 50Hz
motor3 = GPIO.PWM(servo3_pin, 50) # PWM with 50Hz
motor1.start(1) # Initialization
motor2.start(1)
motor3.start(1)

def get_temp(thermo,address):
    try:
        return thermo.get_obj_temp()
    except IOError as e:
        print('temp sensor error!')
        return -1

def move_motor_with_angle(motor,angle):
    # dutycycle = ((angle/180.0) + 1.0) * 5.0
    dutycycle = 4.3+(angle/180.0) * 5.0
    motor.ChangeDutyCycle(dutycycle)
    time.sleep(0.5)

def move_motor(motor,value):
    motor.ChangeDutyCycle(value)
    time.sleep(0.5)

def set_silk(status):
    if not status:
        move_motor_with_angle(motor3,70)
    else:
        move_motor_with_angle(motor3,90)

def get_random_order():
    order = [0,1,2,3,4,5,6,7]
    shuffle(order)
    return order

if __name__ == '__main__':
    temp1 = get_temp(thermo1,temp1_address)
    print(temp1)

    while True:
        #init
        move_motor_with_angle(motor1,87)
        move_motor_with_angle(motor2,87)
        time.sleep(2)

        for index in get_random_order():
            move_motor_with_angle(motor1,angle[index][0])
            move_motor_with_angle(motor2,angle[index][1])
            set_silk(1)
            time.sleep(2)
            set_silk(0)

        # move_motor_with_angle(motor1,135)
        # move_motor_with_angle(motor2,81)
        # time.sleep(2)

        # move_motor(motor2,7)
        # time.sleep(1)
        # move_motor(motor2,7.5)
        # time.sleep(1)



    