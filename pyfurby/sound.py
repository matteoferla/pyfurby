class FurbySound:

    soundcard_status_file = '/proc/asound/sndrpigooglevoi/pcm0p/sub0/status'

    @property
    def playing(self):
        """
        :return: Is the sound card in use?
        """
        try:
            with open(self.soundcard_status_file, 'r') as fh:
                value = fh.read()
        except FileNotFoundError:
            return False
        if 'RUNNING' in value:
            return True
        else:  # 'closed'
            return False
