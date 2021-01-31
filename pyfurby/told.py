# SpeechRecognition
import speech_recognition as sr
import pyaudio, time, wave

class ToldFurby:
    speech_recogniser = sr.Recognizer()


    def listen(self,
               format: int = pyaudio.paInt32,
               chunk:int= 4096,
               rate:int = 16000,
               temp_filename:str = 'temp.wav'):
        """
        Uses the speech_recognition module.
        However, due to the

        :param format:
        :param chunk:
        :param rate:
        :param temp_filename:
        :return:
        """

        # set up stream
        p = pyaudio.PyAudio()
        stream = p.open(format=format,
                        channels=2,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)
        # record
        frames = []
        tock = time.time()
        try:
            while not self.squeezed or time.time() - tock < 2:
                frames.append(stream.read(chunk))
        except: # it whistles otherwise
            stream.stop_stream()
            stream.close()
        stream.stop_stream()
        stream.close()
        p.terminate()
        # save
        wf = wave.open(temp_filename, 'wb')
        wf.setnchannels(2)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        # read and convert
        with sr.AudioFile('temp.wav') as source:
            audio = self.speech_recogniser.record(source)
        return self.speech_recogniser.recognize_google(audio)

    def _resolve_command(self, cmd, *args, **kwargs):
        getattr(self, cmd)(*args, **kwargs)

    def fill_keywords(self):
        self.keywords = {'hello': lambda decree: self.say("Hello"),
                         'execute': self.excute,
                         'pretty': lambda decree: self.flutter(),
                         'your name': lambda decree: self.say("My name is Furby")
                         }

    def be_told(self):
        # listen speech to text.
        # ????
        decree = self.listen()
        for keyword, action in self.keywords.items:
            if all([word in decree for word in keyword.split()]):
                action(decree)

    def excute(self, degree):
        commands = degree.split('execute')[1].strip().split()
        # ...