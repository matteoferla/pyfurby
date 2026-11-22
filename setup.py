from setuptools import setup, find_packages
import os
here = os.path.abspath(os.path.dirname(__file__))

from warnings import warn
import platform

if platform.uname().machine != 'armv6l':
    warn('This can only be installed on a Raspberry Pi Zero')

requires = [
    'Flask',
    'waitress',
    'requests',
    'gpiod>=2.2.2,<3',
    'Adafruit-Blinka-Raspberry-Pi-PWM>=1.0.2',
    'pyserial',
    'Adafruit-Blinka>=10.2.0', # CircuitPython GPIO and pwmio compatibility
    'mpu6050-raspberrypi', #gyro
    'pyttsx3',
    #'smbus'
]

long_description = open(os.path.join(here, 'README.md')).read()

# ============================

setup(
    name='pyfurby',
    version='0.2.0',
    packages=find_packages(),
    url='https://github.com/matteoferla/pyfurby',
    license='MIT',
    author='matteoferla',
    author_email='matteo.ferla@gmail.com',
    description='Controlling the various parts of the Furby with Python and a Pi Zero',
    long_description=long_description,
    extras_require={"notebooks": ["jupyterlab", "ipykernel", "SpeechRecognition"]},
    install_requires=requires
)
