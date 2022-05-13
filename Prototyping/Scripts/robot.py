from servo import Servo
from time import sleep
from math import acos, asin, atan, degrees, sin, cos, sqrt

class Robot:
    def __init__(self, servo1_pin, servo2_pin, servo3_pin, link1, link2, link3):
        self.servo1 = Servo(servo1_pin, 50)
        sleep(1)
        self.servo2 = Servo(servo2_pin, 50)
        sleep(1)
        self.servo3 = Servo(servo3_pin, 50)
        sleep(1)
        self.cur_pos = [0, 0, 0] # x, y, z
        self.link1 = link1
        self.link2 = link2
        self.link3 = link3


    def returnToOrigin(self):
        self.servo1.moveAngle(1)
        sleep(1)
        self.servo2.moveAngle(1)
        sleep(1)
        self.servo3.moveAngle(1)
        sleep(1) 


    def moveToPosition(self, x, y, z):
        # set current position to x, y, z
        self.cur_pos = (x, y, z)

        # compute angle for joint 1
        theta1 = degrees(atan(y/x))

        # compute angle for joint 2
        a = (x^2) + (y^2) + (z^2) - (self.link1^2 * self.link2^2)
        b = 2 * self.link1 * self.link2
        theta2 = degrees(acos(a/b ))

        # compute angle for joint 3
        r = sqrt( (x^2) + (y^2) + (z^2) )
        c = self.link2 * sin(theta2)
        d = self.link1 + (self.link2 * cos(theta2))
        theta3 = degrees(asin(z/r) + atan(c/d))

        # move robot to position x, y z
        self.servo1.moveAngle(theta1)
        sleep(1)
        self.servo2.moveAngle(theta2)
        sleep(1)
        self.servo3.moveAngle(theta3)
        sleep(1)

        # return to robot's original position
        self.returnToOrigin()
 