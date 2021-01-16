import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'board', 'digitalio', 'pulseio' #wrong as circuitpython is installed with blinka something.
    'mpu6050', #gyro
    'pyttsx3'
]

setup(
    name='Pyfurby',
    version='0.0',
    description='Controlling the various parts of the Furby with Python and a Pi Zero',
    long_description=open(os.path.join(here, 'README.md')),
    classifiers=[
        'Programming Language :: Python',
    ],
    author='Matteo Ferla',
    author_email='',
    url='https://github.com/matteoferla/Somewhat-Smart-Home',
    keywords='Furby',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires
)
