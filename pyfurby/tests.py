class TestFurby:
    def tests(self):
        for button_name, trigger_name in [('mouth', 'bitten'),
                                          ('chest', 'fore_squeezed'),
                                          ('back', 'aft_squeezed')]:
            self.say(f'please press {button_name} button')
            while not getattr(self, trigger_name):
                pass
            self.say('thank you')
        self.say(f'please lift me up')
        self.wait_until_moved()
        self.say('thank you')