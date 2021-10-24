import machine
import math
from machine import Pin


class RgbLed:
    chunkSize = 1024 / 255

    def __init__(self, rPin, gPin, bPin):
        self.rPin = self.__setPinPWM(rPin)
        self.gPin = self.__setPinPWM(gPin)
        self.bPin = self.__setPinPWM(bPin)

    def __setPinPWM(self, pinNumber):
        pin = Pin(pinNumber)
        pwmPin = machine.PWM(pin)
        pwmPin.freq(1000)
        return pwmPin

    def setColour(self, r, g, b):
        r = math.floor(1024 - (r * self.chunkSize))
        g = math.floor(1024 - (g * self.chunkSize))
        b = math.floor(1024 - (b * self.chunkSize))

        self.rPin.duty(r)
        self.gPin.duty(g)
        self.bPin.duty(b)
