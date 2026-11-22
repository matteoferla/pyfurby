import runpy
import sys
import types
import unittest
import warnings
from pathlib import Path
from unittest.mock import patch

FurbyGyro = runpy.run_path(str(Path(__file__).parents[1] / 'pyfurby/gyro.py'))['FurbyGyro']


class OptionalGyroTests(unittest.TestCase):
    def test_missing_library_keeps_furby_usable(self):
        with patch.dict(sys.modules, {'mpu6050': None}), warnings.catch_warnings(record=True) as seen:
            gyro = FurbyGyro()
        self.assertTrue(seen)
        self.assertFalse(gyro.is_lifted())
        self.assertFalse(gyro.is_moved())
        with self.assertRaises(RuntimeError):
            gyro.wait_until_moved()

    def test_disconnected_sensor_warns_instead_of_aborting(self):
        module = types.ModuleType('mpu6050')
        def disconnected(address):
            raise OSError('No I2C sensor')
        module.mpu6050 = disconnected
        with patch.dict(sys.modules, {'mpu6050': module}), self.assertWarns(UserWarning):
            gyro = FurbyGyro()
        with self.assertRaises(RuntimeError):
            _ = gyro.temperature

    def test_connected_sensor_still_detects_motion(self):
        module = types.ModuleType('mpu6050')
        module.mpu6050 = lambda address: types.SimpleNamespace(get_gyro_data=lambda: {'x': 0, 'y': 0, 'z': 15})
        with patch.dict(sys.modules, {'mpu6050': module}):
            gyro = FurbyGyro()
        self.assertTrue(gyro.is_lifted())
        self.assertFalse(gyro.is_moved())
