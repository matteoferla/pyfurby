from distutils.core import setup
import os
here = os.path.abspath(os.path.dirname(__file__))


requires = [
    'Adafruit-Blinka', # circuitpython: 'board', 'digitalio', 'pulseio'
    'mpu6050', #gyro
    'pyttsx3'
]

long_description = open(os.path.join(here, 'README.md')).read()

# ============================

setup(
    name='pyfurby',
    version='0.1',
    packages=['pyfurby'],
    url='https://github.com/matteoferla/pyfurby',
    license='MIT',
    author='matteoferla',
    author_email='',
    description='Controlling the various parts of the Furby with Python and a Pi Zero',
    long_description=long_description,
    install_requires=requires
)
