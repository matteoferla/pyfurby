class TestFurby:
    def tests(self):
        """
        Run diagnostic tests. requires human action.
        :return:
        """
        for button_name, trigger_name in [('mouth', 'bitten'),
                                          ('chest', 'fore_squeezed'),
                                          ('back', 'aft_squeezed')]:
            if getattr(self, trigger_name):
                self.say(f'Error, {button_name} button is reported pressed!')
                continue
            self.say(f'please press {button_name} button')
            while not getattr(self, trigger_name):
                pass
            self.say('thank you')
        self.say(f'please lift me up')
        self.wait_until_moved()
        self.say('thank you')
        self.background(self.ambulance, 10)
        self.say('I am blinking my forehead')
