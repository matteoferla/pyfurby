#!/usr/bin/env python

import digitalio, board, pulseio
from typing import Optional

class FurbyMotor:
    """
    TB6612 motor driver and sensor to control cycles (pull-up)
    """
    high_speed = 0xffff

    def __init__(self, pwma: int = 7, stby: int = 13, ain1: int = 16, ain2: int = 11, cycle: int = 21):
        # standby: H-bridges to work when high
        self.standby_pin = digitalio.DigitalInOut(digitalio.Pin(stby))
        self.standby_pin.switch_to_output(False)
        # direction 1
        self.ain1_pin = digitalio.DigitalInOut(digitalio.Pin(ain1))
        self.ain1_pin.switch_to_output(False)
        # direction 2
        self.ain2_pin = digitalio.DigitalInOut(digitalio.Pin(ain2))
        self.ain2_pin.switch_to_output(False)
        # pwma
        self.pwm_pin = pulseio.PWMOut(pin=digitalio.Pin(pwma),
                                      duty_cycle=0,
                                      frequency=100)
        # cycle pin
        self.cycle_pin = digitalio.DigitalInOut(digitalio.Pin(cycle))
        self.cycle_pin.switch_to_input(pull=digitalio.Pull.UP)

    def move_clockwise(self):
        self.standby_pin.value = True
        self.pwm_pin.duty_cycle = self.high_speed
        self.ain1_pin.value = True
        self.ain2_pin.value = False

    def move_counterclockwise(self):
        self.standby_pin.value = True
        self.pwm_pin.duty_cycle = self.high_speed
        self.ain1_pin.value = False
        self.ain2_pin.value = True

    def halt(self):
        self.standby_pin.value = False
        self.pwm_pin.duty_cycle = 0
        self.ain1_pin.value = False
        self.ain2_pin.value = False

    def set_percent_speed(self, speed: int):
        self.high_speed = int(speed/100 * 0xffff)
        if self.ain1_pin.value or self.ain2_pin.value:
            self.pwm_pin.duty_cycle = self.high_speed

    def wait_until_revolution(self):
        while self.cycle_pin.value:
            pass

    def complete_revolution(self, speed: Optional[int]=None):
        if speed:
            self.set_percent_speed(speed)
        self.move_counterclockwise()
        self.wait_until_revolution()
