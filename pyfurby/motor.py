#!/usr/bin/env python

import digitalio, board, pulseio
from typing import Optional

class FurbyMotor:
    """
    TB6612 motor driver and sensor to control cycles (pull-up)
    """
    high_speed = 0xffff

    def __init__(self, pwma: int, stby: int, ain1: int, ain2: int, cycle: int):
        # standby: H-bridges to work when high
        self.standby_pin = digitalio.DigitalInOut(digitalio.Pin(stby))  #: standy pin for TB6612
        self.standby_pin.switch_to_output(False)
        # direction 1
        self.ain1_pin = digitalio.DigitalInOut(digitalio.Pin(ain1))   #: Ain1 pin for TB6612
        self.ain1_pin.switch_to_output(False)
        # direction 2
        self.ain2_pin = digitalio.DigitalInOut(digitalio.Pin(ain2))     #: Ain2 pin for TB6612
        self.ain2_pin.switch_to_output(False)
        # pwma
        self.pwm_pin = pulseio.PWMOut(pin=digitalio.Pin(pwma),
                                      duty_cycle=0,
                                      frequency=100)     #: pwm pin for TB6612
        # cycle pin
        self.cycle_pin = digitalio.DigitalInOut(digitalio.Pin(cycle))  #: is the cycle complete trigger pin (back of furby)
        self.cycle_pin.switch_to_input(pull=digitalio.Pull.UP)

    def move_clockwise(self):
        """
        Start moving fubry clockwise.
        """
        self.standby_pin.value = True
        self.pwm_pin.duty_cycle = self.high_speed
        self.ain1_pin.value = True
        self.ain2_pin.value = False

    def move_counterclockwise(self):
        """
        Start moving fubry counter-clockwise.
        """
        self.standby_pin.value = True
        self.pwm_pin.duty_cycle = self.high_speed
        self.ain1_pin.value = False
        self.ain2_pin.value = True

    def halt(self):
        """
        Stop motion.
        """
        self.standby_pin.value = False
        self.pwm_pin.duty_cycle = 0
        self.ain1_pin.value = False
        self.ain2_pin.value = False

    def inverse(self):
        if self.ain1_pin.value:
            self.move_counterclockwise()
        elif self.ain2_pin.value:
            self.move_clockwise()
        else: # halted
            pass

    def get_percent_speed(self):
        return self.high_speed * 100 / 0xffff

    def set_percent_speed(self, speed: int):
        """
        Will convert to high_speed hex (``0xffff``)
        :param speed: speed of motor as %.
        :return:
        """
        self.high_speed = int(speed/100 * 0xffff)
        if self.ain1_pin.value or self.ain2_pin.value:
            self.pwm_pin.duty_cycle = self.high_speed

    percent_speed = property(get_percent_speed, set_percent_speed)

    def wait_until_revolution(self):
        """
        Idle until the motors complete a revolution/cycle (back trigger)
        """
        while self.cycle_pin.value:
            pass

    def complete_revolution(self, speed: Optional[int]=None):
        """
        Move and wait until the motors complete a revolution/cycle
        :param speed:
        :return:
        """
        if speed:
            self.set_percent_speed(speed)
        self.move_counterclockwise()
        self.wait_until_revolution()
        self.halt()
