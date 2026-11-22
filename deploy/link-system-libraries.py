"""Link selected Raspbian native libraries into an activated Furby venv."""
from pathlib import Path
from importlib.machinery import EXTENSION_SUFFIXES
import sys
import sysconfig

if sys.prefix == sys.base_prefix:
    raise SystemExit('Run this script with the Furby virtual environment Python')

site = Path(sysconfig.get_path('purelib'))
system = Path('/usr/lib/python3/dist-packages')
suffix = EXTENSION_SUFFIXES[0]
patterns = [
    'RPi', 'rpi_lgpio-*.egg-info', 'lgpio.py', '_lgpio' + suffix,
    'lgpio-*.egg-info', 'smbus' + suffix, 'smbus-*.egg-info',
    'spidev' + suffix, 'spidev-*.egg-info',
    'numpy', 'numpy.libs', 'numpy-*.dist-info', 'numpy-*.egg-info',
    'pandas', 'pandas-*.dist-info', 'pandas-*.egg-info',
    'pyaudio', 'PyAudio-*.egg-info', 'pyaudio-*.dist-info',
    'dateutil', 'python_dateutil-*.egg-info', 'python_dateutil-*.dist-info',
    'pytz', 'pytz-*.egg-info', 'pytz-*.dist-info',
    'six.py', 'six-*.egg-info', 'tzdata', 'tzdata-*.dist-info',
]
for pattern in patterns:
    for source in system.glob(pattern):
        destination = site / source.name
        if not destination.exists() and not destination.is_symlink():
            destination.symlink_to(source)
print('Selected distro native libraries linked into the virtual environment.')
