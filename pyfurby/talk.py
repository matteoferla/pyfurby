import pyttsx3

class FurbyTalk:
    def __init__(self, voice_name:str='en-scottish+m4', voice_volume:int=0.7, voice_rate:int=200):
        self.engine = pyttsx3.init()
        self.volume = voice_volume
        self.engine.setProperty('voice', voice_name)
        self.engine.setProperty('rate', voice_rate)

    def say(self, text):
        """
        convert the ``text`` to speech and play it.

        * To say in a different language change ``voice_name``
        * To say in a different volume change ``voice_volume`` (0-1)
        * To say in a different rate change ``voice_rate` (200 is default).

        This gets overwitten.

        :param text: text to say
        :return:
        """
        self.engine.say(text)
        self.engine.runAndWait()

    def _get_volume(self):
        """
        :return: volume of speech
        """
        return self.engine.getProperty('volume')

    def _set_volume(self, volume: float):
        assert 1. >= volume >= 0.
        self.engine.setProperty('volume', volume)

    volume = property(_get_volume, _set_volume)

    def _get_rate(self):
        """
        :return: rate of speech
        """
        return self.engine.getProperty('rate')

    def _set_rate(self, rate: float):
        self.engine.setProperty('rate', rate)

    rate = property(_get_rate, _set_rate)

