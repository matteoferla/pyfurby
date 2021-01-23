## Standard stuff
### SSH and update
Did the usual as discussed in [setting up in the Smart home repo](https://github.com/matteoferla/Somewhat-Smart-Home/blob/main/setting_up.md).

* Flashed a microSD with Raspian
* Added `ssh` file to boot drive before ejecting it from computer.
* Added Wifi supplicant
* SSHed using default user `pi` and password `raspberry`
* set password to something else
* fixed bash_profile
* updates


    sudo passwd
    echo "source ~/.bashrc" >>  ~/.bash_profile
    echo "source ~/.profile" >>  ~/.bash_profile
    sudo apt-get -y update
    sudo apt-get -y upgrade
    
* added to `.bash_profile` the local pi (but most times did `sudo pip3`)
    
    
    export PATH=$PATH:/home/pi/.local/bin

* sorted Python3


    sudo apt-get -y install python3-pandas
    sudo apt-get -y  install python3-dev
    sudo apt-get -y  install python3-pip  
    sudo pip3 install jupyter RPi.GPIO waitress flask Flask-Ask Flask-SQLAlchemy beautifulsoup4 Pillow picamera
 
* Jupyter and Slack notification on start up
 
 
    nano run_jupyter.sh # see ../setting_up.md
    sudo nano /etc/systemd/system/jupyter.service
    jupyter notebook password
    sudo systemctl start jupyter
    sudo systemctl enable jupyter
    
* and setting hostname to `furby`.


    sudo raspi-config 

## Speaker

> Amazon no longer allows AlexaPi & co. to pay music. 
> And there's a fur coat in between and a motor to compete with so sound quality is not a must.

* 5V
* GPIO13 (mono)
* native 32Ω speaker

The original tutorial speaks of the speaker being poor.
In mine it's not that bad and actually better than two 8Ω 1W speakers in loudness, so I am sticking with it.
It still needs an Amp, using a PAM8302A audio amp wiring V<sub>CC</sub> to 5V (tinny, but loud).
That is with `alsamixer` set to max and the variable resistor left as is.

Audio-in with a 10 nF ceramic cap (manually determined) to gnd can stop the tinniness, but lowers volume.

The best explanation of the PWM audio I found is [this post](https://librpip.frasersdev.net/peripheral-config/pwm0and1/).
To configure PWM audio add to `/boot/config.txt`, but first copy it as this can get blanked:

    mkdir backup
    cp /boot/config.txt backup/boot_config.txt
    
However, it really has only four lines

    dtparam=i2c_arm=on
    dtparam=i2s=on
    dtparam=audio=on
    dtoverlay=pwm,pin=13,func=4

The latter is for mono sound: for discussion about `func` see https://sudomod.com/forum/viewtopic.php?t=480&start=30
Two channel would have been `pwm-2chan`
After any edits to the boot/config file a reset is required.   

    sudo nano /boot/config.txt 
    sudo shutdown -r now

Here are some commands to test the sound
    
* list speakers: `aplay -l`
* volume control: `alsamixer`
* play loop: `speaker-test -t wav -c 1`
* play once: `aplay /usr/share/sounds/alsa/Front_Center.wav`

### Espeak

The text to speech system in Linux is `eSpeak` and the `pyttsx3` python wrapper makes it possible to use in Python,
in that very this is a C++ wrapper way.

    sudo apt-get install espeak
    sudo pip3 install pyttsx3

## Mouth sensor and forehead

To test the mouth and leds, I used the following, in the Jupyter notebook.
NB. The photoresistor is just for aesthetics as reading it would be a pain.

Pin test:

    import board, digitalio, time
    
    for color, pin in {'green': board.D24, 'red': board.D14}.items():
        print(color)
        with digitalio.DigitalInOut(pin) as led:
            led.direction = digitalio.Direction.OUTPUT
            led.value = True
            time.sleep(2)
            led.value = False
            
Test buttons:

    with digitalio.DigitalInOut(board.D18) as switch:
        switch.direction = digitalio.Direction.INPUT
        switch.pull = digitalio.Pull.UP
        print('pressed' if not switch.value else 'unpressed')


## Motor

I debated using just a rectifier as opposed to TB6612, as it's overkill as currently used,
but a driver has the advantage of being able to go backwards (H-bridge business).
There is a motor cycle sensor on the Furby, so going backwards would be essential to make it chuckle etc.
This was a great decision as this has been half my fun.

* https://learn.adafruit.com/adafruit-tb6612-h-bridge-dc-stepper-motor-driver-breakout/pinouts
* https://github.com/Howchoo/random-bits/blob/master/furlexa-echo-furby/pi-furby-dc-motor-TB6612-pi_bb.png

NB. AIN1 comes after AIN2 on the TB6612

The motion in the original really useful tutorial is triggered by reading the `/proc/asound/card0/pcm0p/sub0/status` status.
Namely if there is a sound playing it moves. Which is not great.

The functionality is better served with the [Python API](API.md), i.e. adding a service which runs in Python

    from pyfurby import Furby
    furby = Furby()
    furby.move_on_play() # while True loop

As this would allow some variations, such as movement dependent triggers etc.
In fact, this is for the Alexa part, which is not the key feature anymore.
Filming myself having a chat to a silly fluffy thing is.

### Thoughts on sound <-> Motor
 Signal out of the Amp isn't strong enough to trigger movement.
Plus, signal from PWM, even at low frequencies, just results in a slow movement, not a jerky one.
So one would need to have an intensity based cutoff to make it jerky.
However, there is no space to add custom circuitry like bandpass filters etc.
The very minimum would be a GPIO13 -> resistor -> PNP transistor base -> TB6612 and that is already too much.

## USB Microphone

* list mikes: `arecord -l`
* test mikes: `arecord -D plughw:1,0 -d 3 test.wav && aplay test.wav`

This had all sorts of issues. Even when plugged into the Pi via a shim it was temperamental,
while was perfect on my laptop.

## I2S microphone

I2S microphone installation as per Adafruit's instruction requires a quick shoddy hack:

    sudo ln -s /lib/modules/5.4.83+ /lib/modules/5.4.72+
    
With this the installation works fine.
    
    cd ~
    sudo pip3 install --upgrade adafruit-python-shell
    wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2smic.py
    sudo python3 i2smic.py
    arecord -D plughw:0 -c1 -r 48000 -f S32_LE -t wav -V mono -v file.wav

So the microphone works but the PWA does not. I am using GPIO13 so it should not matter.

    lsmod | grep pwm
    pwm_bcm2835            16384  1
    
PWM_1 is GPIO13 so that is correct, but `aplay -l` cannot see it. So it's an also problem.


## Alexa

This differs from the tutorial and is more straightforward.

Using AlexaPi: https://github.com/alexa-pi/AlexaPi/wiki/Installation

This will install via pip3 `backports.functools-lru-cache, certifi, more-itertools, cheroot, pytz, jaraco.functools, tempora, portend, zc.lockfile, cherrypy, humanfriendly, coloredlogs, idna, pocketsphinx, pyaudio, python-vlc, pyyaml, urllib3, requests, webrtcvad`

    sudo apt-get install git
    cd /opt
    sudo git clone https://github.com/alexa-pi/AlexaPi.git
    sudo ./AlexaPi/src/scripts/setup.sh

This will require a few keys to be generated via the Amazon dev site:

* Amazon ID: `👾👾👾`
* Product Name: `Furbexa`
* Product ID: `Furbexa`
* Amazon ID: `👾👾👾`
* Security Profile: `Furbexa`
* Security Profile ID: `amzn1.application.👾👾👾`
* Client ID: `amzn1.application-oa2-client.👾👾👾`
* Client Secret: `👾👾👾`

Also, the permissions IP within the network (192.168.1.xx) are important as the Pi is headless.

The refresh token comes from `/usr/bin/python3 /opt/AlexaPi/src/auth_web.py` run as root.
Which is required by `/usr/bin/python3 /opt/AlexaPi/src/main.py`.
Which is run by the alexapi service, which is present in `/usr/lib/systemd/system/AlexaPi.service`.

Changing

    sudo nano /etc/opt/AlexaPi/config.yaml
    
* GPIO18 --> sensor for mouth (this is a pull-up input (positive), not negative!)
* GPIO24 --> green light
* GPIO14 --> red light