class FurbySound:

    soundcard_status_file = '/proc/asound/card0/pcm0p/sub0/status'

    @property
    def playing(self):
        """
        :return: Is the sound card in use?
        """
        with open(self.soundcard_status_file, 'r') as fh:
            value = fh.read()
        if value == 'RUNNING':
            return True
        else:  # 'closed'
            return False