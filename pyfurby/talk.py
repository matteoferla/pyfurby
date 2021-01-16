import pyttsx3

class FurbyTalk:
    def __init__(self, voice_name:str='en-scottish+m4', voice_volume:int=0.7, voice_rate:int=200):
        self.engine = pyttsx3.init()
        self.volume = voice_volume
        self.engine.setProperty('voice', voice_name)
        self.engine.setProperty('rate', voice_rate)

    def say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def _get_volume(self):
        return self.engine.engine.getProperty('volume')

    def _set_volume(self, volume: float):
        assert 1. >= volume >= 0.
        self.engine.engine.setProperty('volume', volume)

    volume = property(_get_volume, _set_volume)

    def _get_rate(self):
        return self.engine.engine.getProperty('rate')

    def _set_rate(self, rate: float):
        self.engine.engine.setProperty('rate', rate)

    rate = property(_get_rate, _set_rate)

