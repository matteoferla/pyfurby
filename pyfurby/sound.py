class FurbySound:

    soundcard_status_file = '/proc/asound/card0/pcm0p/sub0/status'

    @property
    def playing(self):
        with open(self.soundcard_status_file, 'r') as fh:
            value = fh.read()
        if value == 'RUNNING':
            return True
        else:  # 'closed'
            return False