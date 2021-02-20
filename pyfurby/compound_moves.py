import board, digitalio, time, random
from typing import Optional

class FurbyCompound:
    """
    These are silly moves. Compound moves.
    """

    def ambulance(self, cycles: int = 50):
        for i in range(cycles):
            self.green_pin.value = True
            self.red_pin.value = False
            time.sleep(0.2)
            self.green_pin.value = False
            self.red_pin.value = True
            time.sleep(0.2)
        self.green_pin.value = False
        self.red_pin.value = False

    # Mixed ================================================================

    def bark(self):
        self.wait_until_bitten()
        self.red_pin.value = True
        self.say('woof')
        for i in range(20):
            self.green_pin.value = True
            self.red_pin.value = True
            time.sleep(0.05)
            self.green_pin.value = False
            self.red_pin.value = False
            time.sleep(0.05)
        self.complete_revolution()

    ## Motor based.

    def flutter(self, cycles: int=5):
        """
        Flutters eye lids

        :param cycles:
        :return:
        """
        self.set_percent_speed(70)
        for i in range(cycles):
            for action in (self.move_clockwise, self.move_counterclockwise):
                action()
                time.sleep(0.2)
                self.wait_until_revolution()
                time.sleep(0.2)
        self.halt()

    def fall_asleep(self):
        """
        Mimics falling asleep (does not shutdown)

        :return:
        """
        self.complete_revolution(70)
        self.halt()
        self.set_percent_speed(55)
        self.move_clockwise()
        time.sleep(5)
        self.halt()
        original_volume = self.volume
        original_rate = self.rate
        self.volume = 0.1
        self.rate = 50
        self.say('zed zed zed', move=False)
        time.sleep(1)
        self.say('zed zed zed', move=False)
        time.sleep(1)
        self.say('zed zed zed', move=False)
        self.volume = original_volume
        self.rate = original_rate

    def shut_eyes(self, quickly=False):
        self.complete_revolution(70)
        if quickly:
            speed = 100
            tock = 1.2
        else:
            speed = 70
            tock = 2
        self.set_percent_speed(speed)
        self.move_clockwise()
        time.sleep(tock)
        self.halt()

    def dance(self, speed:Optional[float]=None, cycles:int=10):
        """
        Moves randomly.

        :param speed:
        :param cycles:
        :return:
        """
        if speed:
            self.set_percent_speed(speed)
        self.complete_revolution()
        for i in range(cycles):
            tempo = random.random()
            self.move_counterclockwise()
            time.sleep(tempo)
            self.move_clockwise()
            time.sleep(tempo)
        self.halt()

    def blink(self, cycles:int=10):
        """
        Blinks. Inverse of flutter. Note that depending on power it may overshoot as it's the
        opposite side of the rotation pin.

        :param cycles:
        :return:
        """
        self.shut_eyes(quickly=True)
        self.set_percent_speed(100)
        for i in range(cycles):
            for action in (self.move_clockwise, self.move_counterclockwise):
                action()
                time.sleep(0.6)
        self.halt()