#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
ultrasonic_sensor = UltrasonicSensor(Port.S3)
color_sensor = ColorSensor(Port.S2)
arm_motor = Motor(Port.A)
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# Write your program here.
ev3.speaker.beep()


base_speed = 150
fast_speed = 500
pausetime = 5

ultrasonic_grade = 0


def beepGreen():
    right_motor.stop()
    left_motor.stop()
    ev3.speaker.beep(500,2000)
    right_motor.run(150)
    left_motor.run(-150)
    arm_motor.run(-200)
    wait(1000)
    arm_motor.run(0)

    right_motor.run(-900)
    left_motor.run(900)
    wait(500)
    right_motor.run(90)
    left_motor.run(-90)
    arm_motor.run(200)
    wait(1000)
    arm_motor.stop()

def beepBlue():
    right_motor.stop()
    left_motor.stop()
    ev3.speaker.beep(500,2000)
    wait(500)

    right_motor.run(270)
    left_motor.run(-270)
    wait(1000)



import time

garbage0 = 0
garbage1 = 0
garbage2 = 0
color_sensor.rgb()


# color mask

garbage = color_sensor.rgb()

# calibration
blueCalibration = [0, 0, 0]
offlineCalibration = [0, 0, 0]

ev3.screen.draw_text(1,1, "green tape")
wait(4000)
greenCalibration = color_sensor.rgb()
ev3.screen.clear()

ev3.screen.draw_text(1,1, "blue tape")
wait(4000)
blueCalibration = color_sensor.rgb()
ev3.screen.clear()

ev3.screen.draw_text(1,1, "table")
wait(4000)
offlineCalibration = color_sensor.rgb()
ev3.screen.clear()

ev3.screen.draw_text(1,1, "Place on line")
wait(3000)
ev3.screen.clear()


colornow = Color.BLACK

left_motor.run(base_speed)
right_motor.run(base_speed)

while True:


    colorValue = color_sensor.rgb()
    differenceGreen = tuple(abs(a - b) for a, b in zip(greenCalibration, colorValue))
    differenceBlue = tuple(abs(a - b) for a, b in zip(blueCalibration, colorValue))
    differenceTable = tuple(abs(a - b) for a, b in zip(offlineCalibration, colorValue))


    

    if all(diff < 20 for diff in differenceGreen):
        ev3.screen.clear()
        ev3.screen.draw_text(1,1, "green tape")
        colornow = Color.GREEN
        right_motor.run(-150)
        left_motor.run(fast_speed)
        wait(pausetime)

        if ultrasonic_sensor.distance(silent = False) <= 115:
                beepGreen()

    elif all(diff < 20 for diff in differenceBlue):
        ev3.screen.clear()
        ev3.screen.draw_text(1,1, "blue tape")
        colornow = Color.BLUE
        right_motor.run(-150)
        left_motor.run(fast_speed)
        wait(pausetime)

        if ultrasonic_sensor.distance(silent = False) <= 115:
            beepBlue()

    elif all(diff < 20 for diff in differenceTable):
        ev3.screen.clear()
        ev3.screen.draw_text(1,1, "offline")
        
        if colornow == Color.GREEN:
            left_motor.run(30)

        if colornow == Color.BLUE:
            left_motor.run(-30)

        right_motor.run(220)

        if ultrasonic_sensor.distance(silent = False) <= 115:
            
            if colornow == Color.GREEN:
                beepGreen()

            if colornow == Color.BLUE:
                beepBlue()


