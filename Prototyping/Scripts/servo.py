import RPi.GPIO as GPIO
from time import sleep

class Servo:
    def __init__(self, gpio_pin=26, frequency=50):
        self.gpio_pin = gpio_pin
        self.frequency = frequency
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.gpio_pin, GPIO.OUT)
            self.pwm = GPIO.PWM(self.gpio_pin, self.frequency)
            self.pwm.start(0)
            print(f'Servo at [GPIO pin {gpio_pin}] setup successfully')
        except Exception as e:
            print(f'ERROR: Servo setup unsuccessful - {e}')

    # Setters
    def setGpioPin(self, gpio_pin=26):
        self.gpio_pin = gpio_pin

    def setFrequency(self, frequency=50):
        self.frequency = frequency

    # Getters
    def getGpioPin(self):
        return self.gpio_pin

    def getFrequency(self):
        return self.frequency

    # Move sevrvo to a position
    def moveAngle(self, angle=0):
        if(angle<0 or angle>180):
            print('WARNING:Invalid angle. 0 <= angle <= 180 degrees\n')
        else:
            duty_cycle = (angle/20) + 2.5
            print(f'Moving to: Angle - {angle}   Duty Cycle - {duty_cycle}')
            GPIO.output(self.gpio_pin, True)
            self.pwm.ChangeDutyCycle(duty_cycle)
            sleep(1)
            GPIO.output(self.gpio_pin, False)
            self.pwm.ChangeDutyCycle(0)
            return angle