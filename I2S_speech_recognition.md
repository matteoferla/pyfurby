## I2S and speech_recognition

## Tyranny of sunken costs
The USB microphone had issues in that it was intermittent —sensitive to the tiniest movement to the shim.
So I went with the I2S microphone.

The I2S microphone broke the PWM audio and I assumed the I2S Amp would be better than 
PWM audio with 10 nF and amplifier. However, the sound quality is worse. Okay the ~40 mm speaker is a 32 Ohm 0.25 W speaker.

To add insult to injury it only works when specifying the format to 32bit FLAC as opposed to 24bit.
This means it does not work with AlexaPi out of the box.
And `speech_recognition.Microphone` has issues, but due to the channels.

    >>> dict(enumerate(sr.Microphone.list_microphone_names()))
    {0: 'snd_rpi_i2s_card: simple-card_codec_link snd-soc-dummy-dai-0 (hw:0,0)',
     1: 'sysdefault',
     2: 'speakerbonnet',
     3: 'dmixer',
     4: 'softvol',
     5: 'dmix',
     6: 'default'}

Say we go with `4`.

    import speech_recognition as sr
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=4)
    mic.format = pyaudio.paInt32 # redundant as it is already int(2)
    with mic as source:
        audio = r.listen(source, timeout=5)
    r.recognize_google(audio)

Gives

    OSError: [Errno -9998] Invalid number of channels
    
At the context manager step for `mic`. Turns out its the same object that just gets turned on

    import inspect

    print(inspect.getsource(mic.__enter__))
    
Gives

    def __enter__(self):
        assert self.stream is None, "This audio source is already inside a context manager"
        self.audio = self.pyaudio_module.PyAudio()
        try:
            self.stream = Microphone.MicrophoneStream(
                self.audio.open(
                    input_device_index=self.device_index, channels=1,
                    format=self.format, rate=self.SAMPLE_RATE, frames_per_buffer=self.CHUNK,
                    input=True,  # stream is an input stream
                )
            )
        except Exception:
            self.audio.terminate()
            raise
        return self

So two things get filled `.audio` (`pyaudio.PyAudio` instance) and steam, 
which is a `sr.Microphone.MicrophoneStream` instance, which is a wrapper for a `pyaudio.Stream` object.

Recording audio works —oddly even when setting channel to one.
Curiously, when something goes wrong it shrieks, unless the following is run:

    stream.stop_stream()
    stream.close()
    
However, combining the two

    mic.audio = pyaudio.PyAudio()
    stream = mic.audio.open(
                #input_device_index=mic.device_index, 
                format=pyaudio.paInt32,
                channels=2,
                rate=16000,
                input=True,
                frames_per_buffer=4096) 
    mic.stream = sr.Microphone.MicrophoneStream(stream)
    try:
        audio = r.listen(mic, timeout=5)
    except WaitTimeoutError:
        pass
    finally:
        #mic.__exit__.__call__() #could call in with 'exc_type', 'exc_value', and 'traceback'
        stream.stop_stream()
        stream.close()   
    
If `input_device_index=mic.device_index` is uncommented I get `OSError: [Errno -9998] Invalid number of channels` 
while otherwise it timeouts —annoying, but just without detecting sound.

    import pyaudio
    import wave
    import time
    
    CHUNK = 4096
    FORMAT = pyaudio.paInt32
    CHANNELS = 1
    RATE = 16000 
    WAVE_OUTPUT_FILENAME = "temp.wav"
    
    p = pyaudio.PyAudio()
    
    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK) 
    
    frames = []
    tock = time.time()
    while not furby.squeezed or time.time() - tock < 2:
        frames.append(stream.read(CHUNK))
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    with sr.AudioFile('test.wav') as source:
        audio = r.record(source)
    msg = r.recognize_google(audio)
    furby.say(msg)