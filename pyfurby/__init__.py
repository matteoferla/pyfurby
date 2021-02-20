"""
FurbyMotor adds motor control

SoundMotor controls motor by sound

"""

from .buttons import FurbyButtons
from .motor import FurbyMotor
from .talk import FurbyTalk
from .sound import FurbySound
from .gyro import FurbyGyro
from .restless import RestlessFurby
from .background import BackFurby
from .compound_moves import FurbyCompound  # more like silly actions
from .temporary import TemporaryValue
from .tests import TestFurby

import time
from typing import Optional, Callable, Dict


class Furby(FurbyMotor,
            FurbyButtons,
            FurbyTalk,
            BackFurby,
            FurbySound,
            FurbyCompound,
            FurbyGyro,
            RestlessFurby,
            TestFurby):
    """
    Control a Furby with Python and a pi!

    :ivar acceleration: gyroscope
    :vartype acceleration: dict
    :ivar aft_squeezed: is the back squeezed?
    :vartype aft_squeezed: bool
    :ivar ain1_pin: H-bridge for motor
    :vartype ain1_pin: DigitalInOut
    :ivar ain2_pin: H-bridge for motor
    :vartype ain2_pin: DigitalInOut
    :ivar back_pin: back button (input digitalio.Pull.UP)
    :vartype back_pin: DigitalInOut
    :ivar bitten: is it bitting down?
    :vartype bitten: bool
    :ivar chest_pin: chest button (input digitalio.Pull.UP)
    :vartype chest_pin: DigitalInOut
    :ivar cycle_pin: cycle button (input digitalio.Pull.UP)
    :vartype cycle_pin: DigitalInOut
    :ivar engine: espeak engine
    :vartype engine: Engine
    :ivar fore_squeezed: is back squeezed?
    :vartype fore_squeezed: bool
    :ivar green_pin: forehead green
    :vartype green_pin: DigitalInOut
    :ivar gyro: The gyroscope obkect
    :vartype gyro: mpu6050
    :ivar high_speed: hex value. See percent_speed
    :vartype high_speed: int
    :ivar lifted:
    :vartype lifted: bool
    :ivar mouth_pin:
    :vartype mouth_pin: DigitalInOut
    :ivar moved:
    :vartype moved: bool
    :ivar permitted_actions:
    :vartype permitted_actions: list
    :ivar playing:
    :vartype playing: bool
    :ivar pwm_pin:
    :vartype pwm_pin: PWMOut
    :ivar rate:
    :vartype rate: int
    :ivar red_pin:
    :vartype red_pin: DigitalInOut
    :ivar resting_x:
    :vartype resting_x: float
    :ivar resting_y:
    :vartype resting_y: float
    :ivar resting_z:
    :vartype resting_z: float
    :ivar soundcard_status_file:
    :vartype soundcard_status_file: str
    :ivar speed:
    :vartype speed: dict
    :ivar squeezed:
    :vartype squeezed: bool
    :ivar standby_pin:
    :vartype standby_pin: DigitalInOut
    :ivar temperature:
    :vartype temperature: float
    :ivar volume:
    :vartype volume: float
    """

    def __init__(self,
                 pwma: int = 22,  # motor driver speed - white
                 stby: int = 4,  # motor driver on
                 ain1: int = 27,  # motor driver forward
                 ain2: int = 17,  # motor driver reverse
                 cycle: int = 12,  # revolution button (pull-up input)
                 red: int = 14,  # red LED (output)
                 green: int = 24,  # green LED (output)
                 mouth: int = 15,  # mouth button (pull-up input)
                 chest: int = 16,  # chest button (pull-up input)
                 back: int = 26,  # back button (pull-up input)
                 voice_name: str = 'en-scottish+m4',  # espeak/pyttsx3
                 voice_volume: int = 0.7,  # espeak/pyttsx3
                 voice_rate: int = 200):  # espeak/pyttsx3
        FurbyMotor.__init__(self, pwma=pwma, stby=stby, ain1=ain1, ain2=ain2, cycle=cycle)
        FurbyButtons.__init__(self, red=red, green=green, mouth=mouth, chest=chest, back=back)
        FurbyTalk.__init__(self, voice_name=voice_name, voice_rate=voice_rate, voice_volume=voice_volume)
        FurbyGyro.__init__(self)
        # FurbySound, BackFurby and FurbyTests no init.
        TemporaryValue.furby = self
        self.use_temporarily = TemporaryValue

    def move_on_play(self):
        """
        This is for playing sound -not via say/yell.

        Holds forever.
        """
        while True:
            if self.playing:
                self.move_clockwise()
            else:
                self.halt()
            time.sleep(0.1)

    def say(self, text: str, move: bool = True):
        """
        convert the ``text`` to speech and play it.

        * To say in a different language change ``voice_name``
        * To say in a different volume change ``voice_volume`` (0-1)
        * To say in a different rate change ``voice_rate` (200 is default).

        :param text: text to say
        :param move: move while talking
        :return:
        """
        if move:
            self.move_clockwise()
            for phrase in text.replace(',','.').split('.'):
                super().say(phrase)
                self.inverse()
                time.sleep(0.1)
            self.halt()
        else:
            super().say(text)

    def yell(self, text):
        """
        ``say`` but at full volume.
        With red led for drama.

        :param text:
        :return:
        """
        original_volume = self.volume
        original_speed = self.high_speed
        # max
        self.set_percent_speed(100)
        self.red_pin.value = True
        self.volume = 1.
        self.say(text)
        self.high_speed = original_speed
        self.volume = original_volume
        self.red_pin.value = False

    permitted_actions = ['lifted', 'moved', 'bitten', 'squeezed', 'aft_squeezed', 'fore_squeezed']

    def action_cycle(self, actions: Dict[str, Callable]):
        """
        This runs a single cycle
        Given a dictionary of actions, where the key is an trigger (past particle, e.g. ``bitten``)
        and vale is a function to be called if the trigger is true.

        :param actions: dictionary of trigger name --> action function to call
        :return:
        """
        for trigger_name, action in actions.items():
            if trigger_name in self.permitted_actions and getattr(self, trigger_name):
                action()

    def loop_actions(self, actions: Dict[str, Callable]):
        """
        Runs on loop the method ``action_cycle``.
        Namely, given a dictionary of actions, where the key is an trigger (past particle, e.g. ``bitten``)
        and vale is a function to be called if the trigger is true.

        :param actions: dictionary of trigger name --> action function to call
        :return:
        """
        while True:
            self.action_cycle(actions)
