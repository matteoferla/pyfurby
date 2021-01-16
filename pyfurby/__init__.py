"""
FurbyMotor adds motor control

SoundMotor controls motor by sound

"""

from .buttons import FurbyButtons
from .motor import FurbyMotor
from .talk import FurbyTalk
from .sound import FurbySound
from .gyro import FurbyGyro
from .test_moves import FurbyTests # more like silly actions

import time
from typing import Optional, Callable, Dict


class Furby(FurbyMotor, FurbyButtons, FurbyTalk, FurbySound, FurbyTests, FurbyGyro):

    def __init__(self,
                 pwma: int = 22,  # motor driver speed - white
                 stby: int = 4,  # motor driver on
                 ain1: int = 27, # motor driver forward
                 ain2: int = 17, # motor driver reverse
                 cycle: int = 21, # revolution button (pull-up input)
                 red: int = 14, # red LED (output)
                 green: int = 24, # green LED (output)
                 mouth: int = 18, # mouth button (pull-up input)
                 chest: int = 26, # chest button (pull-up input)
                 back: int = 16, # back button (pull-up input)
                 voice_name: str = 'en-scottish+m4', # espeak/pyttsx3
                 voice_volume: int = 0.7, # espeak/pyttsx3
                 voice_rate: int = 200): # espeak/pyttsx3
        FurbyMotor.__init__(self, pwma=pwma, stby=stby, ain1=ain1, ain2=ain2, cycle=cycle)
        FurbyButtons.__init__(self, red=red, green=green, mouth=mouth, chest=chest, back=back)
        FurbyTalk.__init__(self, voice_name=voice_name, voice_rate=voice_rate, voice_volume=voice_volume)
        FurbyGyro.__init__(self)
        # FurbySound and FurbyTests no init.

    def move_on_play(self):
        """
        This is for playing sound not via say/yell.
        :return:
        """
        while True:
            if self.playing:
                self.move_clockwise()
            else:
                self.halt()
            time.sleep(0.1)

    def say(self, text:str, move: bool=True):
        self.move_clockwise()
        super().say(text)
        self.halt()

    def yell(self, text):
        original_volume = self.volume
        original_speed = self.high_speed
        # max
        self.set_percent_speed(100)
        self.red_pin.value = True
        self.volume = 1.
        self.say(text)
        self.high_speed = original_speed
        self.volume = original_volume

    permitted_actions = ['lifted', 'moved', 'bitten', 'squeezed', 'aft_squeezed', 'fore_squeezed']

    def action_cycle(self, actions: Dict[str, Callable]):
        for trigger_name, action in actions.items():
            if trigger_name in self.permitted_actions and getattr(self, trigger_name):
                action()

    def loop_actions(self, actions: Dict[str, Callable]):
        while True:
            self.action_cycle(actions)
