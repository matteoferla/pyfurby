import board, digitalio, time


class FurbyButtons:
    """
    There are a few buttons. All configured as pull-ups
    """

    def __init__(self, red: int, green: int, mouth: int, chest: int, back: int):
        # LEDs
        self.red_pin = digitalio.DigitalInOut(digitalio.Pin(red))  #: red pin LED
        self.green_pin = digitalio.DigitalInOut(digitalio.Pin(green)) #: green pin LED
        for color_pin in (self.red_pin, self.green_pin):
            color_pin.switch_to_output(False)
        # buttons
        self.mouth_pin = digitalio.DigitalInOut(digitalio.Pin(mouth))  #: mouth pin trigger "bitten"
        self.chest_pin = digitalio.DigitalInOut(digitalio.Pin(chest))  #: chest pin trigger: "fore_squeezed"/"squeezed"
        self.back_pin = digitalio.DigitalInOut(digitalio.Pin(back))  #: back pin trigger: "aft_squeezed"/"squeezed"
        for button_pin in (self.mouth_pin, self.chest_pin, self.back_pin):
            button_pin.switch_to_input(pull=digitalio.Pull.UP)

    @property
    def bitten(self) -> bool:
        """
        True when self.mouth_pin.value is not 1

        :return: is the furby mouth pressed?
        """
        return not self.mouth_pin.value

    @property
    def fore_squeezed(self) -> bool:
        """
        True when self.chest_pin.value is not 1

        :return: is the furby chest squeezed?
        """
        return not self.chest_pin.value

    @property
    def aft_squeezed(self) -> bool:
        """
        True when self.back_pin.value is not 1

        :return: is the furby back squeezed?
        """
        return not self.back_pin.value

    @property
    def squeezed(self) -> bool:
        """
        True when self.chest_pin.value or self.back_pin.value is not 1

        :return: is the furby chest or back squeezed?
        """
        return self.fore_squeezed or self.aft_squeezed

    # === Waits ==============================

    def wait_until_squeezed(self):
        """
        Hold until the furby is squeezed
        """
        while not self.squeezed:
            pass

    def wait_until_bitten(self):
        """
        Hold until the furby has its mouth pressed
        """
        while not self.bitten:
            pass
