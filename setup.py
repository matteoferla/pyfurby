from setuptools import setup, find_packages
import os
here = os.path.abspath(os.path.dirname(__file__))


requires = [
    'Flask',
    'Adafruit-Blinka', # circuitpython: 'board', 'digitalio', 'pulseio'
    'mpu6050-raspberrypi', #gyro
    'pyttsx3',
    #'smbus'
]

long_description = open(os.path.join(here, 'README.md')).read()

# ============================

setup(
    name='pyfurby',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/matteoferla/pyfurby',
    license='MIT',
    author='matteoferla',
    author_email='matteo.ferla@gm',
    description='Controlling the various parts of the Furby with Python and a Pi Zero',
    long_description=long_description,
    install_requires=requires
)
