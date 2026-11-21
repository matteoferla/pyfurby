"""Hardware-free regression tests for disconnected cycle-switch handling."""
import runpy
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch


class MotorSafetyTests(unittest.TestCase):
    def setUp(self):
        modules = {name: types.ModuleType(name) for name in ('digitalio', 'board', 'pwmio')}
        with patch.dict(sys.modules, modules):
            motor_class = runpy.run_path(str(Path(__file__).parents[1] / 'pyfurby' / 'motor.py'))['FurbyMotor']
        self.motor = object.__new__(motor_class)
        self.motor.cycle_pin = types.SimpleNamespace(value=True)
        self.halted = False
        self.motor.halt = self.halt

    def halt(self):
        self.halted = True

    def test_missing_switch_stops_motor(self):
        with self.assertRaises(TimeoutError):
            self.motor.wait_until_revolution(timeout=0)
        self.assertTrue(self.halted)

    def test_triggered_switch_returns(self):
        self.motor.cycle_pin.value = False
        self.motor.wait_until_revolution(timeout=0)
        self.assertFalse(self.halted)

    def test_gpio_read_failure_stops_motor(self):
        class BrokenPin:
            @property
            def value(self):
                raise OSError('GPIO unavailable')
        self.motor.cycle_pin = BrokenPin()
        with self.assertRaises(OSError):
            self.motor.wait_until_revolution()
        self.assertTrue(self.halted)


if __name__ == '__main__':
    unittest.main()
